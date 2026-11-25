---
last-updated: 2026-11-25
---

# Section 2: Implementing a VPC Network (~20%)

Section 1 was about choosing; this section is about building. The exam expects you to know what each resource is, which flags and settings matter, which project and role each step needs, and what silently breaks when a step is missed. The four tasks are:

| Task | Scope |
|------|-------|
| 2.1 | Configure VPCs: networks, subnets, firewall rules or policies, private services access, private pools, peering, Shared VPC and its IAM, access to Google APIs, subnet expansion, VPC Service Controls |
| 2.2 | Configure routing: static and dynamic, regional vs global dynamic routing, tags and priority, internal load balancer next hop, custom route exchange over peering and NCC, policy-based routing |
| 2.3 | Configure Network Connectivity Center: spoke types, topologies, Private NAT and PSC propagation, CIDR filters, monitoring |
| 2.4 | Configure and maintain GKE cluster networking |

Firewall rules are introduced here because they are part of "creating VPC resources", but the full firewall strategy (Cloud NGFW tiers, hierarchical policies, migration) is in [Section 6.2](06-network-security.md#62-cloud-ngfw-policies-and-vpc-firewall-rules). Design reasoning for everything here is in [Section 1](01-designing-planning-vpc-network.md).

---

## 2.1 Configuring VPCs

### Creating networks and subnets

Always create **custom mode** networks for production so you control every range. Two network-level settings are worth setting deliberately at creation: the **dynamic routing mode** (regional or global, changeable later) and the **MTU** (1,460 default, 1,300-8,896 allowed).

```bash
# Custom mode VPC, regional dynamic routing, default MTU
gcloud compute networks create production-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional \
  --mtu=1460

# A general-purpose subnet with Private Google Access and flow logs
gcloud compute networks subnets create app-subnet \
  --network=production-vpc \
  --region=us-central1 \
  --range=10.0.2.0/24 \
  --enable-private-ip-google-access \
  --enable-flow-logs

# A GKE subnet: primary range for nodes, secondary ranges for Pods and Services
gcloud compute networks subnets create gke-subnet \
  --network=production-vpc \
  --region=us-central1 \
  --range=10.0.10.0/24 \
  --secondary-range=pods=10.4.0.0/14,services=10.8.0.0/20 \
  --enable-private-ip-google-access

# A dual-stack subnet with internal IPv6
gcloud compute networks subnets create v6-subnet \
  --network=production-vpc \
  --region=us-central1 \
  --range=10.0.20.0/24 \
  --stack-type=IPV4_IPV6 \
  --ipv6-access-type=INTERNAL
```

Internal IPv6 requires the network to have a ULA range (`--enable-ula-internal-ipv6` on the network). Remember that each subnet reserves four IPv4 addresses and the smallest subnet is a `/29`.

**Special-purpose subnets** are created with `--purpose`:

| Purpose | Used by |
|---------|---------|
| `PRIVATE` (default) | VMs, nodes, internal passthrough LB IPs |
| `REGIONAL_MANAGED_PROXY` | Proxy-only subnet for regional Envoy-based load balancers and Secure Web Proxy |
| `GLOBAL_MANAGED_PROXY` | Proxy-only subnet for cross-region internal load balancers |
| `PRIVATE_SERVICE_CONNECT` | NAT subnet for a PSC service attachment (producer side) |
| `PRIVATE_NAT` | Source addresses for Private NAT |

```bash
# Proxy-only subnet (one active per region per network for this purpose)
gcloud compute networks subnets create proxy-only-us-central1 \
  --purpose=REGIONAL_MANAGED_PROXY \
  --role=ACTIVE \
  --network=production-vpc \
  --region=us-central1 \
  --range=10.129.0.0/23
```

The same thing in Terraform, for reference:

```hcl
resource "google_compute_network" "production_vpc" {
  name                    = "production-vpc"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "gke_subnet" {
  name                     = "gke-subnet"
  ip_cidr_range            = "10.0.10.0/24"
  region                   = "us-central1"
  network                  = google_compute_network.production_vpc.id
  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.4.0.0/14"
  }
  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.8.0.0/20"
  }
}
```

### Firewall rules and policies (creation basics)

Every VPC has two **implied** rules you cannot see or delete: **deny all ingress** and **allow all egress**, at the lowest priority. Default networks also get pre-populated `default-allow-*` rules, which custom networks do not. VPC firewall rules are **stateful**: allowing a connection allows its return traffic.

```bash
# Allow Google health check and proxy ranges to reach load balancer backends
gcloud compute firewall-rules create allow-health-checks \
  --network=production-vpc \
  --allow=tcp \
  --source-ranges=35.191.0.0/16,130.211.0.0/22 \
  --target-tags=lb-backend

# Allow IAP TCP forwarding for SSH without public IPs
gcloud compute firewall-rules create allow-iap-ssh \
  --network=production-vpc \
  --allow=tcp:22 \
  --source-ranges=35.235.240.0/20

# Identity-based: app tier service account to database service account
gcloud compute firewall-rules create allow-app-to-db \
  --network=production-vpc \
  --allow=tcp:5432 \
  --source-service-accounts=app-sa@PROJECT.iam.gserviceaccount.com \
  --target-service-accounts=db-sa@PROJECT.iam.gserviceaccount.com
```

Network firewall policies are the newer model and are what Google recommends going forward; see [Section 6.2](06-network-security.md#62-cloud-ngfw-policies-and-vpc-firewall-rules).

### Private services access subnet and private pools

**Private services access** (PSA) connects your VPC to Google-managed producer networks (Cloud SQL, Memorystore, Filestore and others) through a peering called `servicenetworking-googleapis-com`. You allocate a range with purpose `VPC_PEERING`, then create the connection:

```bash
# 1. Reserve a range for Google-managed services
gcloud compute addresses create google-managed-services \
  --global \
  --purpose=VPC_PEERING \
  --prefix-length=16 \
  --network=production-vpc

# 2. Create the private connection (a VPC Network Peering under the hood)
gcloud services vpc-peerings connect \
  --service=servicenetworking.googleapis.com \
  --ranges=google-managed-services \
  --network=production-vpc

# 3. Optional: let the producer side learn your custom (e.g. on-prem) routes
gcloud compute networks peerings update servicenetworking-googleapis-com \
  --network=production-vpc \
  --export-custom-routes
```

**Private pools** for Cloud Build are worker pools in a Google-managed network; to let builds reach private resources (a private GKE control plane, an artifact server), you peer the private pool to your VPC through the same service networking connection, using a PSA allocated range. Because that is peering, builds cannot reach on-premises or peered networks unless custom routes are exported.

### Configuring VPC Network Peering

Peering is configured **from both sides**; it only becomes `ACTIVE` when both peerings exist. Subnet routes are always exchanged (IPv4 private ranges); everything else is opt-in:

```bash
gcloud compute networks peerings create hub-to-spoke \
  --network=hub-vpc \
  --peer-project=spoke-project \
  --peer-network=spoke-vpc \
  --export-custom-routes \
  --import-custom-routes

gcloud compute networks peerings create spoke-to-hub \
  --network=spoke-vpc \
  --peer-project=hub-project \
  --peer-network=hub-vpc \
  --import-custom-routes \
  --export-custom-routes

# Exchange subnet routes that use privately used public IPs (PUPI)
gcloud compute networks peerings update hub-to-spoke \
  --network=hub-vpc \
  --export-subnet-routes-with-public-ip \
  --import-subnet-routes-with-public-ip
```

What you must know about peering:

- **Not transitive**: A peered to B and B peered to C does not connect A and C.
- **No overlapping subnet ranges** (primary or secondary) are allowed at creation, and later subnet creation that would overlap is blocked.
- **Custom routes** (static and dynamic) are exchanged only when one side exports and the other imports. Static routes that use **network tags** are never exchanged, and the default internet route is not exchanged, so a peer cannot use your internet egress or Cloud NAT.
- **Firewalls are not shared**: each side writes its own rules referencing the other side's ranges. Network tags and service accounts from the peer cannot be used as sources.
- **Peering group limits**: quotas such as instances and internal forwarding rules apply across a network and its directly peered networks.
- DNS is not shared automatically; use DNS peering or cross-project binding.

### Creating a Shared VPC network and sharing subnets

The Shared VPC Admin (`roles/compute.xpnAdmin`, granted at organization or folder) enables the host project and attaches service projects; the host project's network admins create subnets; service project admins get `roles/compute.networkUser` on the host project or on chosen subnets.

```bash
# Enable the host project and attach a service project
gcloud compute shared-vpc enable host-project
gcloud compute shared-vpc associated-projects add app-project \
  --host-project=host-project

# Subnet-level delegation (least privilege)
gcloud compute networks subnets add-iam-policy-binding app-subnet \
  --project=host-project \
  --region=us-central1 \
  --member='group:app-team@example.com' \
  --role='roles/compute.networkUser'
```

### Assigning IAM permissions for service projects

Humans are only half of it. Google-managed **service agents** in the service project also act on the host network and need roles there:

| Who | Role on host project or subnet | Why |
|-----|-------------------------------|-----|
| Service project admins (people, groups) | `compute.networkUser` on subnets | Create VMs, internal LBs and so on in shared subnets |
| Google APIs service agent `PROJECT_NUMBER@cloudservices.gserviceaccount.com` | `compute.networkUser` | Managed instance groups and other services create resources on your behalf |
| GKE service agent `service-PROJECT_NUMBER@container-engine-robot.iam.gserviceaccount.com` | `compute.networkUser` on the subnet, and `container.hostServiceAgentUser` on the host project | GKE manages node and Pod networking in the host's subnet |
| GKE service agent (optional) | `compute.securityAdmin` on host project, or pre-create firewall rules | GKE creates firewall rules for load balancers and node communication |
| Load balancer frontend owners | `compute.loadBalancerServiceUser` on the backend project | Cross-project backend service referencing |

A frequent failure: the cluster or MIG creation in a service project fails with a permissions error even though the human has `networkUser`, because the service agent does not.

### Configuring access to Google APIs and managed services

Three ways for VMs without external IPs to reach Google APIs:

1. **Private Google Access** (per subnet): VMs with only internal IPs reach Google APIs on their public IPs through Google's network. It needs a route to the API destination with the **default internet gateway** as next hop (the default route works); the VM does not need an external IP. It does not give general internet access.
2. **Private Google Access with the special VIPs**: route `199.36.153.8/30` (`private.googleapis.com`) or `199.36.153.4/30` (`restricted.googleapis.com`, only VPC Service Controls-supported services) and set private DNS so `*.googleapis.com` is a CNAME to the chosen name. This works even if you remove the default route, and is the basis for on-premises access.
3. **Private Service Connect endpoint for Google APIs**: an internal IP you choose in your VPC that targets a bundle (`all-apis` or `vpc-sc`).

```bash
# Private zone so *.googleapis.com resolves to restricted.googleapis.com
gcloud dns managed-zones create googleapis \
  --dns-name=googleapis.com. --visibility=private --networks=production-vpc
gcloud dns record-sets create restricted.googleapis.com. --zone=googleapis \
  --type=A --ttl=300 \
  --rrdatas=199.36.153.4,199.36.153.5,199.36.153.6,199.36.153.7
gcloud dns record-sets create '*.googleapis.com.' --zone=googleapis \
  --type=CNAME --ttl=300 --rrdatas=restricted.googleapis.com.

# Route to the restricted VIP via the default internet gateway
gcloud compute routes create restricted-apis \
  --network=production-vpc \
  --destination-range=199.36.153.4/30 \
  --next-hop-gateway=default-internet-gateway

# PSC endpoint for all Google APIs at an internal address
gcloud compute addresses create psc-apis-ip --global \
  --purpose=PRIVATE_SERVICE_CONNECT --addresses=10.0.254.1 \
  --network=production-vpc
gcloud compute forwarding-rules create pscapis --global \
  --network=production-vpc --address=psc-apis-ip \
  --target-google-apis-bundle=all-apis
```

Note the old exam myth: `restricted` is `.4/30` and `private` is `.8/30`. **Public interfaces** of Google APIs remain reachable through the internet gateway when a VM has an external IP or Cloud NAT; Private Google Access only matters for VMs without them.

Publishing and consuming services with PSC:

```bash
# Producer: NAT subnet + service attachment in front of an internal LB
gcloud compute networks subnets create psc-nat-subnet \
  --network=producer-vpc --region=us-central1 \
  --range=10.100.200.0/24 --purpose=PRIVATE_SERVICE_CONNECT
gcloud compute service-attachments create orders-svc \
  --region=us-central1 \
  --producer-forwarding-rule=orders-ilb \
  --connection-preference=ACCEPT_MANUAL \
  --consumer-accept-list=consumer-project-1=10 \
  --nat-subnets=psc-nat-subnet

# Consumer: endpoint IP in its own subnet pointing at the attachment
gcloud compute addresses create orders-endpoint-ip \
  --region=us-central1 --subnet=consumer-subnet --addresses=10.0.5.100
gcloud compute forwarding-rules create orders-endpoint \
  --region=us-central1 --network=consumer-vpc \
  --address=orders-endpoint-ip \
  --target-service-attachment=projects/PRODUCER/regions/us-central1/serviceAttachments/orders-svc
```

### Expanding subnet ranges after creation

```bash
gcloud compute networks subnets expand-ip-range app-subnet \
  --region=us-central1 --prefix-length=22
```

Expansion is online and non-disruptive, but one-way: you cannot shrink or replace a primary range, the new range must contain the old one and must not overlap other subnets, peered networks or static routes, and auto mode subnets can only grow to `/16`. Secondary ranges cannot be expanded in place; for GKE you add more ranges instead (2.4).

### Configuring VPC Service Controls perimeters

VPC Service Controls (VPC-SC) protects **Google API data** (Cloud Storage, BigQuery and others) against exfiltration by drawing a **service perimeter** around projects. Calls to a **restricted service** from outside the perimeter are denied even with valid IAM, and resources inside cannot copy data to resources outside. It is not a packet firewall; it acts at the API layer.

Building blocks:

- **Access policy**: the organization-level container (one org policy, plus optional scoped policies).
- **Service perimeter** (regular): projects (or VPC networks) inside, plus the list of **restricted services**. **VPC accessible services** limits which APIs can be called from networks inside the perimeter.
- **Access levels** (Access Context Manager): conditions such as source IP ranges, device policy, identities or regions that allow access from outside.
- **Ingress and egress rules**: fine-grained exceptions naming identities, sources, target resources and methods.
- **Perimeter bridges**: let two perimeters share specific projects (ingress/egress rules are usually preferred now).
- **Dry-run mode**: evaluate a new configuration and log would-be violations without enforcing, then promote.

```bash
gcloud access-context-manager perimeters create prod_perimeter \
  --policy=POLICY_ID \
  --title="Production" \
  --resources=projects/123456789 \
  --restricted-services=storage.googleapis.com,bigquery.googleapis.com \
  --access-levels=corp_network

# Try a change in dry-run first
gcloud access-context-manager perimeters dry-run update prod_perimeter \
  --policy=POLICY_ID --add-resources=projects/555555555
```

For private API access from VMs or on-premises into a perimeter, use `restricted.googleapis.com` or a PSC endpoint with the `vpc-sc` bundle, and an access level or ingress rule for on-premises sources. Violations appear in Cloud Audit Logs with a VPC Service Controls `violationReason`; troubleshooting is covered in [Section 5](05-network-operations-monitoring-troubleshooting.md).

---

## 2.2 Configuring VPC routing

### How Google Cloud chooses a route

Routes are in the **VPC network's routing table** and are applied by the virtual network, not by a router VM. Route types:

- **System-generated**: subnet routes for every subnet range, and the default route `0.0.0.0/0` (and `::/0`) to the default internet gateway.
- **Custom static routes**: your destination and next hop (instance, IP, internal passthrough NLB, VPN tunnel, default internet gateway).
- **Dynamic routes**: learned by Cloud Router over BGP.
- **Peering and NCC routes**: subnet and custom routes imported from peers or from the NCC hub.
- **Policy-based routes**: match source, destination and protocol.

Selection order, simplified from Google's documentation:

1. **Policy-based routes** are evaluated first, by priority.
2. If the destination is in a **subnet route**, that subnet route wins. You cannot create a static route that equals or fits inside a subnet range.
3. Otherwise the **most specific destination** (longest prefix) wins.
4. Among equally specific routes, the **lowest priority number** wins (priority 0-65535; static and default routes default to 1000).
5. Equal priority and valid next hops: **ECMP** across them (except multiple internal-LB next hops for the same destination and priority, which is not supported).

Static routes can be limited to VMs carrying specific **network tags**, which is how you send only some VMs through an egress appliance.

```bash
# Static route through a VPN tunnel (classic route-based)
gcloud compute routes create to-onprem \
  --network=production-vpc --destination-range=192.168.0.0/16 \
  --next-hop-vpn-tunnel=tunnel-1 --next-hop-vpn-tunnel-region=us-central1 \
  --priority=100

# Tag-scoped default route through a proxy appliance
gcloud compute routes create egress-via-proxy \
  --network=production-vpc --destination-range=0.0.0.0/0 \
  --next-hop-instance=proxy-vm --next-hop-instance-zone=us-central1-a \
  --tags=use-proxy --priority=500
```

### Static and dynamic routing with Cloud Router

Cloud Router is a fully managed BGP speaker. It does not forward packets; it **programs** routes into the VPC and advertises your prefixes to peers over HA VPN, Interconnect VLAN attachments and router appliances. HA VPN and Interconnect require it (Classic VPN can use static routes).

```bash
gcloud compute routers create hybrid-router \
  --network=production-vpc --region=us-central1 --asn=65001
```

BGP details (ASNs, MED, BFD, custom advertisements and learned routes) are in [Section 4.3](04-hybrid-multicloud-interconnectivity.md#43-configuring-cloud-router).

### Global or regional dynamic routing

```bash
gcloud compute networks update production-vpc --bgp-routing-mode=global
gcloud compute networks describe production-vpc \
  --format="get(routingConfig.routingMode)"
```

- **Regional**: Cloud Router installs learned routes only in its region and advertises only its region's subnets. On-premises cannot reach other regions through that router.
- **Global**: learned routes are installed in all regions. Routes learned in another region get an **inter-region cost** added to their priority, so local paths stay preferred and remote ones act as backup.

A classic symptom: VMs in `europe-west1` cannot reach on-premises while VMs in `us-central1` can, and the only VPN is in `us-central1`. The fix is global dynamic routing mode (or a router and link in Europe).

### Route priorities with global routing and policy-based routing

Priority interacts with three mechanisms:

- **Static vs dynamic**: for the same prefix, the lower priority number wins regardless of type; if equal, Google prefers static over dynamic in its preference ordering.
- **Dynamic route priority** comes from the **MED** received from the peer (base priority), plus the inter-region cost in global mode. You influence inbound-to-Google preference from on-premises by setting MED on your router; you influence on-premises' choice by setting Cloud Router's **advertised route priority**.
- **Policy-based routes** sit above all of this: they are evaluated before subnet and destination routes, so a PBR that matches traffic overrides even a more specific static route. Use `DEFAULT_ROUTING` as the next hop of a higher-priority PBR to exempt traffic (for example, health check ranges) from a broader PBR.

### Internal load balancer as next hop

An **internal passthrough Network Load Balancer** can be the next hop of a static route (and of policy-based routes). This is the standard way to make a group of appliances highly available.

```bash
gcloud compute routes create default-via-nva \
  --network=hub-vpc --destination-range=0.0.0.0/0 \
  --next-hop-ilb=nva-ilb --next-hop-ilb-region=us-central1 \
  --priority=800
```

Behaviors to know: backends need **IP forwarding**; all traffic on all ports is forwarded regardless of the forwarding rule's ports; if all backends fail health checks the route still sends traffic to one of them (it does not withdraw); referencing the LB by **IP address** lets the route be used in peered or NCC-connected networks; **symmetric hashing** keeps both directions of a flow on the same appliance. A forwarding rule with a shared VIP purpose cannot be used as a next hop.

### Custom route import/export over peering and NCC

- **Peering**: `--export-custom-routes` / `--import-custom-routes` per side. Exports include static and dynamic routes (not tag-scoped static routes, and not the default internet route). This is how spokes learn on-premises routes from a hub that holds the VPN or Interconnect. Remember to also advertise spoke ranges to on-premises with Cloud Router **custom advertisement**.
- **NCC**: VPC spokes export their subnet routes to the hub and import routes from other spokes; hybrid spokes export dynamic routes. **Export filters** (include and exclude ranges) on VPC spokes and route-table-based groups control what is shared. Peering subnet routes are not exported by a VPC spoke.

```bash
# Inspect what a peering is actually exchanging
gcloud compute networks peerings list-routes hub-to-spoke \
  --network=hub-vpc --region=us-central1 --direction=OUTGOING
```

### Configuring policy-based routing

Policy-based routes (PBR) match on **source range, destination range and protocol** (not ports), apply to all VMs, tagged VMs, or Interconnect VLAN attachments in a region, and forward to an **internal passthrough NLB** (or `DEFAULT_ROUTING` to skip). They cannot be edited after creation (delete and recreate), are not exchanged over peering, and cannot target PSC endpoints.

```bash
# Send all traffic from on-prem (arriving on VLAN attachments) through inspection
gcloud network-connectivity policy-based-routes create inspect-onprem \
  --network=projects/PROJECT/global/networks/hub-vpc \
  --source-range=192.168.0.0/16 \
  --destination-range=0.0.0.0/0 \
  --ip-protocol=ALL \
  --next-hop-ilb-ip=10.0.2.10 \
  --interconnect-attachment-region=us-central1 \
  --priority=100

# Exempt Google health check probes from a VM-scoped PBR
gcloud network-connectivity policy-based-routes create skip-hc \
  --network=projects/PROJECT/global/networks/hub-vpc \
  --source-range=35.191.0.0/16 --destination-range=0.0.0.0/0 \
  --ip-protocol=ALL --next-hop-other-routes=default-routing --priority=50
```

---

## 2.3 Configuring Network Connectivity Center

NCC is Google Cloud's hub-and-spoke connectivity service. A **hub** is a global management resource that holds route tables; **spokes** attach networks or hybrid links to it. Unlike peering, connectivity is transitive within the rules of the hub.

### Spoke types

| Spoke type | What it attaches | Notes |
|-----------|------------------|-------|
| **VPC spoke** | A VPC network (any project, even another organization) | Exchanges subnet routes; supports include/exclude export ranges; overlapping subnets need Private NAT or exclusions |
| **Hybrid spoke** | HA VPN tunnels, Cloud Interconnect VLAN attachments (Dedicated, Partner, Cross-Cloud) or router appliance VMs | Exports dynamic routes learned by Cloud Router; can enable **site-to-site data transfer** |
| **Router appliance spoke** (a kind of hybrid spoke) | Third-party router or SD-WAN VMs that BGP-peer with Cloud Router | How SD-WAN is integrated |
| **Producer VPC spoke** | A producer network reached through VPC Network Peering (for example a PSA producer) | Makes peered managed services reachable from other spokes |

Rules worth remembering: different spokes must use different ASNs; site-to-site data transfer requires the hybrid spokes to be in the same VPC network and is available only in supported locations; a VPC spoke cannot export peering subnet routes.

### Managing the topology: mesh and star

```bash
# Mesh hub (default): every spoke reaches every spoke
gcloud network-connectivity hubs create corp-hub --preset-topology=mesh

# Star hub: center group reaches all, edge group reaches only center
gcloud network-connectivity hubs create seg-hub --preset-topology=star

gcloud network-connectivity spokes linked-vpc-network create shared-svcs \
  --hub=seg-hub --vpc-network=projects/svc-proj/global/networks/shared-vpc \
  --group=center --global
gcloud network-connectivity spokes linked-vpc-network create team-a \
  --hub=seg-hub --vpc-network=projects/team-a/global/networks/team-a-vpc \
  --group=edge --global
```

- **Mesh**: one spoke group, full any-to-any.
- **Star**: two groups created with the hub, `center` and `edge`. Each group has its own route table: center spokes learn routes to everything; edge spokes learn routes only to center spokes. Use it for shared services or segmentation where teams must not talk to each other. Hybrid spokes with site-to-site data transfer must be in the center group.
- The **preset topology cannot be changed** after the hub is created; to switch, build a new hub.

Spokes from other projects can be proposed to the hub and must be **accepted** by the hub administrator, which keeps the hub owner in control.

### Private NAT and PSC propagation

- **Private NAT for NCC spokes** lets a VPC spoke whose subnets overlap with another spoke still reach it. You create a `PRIVATE_NAT` subnet and a Cloud NAT gateway of type `PRIVATE` on a Cloud Router, with a NAT rule matching traffic toward the hub. Outbound connections are source-NATed into the Private NAT range; replies come back; unsolicited inbound is not allowed. TCP and UDP only.

```bash
gcloud compute networks subnets create pnat-subnet \
  --network=team-b-vpc --region=us-central1 \
  --range=100.64.10.0/29 --purpose=PRIVATE_NAT
gcloud compute routers create pnat-router --network=team-b-vpc --region=us-central1
gcloud compute routers nats create pnat-gw --router=pnat-router \
  --region=us-central1 --type=PRIVATE \
  --nat-custom-subnet-ip-ranges=overlapping-subnet
gcloud compute routers nats rules create 1 --nat=pnat-gw --router=pnat-router \
  --region=us-central1 \
  --match='nexthop.hub == "//networkconnectivity.googleapis.com/projects/HUB_PROJECT/locations/global/hubs/corp-hub"' \
  --source-nat-active-ranges=pnat-subnet
```

- **PSC connection propagation**: when enabled on the hub, a PSC endpoint in one VPC spoke is propagated so that other VPC spokes reach the same published service through the hub, instead of each VPC creating its own endpoint. Endpoints in excluded subnets are not propagated. A subnet using Private NAT toward the hub cannot use propagated PSC connections, and a Private NAT gateway using `--nat-all-subnet-ip-ranges` breaks propagation for the whole spoke; use `--nat-custom-subnet-ip-ranges` to limit it to the overlapping subnets.

### IP/CIDR range filters for spokes

VPC spokes accept **exclude export ranges** and **include export ranges** to control which subnet routes enter the hub, and can export IPv4, IPv6 or both. Typical uses: exclude an overlapping subnet that is reachable only via Private NAT, or include only a summary block of production ranges.

```bash
gcloud network-connectivity spokes linked-vpc-network create team-b \
  --hub=corp-hub --global \
  --vpc-network=projects/team-b/global/networks/team-b-vpc \
  --exclude-export-ranges=10.50.0.0/16 \
  --include-export-ranges=10.0.0.0/8
```

### Monitoring and troubleshooting NCC

- Inspect the **hub route tables** (`gcloud network-connectivity hubs route-tables routes list`) to see which prefixes each group knows and their next-hop spoke.
- Check **spoke state** (active, pending acceptance, inactive) and the reason for rejected or overlapping ranges.
- Use **Network Topology** and **Connectivity Tests** (both understand NCC) to trace a path, and Cloud Audit Logs for who changed what.
- Common faults: overlapping subnet ranges rejected at spoke creation; expecting peered networks to be reachable through a VPC spoke; star edge spokes expecting to reach each other; hybrid routes not reaching spokes because the hybrid link is not a spoke.

---

## 2.4 Configuring and maintaining GKE clusters

### VPC-native clusters using alias IPs

VPC-native clusters allocate Pod IPs from a subnet secondary range as **alias IPs** on the node NIC. Pod IPs are therefore real VPC addresses: routable across peering and hybrid links, visible to firewall rules and flow logs, and not dependent on custom routes. Routes-based clusters are legacy.

```bash
gcloud container clusters create prod-cluster \
  --region=us-central1 \
  --network=production-vpc --subnetwork=gke-subnet \
  --enable-ip-alias \
  --cluster-secondary-range-name=pods \
  --services-secondary-range-name=services \
  --max-pods-per-node=64
```

If you omit the secondary range names, GKE can create ranges itself (not in Shared VPC). Newer versions place ClusterIP Services in a GKE-managed range by default.

### Clusters with Shared VPC

In Shared VPC the host project's network admin creates the subnet and secondary ranges in advance; the service project creates the cluster referencing them by full path, and the GKE service agent needs `compute.networkUser` on the subnet and `container.hostServiceAgentUser` on the host project (see 2.1).

```bash
gcloud container clusters create shared-cluster \
  --project=service-project --region=us-central1 \
  --network=projects/host-project/global/networks/shared-vpc \
  --subnetwork=projects/host-project/regions/us-central1/subnetworks/gke-subnet \
  --cluster-secondary-range-name=pods \
  --services-secondary-range-name=services \
  --enable-ip-alias
```

### Private clusters, private control plane endpoints and authorized networks

```bash
# Private nodes, control plane reachable only on its internal endpoint,
# with an allow list for the internal endpoint
gcloud container clusters create private-cluster \
  --region=us-central1 --network=production-vpc --subnetwork=gke-subnet \
  --enable-ip-alias --enable-private-nodes --enable-private-endpoint \
  --enable-master-authorized-networks \
  --master-authorized-networks=10.0.100.0/24
```

- **Private nodes** need **Cloud NAT** for internet egress (image pulls from outside Google, external APIs) and Private Google Access for Google APIs and Artifact Registry.
- **Authorized networks** restrict which CIDRs can reach IP-based endpoints. With an internal endpoint, sources in other regions need global access to the endpoint enabled, and on-premises sources need routing to it.
- Nodes always reach the control plane; authorized networks control administrators and tools.

### DNS-based endpoint for control plane access

```bash
gcloud container clusters update prod-cluster --region=us-central1 \
  --enable-dns-access
# kubectl then uses the cluster's FQDN; access is checked by IAM
```

The DNS-based endpoint is reachable from anywhere that can reach Google APIs, with access controlled by IAM (and optionally VPC Service Controls), so you can turn off or restrict IP-based endpoints without building jump hosts.

### Enabling GKE Dataplane V2

Dataplane V2 is the **eBPF**-based datapath built on **Cilium**. It replaces kube-proxy for Services, has **Kubernetes NetworkPolicy always on**, and supports **network policy logging**. It can be enabled **only when creating a cluster** (it is the default for new Autopilot clusters).

```bash
gcloud container clusters create dpv2-cluster --region=us-central1 \
  --enable-dataplane-v2 --enable-ip-alias
```

### SNAT and IP masquerade policies

By default GKE masquerades (SNATs) Pod traffic to the node IP for destinations outside a set of **non-masquerade** ranges; the defaults include RFC 1918 and other reserved private ranges, so Pod-to-Pod and Pod-to-VPC traffic keeps the Pod IP. Configure it with the **ip-masq-agent** ConfigMap (Standard) or an **EgressNATPolicy** (Autopilot).

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ip-masq-agent
  namespace: kube-system
data:
  config: |
    nonMasqueradeCIDRs:
      - 10.0.0.0/8
      - 100.64.0.0/10      # keep Pod IPs toward this PUPI/shared range
    masqLinkLocal: false
    resyncInterval: 60s
```

Why it matters: if on-premises firewalls only allow node ranges, masquerade the on-premises destination; if you use PUPI or non-RFC 1918 Pod ranges, add them to `nonMasqueradeCIDRs` so Pod-to-Pod traffic is not SNATed. Pod traffic to the internet keeps a private source, so it still needs Cloud NAT.

### Creating GKE network policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-frontend
  namespace: shop
spec:
  podSelector:
    matchLabels: {app: api}
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels: {app: frontend}
      ports:
        - protocol: TCP
          port: 8080
```

Network policies are namespaced and additive; once a Pod is selected by any policy for a direction, everything not allowed is denied. On Dataplane V2 they are always enforced; on the legacy dataplane you enable network policy enforcement on the cluster. They govern Pod-to-Pod traffic inside the cluster, while VPC firewall rules and Cloud NGFW govern traffic at the VM/node level.

### Configuring Pod ranges and Service ranges

- Max Pods per node sets the per-node Pod slice: the netmask is `31 - ceil(log2(max Pods))`, so 110 gives `/24`, 64 gives `/25`, 32 gives `/26`.
- The Service range is fixed at creation (or GKE-managed); size it for the number of ClusterIP Services.
- Node subnet primary ranges can be expanded with `expand-ip-range`.

### Deploying additional Pod ranges

When the Pod range is exhausted, add more secondary ranges to the subnet and attach them with **discontiguous multi-Pod CIDR**:

```bash
# Add a secondary range to the subnet (host project in Shared VPC)
gcloud compute networks subnets update gke-subnet --region=us-central1 \
  --add-secondary-ranges=pods-2=10.40.0.0/16

# Cluster level: available to future node pools
gcloud container clusters update prod-cluster --region=us-central1 \
  --additional-pod-ipv4-ranges=pods-2

# Node pool level: this pool uses its own range (immutable afterwards)
gcloud container node-pools create pool-2 --cluster=prod-cluster \
  --region=us-central1 --pod-ipv4-range=pods-2 --max-pods-per-node=64
```

GKE updates its own `gke-<cluster>-<hash>-all` firewall rule to include new Pod ranges, but your own firewall rules, ip-masq-agent config and on-premises filters must be updated by hand.

### Configuring DNS: kube-dns, Cloud DNS and NodeLocal DNSCache

| Option | How it works | When |
|--------|--------------|------|
| **kube-dns** | In-cluster DNS Deployment | Legacy default on Standard |
| **Cloud DNS for GKE** | Cloud DNS serves cluster records; no in-cluster DNS Pods to scale | Default on new clusters in recent versions; **cluster scope** (in-cluster only), **VPC scope** (resolvable across the VPC, Standard only, disruptive migration), **additive VPC scope** (cluster scope plus VPC-wide) |
| **NodeLocal DNSCache** | DaemonSet cache on each node; forwards misses to kube-dns or Cloud DNS | Reduce latency and conntrack load; on by default in Autopilot |

```bash
gcloud container clusters update prod-cluster --region=us-central1 \
  --cluster-dns=clouddns --cluster-dns-scope=cluster
gcloud container clusters update prod-cluster --region=us-central1 \
  --update-addons=NodeLocalDNS=ENABLED
```

VPC scope (or additive VPC scope) is what lets VMs or on-premises clients resolve headless Services directly. Manual edits to the managed private zones are not supported. Publishing Service and Ingress hostnames into your own public or private zones is a separate job for **ExternalDNS** (covered in [Section 3.3](03-managed-network-services.md#33-configuring-cloud-dns)).

---

## Exam traps

- Static routes **cannot** be equal to or more specific than a subnet route; **policy-based routes** are evaluated before subnet routes.
- Peering needs **both sides**, is **non-transitive**, never exchanges tag-scoped static routes or the default internet route, and needs explicit flags for custom routes and PUPI subnet routes.
- In Shared VPC, **service agents** (Google APIs and GKE) need `compute.networkUser`; GKE also needs `container.hostServiceAgentUser`.
- `restricted.googleapis.com` = `199.36.153.4/30`; it only serves VPC Service Controls-supported APIs.
- Subnet expansion is one-way and online; secondary ranges are not expanded, they are added.
- Regional dynamic routing confines learned routes to one region; global adds inter-region cost.
- An internal passthrough NLB next hop keeps sending traffic even if every backend is unhealthy.
- NCC: topology fixed at hub creation; star edge spokes cannot reach each other; different spokes need different ASNs; Private NAT is TCP/UDP and outbound-initiated only.
- Dataplane V2 only at cluster creation; network policy always on with it.
- Private nodes need Cloud NAT for internet and Private Google Access for Google APIs.

## Key terms

- **Proxy-only subnet** - Subnet with purpose REGIONAL_MANAGED_PROXY or GLOBAL_MANAGED_PROXY that supplies source IPs for Envoy-based load balancers.
- **Private Google Access** - Per-subnet setting that lets VMs with only internal IPs reach Google APIs over Google's network.
- **restricted.googleapis.com** - VIP range 199.36.153.4/30 that serves only APIs supported by VPC Service Controls.
- **private.googleapis.com** - VIP range 199.36.153.8/30 that serves most Google APIs privately.
- **Service attachment** - Producer-side PSC resource that publishes an internal load balancer through a NAT subnet with a consumer accept list.
- **Service perimeter** - VPC Service Controls boundary around projects that blocks restricted API access and data copy across the boundary.
- **Dynamic routing mode** - VPC setting (regional or global) that decides whether Cloud Router installs learned routes in one region or all regions.
- **Policy-based route** - Route matching source, destination and protocol that is evaluated before other routes and forwards to an internal passthrough NLB.
- **Custom route export/import** - Peering flags that share static and dynamic routes between peered VPC networks.
- **Star topology** - NCC preset with center and edge spoke groups where edge spokes reach only center spokes.
- **PSC connection propagation** - NCC feature that makes a PSC endpoint in one VPC spoke reachable from other VPC spokes.
- **Private NAT** - Cloud NAT type that source-translates traffic from overlapping subnets toward NCC spokes or hybrid networks.
- **GKE Dataplane V2** - eBPF and Cilium based GKE datapath with always-on NetworkPolicy, enabled only at cluster creation.
- **ip-masq-agent** - GKE component whose nonMasqueradeCIDRs list decides which destinations see the Pod IP instead of the node IP.
- **Discontiguous multi-Pod CIDR** - GKE feature that adds extra Pod secondary ranges at cluster or node pool level when the first range runs out.

## Vendor documentation

- **[📖 Create and manage VPC networks](https://cloud.google.com/vpc/docs/create-modify-vpc-networks)** - networks, subnets, expansion
- **[📖 Subnets](https://docs.cloud.google.com/vpc/docs/subnets)** - purposes, stack types, reserved addresses
- **[📖 VPC Network Peering](https://cloud.google.com/vpc/docs/vpc-peering)** - route exchange and restrictions
- **[📖 Shared VPC](https://docs.cloud.google.com/vpc/docs/shared-vpc)** - roles and administration
- **[📖 Set up clusters with Shared VPC](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-shared-vpc)** - GKE service agent permissions
- **[📖 Private services access](https://cloud.google.com/vpc/docs/private-services-access)** - service networking peering
- **[📖 Configure Private Google Access](https://docs.cloud.google.com/vpc/docs/configure-private-google-access)** - VIP ranges, routes and DNS
- **[📖 Private Service Connect](https://docs.cloud.google.com/vpc/docs/private-service-connect)** - endpoints, backends, interfaces, service attachments
- **[📖 VPC Service Controls overview](https://cloud.google.com/vpc-service-controls/docs/overview)** - perimeters, access levels, dry run
- **[📖 Routes](https://docs.cloud.google.com/vpc/docs/routes)** - route types and selection order
- **[📖 Policy-based routes](https://docs.cloud.google.com/vpc/docs/policy-based-routes)** - match criteria and limits
- **[📖 Internal passthrough NLB as next hop](https://docs.cloud.google.com/load-balancing/docs/internal/ilb-next-hop-overview)** - appliance HA routing
- **[📖 NCC overview](https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview)** - spokes and hubs
- **[📖 NCC connectivity topologies](https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/connectivity-topologies)** - mesh and star
- **[📖 Private NAT](https://docs.cloud.google.com/nat/docs/private-nat)** - NAT for NCC spokes and hybrid networks
- **[📖 PSC connection propagation](https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/psc-propagated-connection-overview)** - sharing endpoints through NCC
- **[📖 GKE Dataplane V2](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/dataplane-v2)** - eBPF datapath
- **[📖 IP masquerade agent](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/ip-masquerade-agent)** - SNAT behavior
- **[📖 Discontiguous multi-Pod CIDR](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-pod-cidr)** - additional Pod ranges
- **[📖 Cloud DNS for GKE](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/cloud-dns)** - scopes and NodeLocal DNSCache

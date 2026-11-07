---
last-updated: 2026-11-07
---

# VPC Explained

> **6-minute read.**

## The one-line answer

A VPC (Virtual Private Cloud) is a private, isolated network you carve out inside a cloud provider's infrastructure. It's how you control what can talk to what.

## Why this exists

If every VM you launched was just "on the internet," you'd have:

- No firewall control beyond what each VM does individually
- No private connection between your servers (e.g., web → DB)
- No way to bring on-prem networks into the cloud cleanly
- No enforcement of "this database is internal only"

VPCs give you a configurable, software-defined network with the same primitives you'd build in a corporate datacenter: subnets, route tables, gateways, firewalls.

## The mental model

Picture an empty office building you rent inside a cloud provider's headquarters:

- [**VPC**](../glossary.md#term-vpc-virtual-private-cloud) = the floor you rented. Has its own address (a CIDR block like `10.0.0.0/16`).
- **Subnets** = rooms on that floor. Each subnet is in one AZ, with its own smaller CIDR (`10.0.1.0/24`).
- **Route tables** = the floorplan that says where doors lead.
- **Internet gateway** = the front door to the public internet.
- **NAT gateway** = a way for inside-only rooms to reach the internet without being reachable from it.
- **Security groups** = locks on each VM's door.
- **Network ACLs** = security desk for each room (subnet-level rules).

## Public vs private subnets

The most important VPC concept:

- **Public subnet** - has a route to an internet gateway. Resources can have public IPs and be reached from the internet.
- **Private subnet** - no route to an internet gateway. Resources here can't be reached from the internet directly.

Typical pattern: web servers in public subnet, DB servers in private subnet. The DB never exposes itself.

```mermaid
flowchart LR
  I[Internet] <--> IGW[Internet Gateway]
  IGW <--> WEB[Public subnet<br/>web servers]
  WEB --> NAT[NAT Gateway]
  WEB <--> DB[Private subnet<br/>databases]
  NAT --> IGW
```

Inbound traffic stops at the IGW unless explicitly routed to a public subnet. Private subnets reach out via the NAT for things like package updates without ever being inbound-reachable.

```
                        Internet
                            |
                    [Internet Gateway]
                            |
       +-------- Public Subnet (10.0.1.0/24) --------+
       |    [Web server]    [Load balancer]          |
       +----------------------------------------------+
                            |
       +------- Private Subnet (10.0.2.0/24) --------+
       |    [App server]    [Database]               |
       +----------------------------------------------+
                            |
                    [NAT Gateway] --- (outbound only)
```

## CIDR blocks (the address math)

A CIDR block like `10.0.0.0/16` defines how big the network is. The number after the slash is how many bits are "fixed":

- `/16` → 65,536 addresses (e.g., `10.0.0.0` to `10.0.255.255`)
- `/24` → 256 addresses (e.g., `10.0.1.0` to `10.0.1.255`)
- `/28` → 16 addresses

A VPC is usually `/16`. You carve subnets out of it as `/24` or smaller.

Use **private IP ranges** (RFC 1918):
- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

## Security groups vs network ACLs

Both are firewalls. The difference:

| | Security Group | Network ACL |
|---|---|---|
| Scope | Per-VM (or per-resource) | Per-subnet |
| Stateful? | Yes (replies allowed automatically) | No (must allow both directions) |
| Default | Deny all inbound, allow all outbound | Allow all both directions |
| Rules | Allow only | Allow + Deny |
| When to use | Always | Rarely - only for subnet-level blanket rules |

Day to day: configure security groups. NACLs are the rarely-used outer layer.

## Connecting things

Common VPC connectivity patterns:

- [**VPC peering**](../glossary.md#term-vpc-peering) - direct connection between two VPCs (same or different accounts)
- **Transit Gateway** - hub for connecting many VPCs (and on-prem) together
- [**VPN**](../glossary.md#term-vpn-virtual-private-network) - encrypted tunnel from on-prem to VPC over the internet
- **Direct Connect (AWS) / ExpressRoute (Azure) / Interconnect (GCP)** - dedicated fiber from your office/datacenter to the cloud
- **VPC endpoints / Private Link** - reach AWS services (S3, DynamoDB, etc.) without traversing the public internet

## A small concrete example

A typical 3-tier web app VPC:

```
VPC: my-app-prod (10.0.0.0/16) in us-east-1
├── Public subnet 10.0.1.0/24  (us-east-1a) → ALB, NAT GW
├── Public subnet 10.0.2.0/24  (us-east-1b) → ALB, NAT GW
├── App subnet    10.0.10.0/24 (us-east-1a) → ECS tasks
├── App subnet    10.0.11.0/24 (us-east-1b) → ECS tasks
├── DB subnet     10.0.20.0/24 (us-east-1a) → RDS primary
└── DB subnet     10.0.21.0/24 (us-east-1b) → RDS standby
```

Why this layout:
- Multi-AZ for resilience
- Public subnets for load balancers (need internet)
- App subnets private (only reached via ALB)
- DB subnets private (only reached from app subnets)
- Security groups: ALB → App, App → DB, deny everything else

## Equivalents across clouds

| Concept | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Virtual network | VPC | Virtual Network (VNet) | VPC |
| Subnet | Subnet | Subnet | Subnet |
| Per-resource firewall | Security group | NSG (Network Security Group) | Firewall rule (per-network) |
| Internet egress | Internet gateway | (default outbound) | Cloud NAT / Internet gateway |

GCP VPCs are global by default (subnets are regional). AWS and Azure VPCs are regional.

## What to look at next

- **[Regions and availability zones](./regions-and-availability-zones.md)** - subnets live in AZs
- **[CDN explained](./cdn-explained.md)** - how user traffic actually reaches your VPC
- **[Glossary: VPC, Subnet, Security Group, NAT Gateway](../glossary.md#networking)**
- **[Networking deep dives](../../resources/networking-deep-dives/)** - hybrid connectivity, multi-cloud patterns

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. What makes a subnet public rather than private?

    <details>
    <summary>Answer</summary>
    A public subnet has a route to an internet gateway. A private subnet has no such route and cannot be reached from the internet directly. See: <a href="#public-vs-private-subnets">Public vs private subnets</a>
    </details>

2. How does a resource in a private subnet get package updates?

    <details>
    <summary>Answer</summary>
    Through a NAT gateway, which allows outbound access without making the resource inbound-reachable. See: <a href="#public-vs-private-subnets">Public vs private subnets</a>
    </details>

3. How many addresses does a `/24` CIDR block contain, and what is it typically used for?

    <details>
    <summary>Answer</summary>
    256 addresses. A VPC is usually a <code>/16</code> and subnets are carved out of it as <code>/24</code> or smaller. See: <a href="#cidr-blocks-the-address-math">CIDR blocks (the address math)</a>
    </details>

4. Security group or network ACL: which is stateful, and which is per-subnet?

    <details>
    <summary>Answer</summary>
    Security groups are stateful and per-resource. Network ACLs are per-subnet and not stateful, so both directions must be allowed. See: <a href="#security-groups-vs-network-acls">Security groups vs network ACLs</a>
    </details>

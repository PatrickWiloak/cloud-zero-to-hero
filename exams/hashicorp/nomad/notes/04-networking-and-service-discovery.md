# Networking and Service Discovery

Nomad tasks need network access and ways to find each other. This domain covers network modes, port allocation, service registration (Consul or native), health checks, and service mesh via Consul Connect.

## Network Stanza

Networking is configured at the group level (one namespace shared by all tasks in the group):

```hcl
group "web" {
  network {
    mode = "bridge"
    port "http" {
      to     = 8080         # container port
      static = 80           # host port (optional)
    }
    port "metrics" {
      to = 9100
    }
  }
}
```

## Network Modes

- **`host`:** task shares the client's network namespace. Uses host's IP and ports. High performance; no isolation.
- **`bridge`:** Nomad creates a separate namespace with its own virtual interface. NAT between the task and the host. Default for many scenarios.
- **`none`:** no network; task runs in isolation.
- **CNI plugins:** for advanced networking (Calico, Cilium, etc.). Configure via plugins.

```hcl
network {
  mode = "bridge"    # or "host", "none", or a CNI plugin name
}
```

## Static vs Dynamic Ports

Dynamic:

```hcl
port "http" {
  to = 8080
}
```

Nomad chooses a host port (typically from 20000-32000 range) and maps it to container port 8080. Different allocations get different host ports.

Static:

```hcl
port "http" {
  to     = 8080
  static = 80
}
```

Host port 80 is fixed. Only one allocation per node can use it. Conflicts prevent scheduling.

## Accessing Port Info from Tasks

Nomad injects runtime variables:

- `NOMAD_IP_http`: the host IP for the `http` port
- `NOMAD_PORT_http`: the host port assigned
- `NOMAD_ADDR_http`: `IP:PORT` combined
- `NOMAD_HOST_PORT_http`: explicit host port
- `NOMAD_HOST_IP_http`: explicit host IP
- `NOMAD_PORT_<label>` for container-side: the `to` value

Applications use these to bind to the correct interface/port.

## Service Block

Register the task's service with a registry (Consul or Nomad native):

```hcl
service {
  name     = "api"
  port     = "http"
  tags     = ["v1", "production"]
  provider = "consul"    # default; or "nomad"

  check {
    type     = "http"
    path     = "/health"
    interval = "10s"
    timeout  = "2s"
  }
}
```

Attributes:

- `name`: service name for discovery
- `port`: label from the network block
- `tags`: arbitrary strings for filtering
- `provider`: `consul` (default) or `nomad`
- `address_mode`: `auto`, `driver`, `host`

## Service Providers

### Consul Provider (default)

- Requires Consul agent running on the Nomad client
- Services register in Consul's catalog
- DNS and HTTP discovery via Consul
- Full health-check integration
- Supports Consul Connect service mesh

### Nomad Native Provider (1.3+)

- No Consul required
- Services register in Nomad's built-in catalog
- Discovery via `nomad service list` and DNS API
- Lighter; good for small deployments
- Does not support Consul Connect

```hcl
service {
  name     = "api"
  provider = "nomad"
}
```

Query:

```
nomad service list
nomad service info api
```

## Health Checks

Supported check types:

- **http:** HTTP GET, expect 2xx status
- **tcp:** TCP connect
- **grpc:** gRPC health check protocol
- **script:** run a script inside the task
- **docker:** Docker healthcheck (for Docker driver)

```hcl
check {
  name     = "api-healthy"
  type     = "http"
  path     = "/health"
  interval = "10s"
  timeout  = "2s"
  method   = "GET"

  header {
    Authorization = ["Bearer token"]
  }

  check_restart {
    limit = 3
    grace = "30s"
    ignore_warnings = false
  }
}
```

`check_restart` restarts the task if checks fail repeatedly.

## Consul Integration Config

On the Nomad client:

```hcl
consul {
  address = "127.0.0.1:8500"
  token   = "consul-token"
}
```

Nomad expects a Consul agent on each client. The agent handles check execution, catalog registration, and DNS.

## Consul Connect (Service Mesh)

Sidecar proxies (Envoy) provide mTLS and L7 features without app changes.

```hcl
group "frontend" {
  network {
    mode = "bridge"
    port "http" { to = 8080 }
  }

  service {
    name = "frontend"
    port = "http"
    connect {
      sidecar_service {
        proxy {
          upstreams {
            destination_name = "api"
            local_bind_port  = 9000
          }
        }
      }
    }
  }

  task "app" {
    driver = "docker"
    config { image = "frontend:v1" }
    env {
      API_URL = "http://localhost:9000"
    }
  }
}
```

The `connect` stanza:

- Runs an Envoy sidecar in the same group
- Registers the service in Consul
- Configures upstreams (other services to reach)

The app talks to `localhost:9000` which Envoy forwards through the mesh.

### Intentions

Consul intentions authorize service-to-service traffic:

```
consul intention create frontend api
```

Without intentions, service mesh traffic is denied by default.

## Ingress Gateway

Expose services outside the mesh via Consul's ingress gateway:

```hcl
service {
  name = "ingress"
  connect {
    gateway {
      ingress {
        listener {
          port     = 8080
          protocol = "http"
          service {
            name  = "frontend"
            hosts = ["frontend.example.com"]
          }
        }
      }
    }
  }
}
```

Alternative: use Traefik or another reverse proxy with Consul catalog as its backend.

## Terminating Gateway

Connect mesh to external services (databases outside mesh, third-party APIs):

```hcl
connect {
  gateway {
    terminating {
      service { name = "external-db" }
    }
  }
}
```

## DNS Service Discovery

With Consul: `api.service.consul` resolves to all healthy `api` service instances.

With Nomad native: `api.service.nomad` resolves similarly via Nomad's DNS plugin.

Applications can use DNS without app changes for basic discovery.

## CNI Plugins

For advanced networking:

```hcl
network {
  mode = "cni/mynetwork"
}
```

Where `mynetwork` is a CNI config in `/opt/cni/config`. Supports BGP (Calico), eBPF (Cilium), etc.

## Network Namespaces and Isolation

Bridge mode creates per-group network namespaces. Tasks within a group share the namespace; tasks in different groups have separate namespaces. Useful for:

- Per-group network policies
- Isolated port spaces
- Sidecar communication via localhost

## Example: Two-Service Mesh Job

```hcl
job "mesh-demo" {
  datacenters = ["dc1"]

  group "backend" {
    network { mode = "bridge" }

    service {
      name = "backend"
      port = "8080"
      connect { sidecar_service {} }
    }

    task "api" {
      driver = "docker"
      config { image = "myapp/backend:v1" }
    }
  }

  group "frontend" {
    network {
      mode = "bridge"
      port "http" { static = 80; to = 8080 }
    }

    service {
      name = "frontend"
      port = "http"
      connect {
        sidecar_service {
          proxy {
            upstreams {
              destination_name = "backend"
              local_bind_port  = 9000
            }
          }
        }
      }
    }

    task "web" {
      driver = "docker"
      config { image = "myapp/frontend:v1" }
      env { BACKEND_URL = "http://localhost:9000" }
    }
  }
}
```

Don't forget the Consul intention:

```
consul intention create frontend backend
```

## Network Monitoring

Metrics exposed via telemetry:

- `nomad.client.allocs.cpu.*`
- `nomad.client.allocs.memory.*`
- `nomad.client.host.*`

Envoy sidecars also emit their own metrics. Scrape with Prometheus.

## Common Pitfalls

- Forgetting `network { mode = "bridge" }` when using Consul Connect (required)
- Static port conflicts across allocations on the same node
- Missing Consul intentions causing service mesh denial
- Wrong `port` label reference in `service { port = "http" }` vs the task's network stanza
- Using `provider = "nomad"` then trying to use Consul Connect (doesn't work)

## Exam-Ready Checklist

- [ ] Know network modes: host, bridge, none, CNI
- [ ] Can use static and dynamic port allocation
- [ ] Know NOMAD_PORT_<label> and related env vars
- [ ] Understand service providers (consul vs nomad)
- [ ] Can write Consul Connect sidecar config
- [ ] Know health check types
- [ ] Understand DNS discovery via Consul or Nomad

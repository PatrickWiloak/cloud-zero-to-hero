---
last-updated: 2026-11-07
---

# DNS Explained

> **5-minute read.**

## The one-line answer

DNS (Domain Name System) is the internet's phonebook. It turns human-readable names like `example.com` into the numeric IP addresses (`93.184.216.34`) that computers actually route to.

## Why this exists

Computers route to IPs, not names. But IPs are:
- Hard to remember
- Hard to change (your server moves IPs and now everyone's bookmarks break)
- Provider-specific (the IP behind `gmail.com` changes constantly)

DNS adds a layer of indirection. You publish "the IP for `gmail.com` is X." Browsers look it up at request time. You can change X without anyone noticing.

## How a lookup works

When you type `example.com`:

```mermaid
sequenceDiagram
  participant B as Browser
  participant OS as OS resolver
  participant R as Recursive resolver<br/>(1.1.1.1, 8.8.8.8)
  participant Root as Root servers (.)
  participant TLD as .com TLD servers
  participant Auth as example.com<br/>authoritative
  B->>OS: example.com?
  alt OS cache hit
    OS-->>B: cached IP
  else OS cache miss
    OS->>R: example.com?
    alt Resolver cache hit
      R-->>OS: cached IP
    else Resolver cache miss
      R->>Root: example.com?
      Root-->>R: ask .com TLD at...
      R->>TLD: example.com?
      TLD-->>R: ask example.com NS at...
      R->>Auth: example.com?
      Auth-->>R: A 93.184.216.34
      R-->>OS: 93.184.216.34
    end
    OS-->>B: 93.184.216.34
  end
  B->>B: Connect to 93.184.216.34
```

This whole dance often takes <50ms because of aggressive caching at every layer.

## Record types you'll meet

| Record | What it means |
|--------|---------------|
| **A** | "name → IPv4 address" |
| **AAAA** | "name → IPv6 address" |
| **CNAME** | "this name is an alias for another name" |
| **MX** | "email for this domain goes to..." |
| **TXT** | Arbitrary text. Used for SPF, DKIM, domain verification |
| **NS** | "this zone's authoritative servers are..." |
| **SOA** | Zone metadata (serial, refresh interval, etc.) |
| **CAA** | Which certificate authorities can issue certs for this domain |
| **SRV** | Service location (host + port). Used by SIP, XMPP, etc. |
| **PTR** | Reverse lookup (IP → name) |

For 95% of work: A, AAAA, CNAME, MX, TXT, NS.

## A small concrete example

You bought `myapp.com`. To put it online:

1. **Set the nameservers** at the registrar (where you bought the domain) to your DNS provider (Route 53, Cloudflare, etc.).
2. **Add records:**
   ```
   A     myapp.com           34.120.X.X      (your load balancer)
   A     www.myapp.com       34.120.X.X      (or CNAME to myapp.com)
   MX    myapp.com           10 mail.example. (your email provider)
   TXT   myapp.com           "v=spf1 include:_spf.example.com ~all"
   ```
3. Wait for caches to expire (TTL minutes to hours).
4. Browser typing `myapp.com` now hits your load balancer.

## TTL - the cache duration

Every DNS record has a TTL (Time To Live). It's how long resolvers cache the answer before asking again. Common values:

- `300` (5 min) - changes propagate quickly. Good before changes.
- `3600` (1 hour) - balance.
- `86400` (24 hours) - fewer lookups, slow propagation.

Strategy: **lower the TTL before changes**, deploy the change, raise it back when stable.

## Apex vs subdomain

The "apex" or "root" domain is `example.com` itself. Subdomains are `www.example.com`, `api.example.com`, etc.

CNAME records are **not allowed at the apex** by spec (the root needs SOA/NS records). Workarounds:

- **A record at the apex** pointing directly at IPs (works but breaks if the target's IP changes)
- **ALIAS / ANAME records** (Route 53 alias, Cloudflare CNAME flattening) - DNS provider hides the CNAME-at-apex limitation

This trips people up constantly. If your DNS provider supports apex aliases, use them.

## The cloud DNS providers

| Provider | Best for |
|----------|----------|
| **Cloudflare DNS** | Free, fast, includes DDoS + WAF if you proxy. Default for most |
| **AWS Route 53** | Tight AWS integration, alias records to ELB/CloudFront/S3 |
| **Azure DNS** | Tight Azure integration |
| **Google Cloud DNS** | Tight GCP integration |
| **NS1 / DNSimple** | Premium, advanced traffic management |

For most projects: Cloudflare. Fast, free, sane defaults, generous proxying.

## Common gotchas

### Caching is everywhere
Your laptop, your router, your ISP, the resolver - all cache. After a change, "it's not working" might just be cached old data. `dig +trace` to bypass caches.

### TTL only kicks in after the next refresh
Lowering TTL doesn't retroactively shorten cached records. Lower TTL **before** the change, by at least the old TTL.

### DNS != HTTP
DNS resolves a name to an IP. The IP still has to serve content. "DNS is wrong" is sometimes "DNS is right and the server is broken."

### Email DNS is its own beast
SPF, DKIM, DMARC, MX records, plus rDNS for reputation. If you send email from your domain, expect to spend an hour learning these.

### `nslookup` lies sometimes
Use `dig` instead. `dig` is more accurate and gives more detail.

## Quick CLI reference

```bash
dig example.com                    # A record
dig example.com AAAA               # IPv6
dig example.com MX                 # mail servers
dig example.com TXT                # text records
dig +trace example.com             # full resolution path
dig @1.1.1.1 example.com           # query specific resolver
dig +short example.com             # just the answer

host example.com                   # quick lookup
whois example.com                  # registrar info
```

## What to look at next

- **[CDN explained](./cdn-explained.md)** - CDNs typically need DNS records pointed at them
- **[TLS and HTTPS](https://security.noblerworks.com/learn/concepts/tls-and-https/)** - TLS depends on the CN/SAN matching the DNS name
- **[Glossary: DNS, A record, CNAME, TTL](../glossary.md#networking)**
- **[Networking deep dives: DNS](../../resources/networking-deep-dives/dns-deep-dive.md)**

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. What are the first two places that are checked for an answer when a browser looks up a name?

   <details markdown="1">
   <summary>Answer</summary>

   The OS cache and then the recursive resolver's cache. Only if both miss does the resolver ask the root, TLD and authoritative servers. See: [How a lookup works](#how-a-lookup-works)

   </details>

2. Why must you lower a record's TTL before a planned change instead of after?

   <details markdown="1">
   <summary>Answer</summary>

   Lowering the TTL does not shorten records that are already cached. Lower it at least the old TTL before the change. See: [Common gotchas](#common-gotchas)

   </details>

3. Why can a CNAME not be used at the apex, and what is a workaround?

   <details markdown="1">
   <summary>Answer</summary>

   The apex needs SOA and NS records. Workarounds are an A record at the apex or an ALIAS/ANAME record such as a Route 53 alias or Cloudflare CNAME flattening. See: [Apex vs subdomain](#apex-vs-subdomain)

   </details>

4. What does an MX record say?

   <details markdown="1">
   <summary>Answer</summary>

   That email for this domain goes to the named mail server. See: [Record types you'll meet](#record-types-youll-meet)

   </details>

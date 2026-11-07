---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 6 min
---

# Managed Databases Explained

> **6-minute read.** This is the cloud-builder's short version. For choosing a database model, consistency and data engineering in depth, read **[SQL vs NoSQL](https://data.noblerworks.com/learn/concepts/sql-vs-nosql/)** and the **[database service comparison](https://data.noblerworks.com/resources/service-comparison-databases/)** on Data Zero to Hero.

## The one-line answer

A managed database is a database the cloud provider runs for you. You choose the engine and size and get a connection string; the provider handles installation, patching, backups, replication and failover. You still own the schema, the queries, the data and who can reach it.

## What "managed" takes off your plate

Running PostgreSQL yourself on a VM means you are on the hook for:

- Installing and upgrading the engine and the OS
- Configuring backups, and proving restores work
- Setting up a replica and writing failover scripts
- Monitoring disk space before it fills at 3am
- Encryption, certificates and security patches

A managed service turns most of that into settings. Turn on automated backups with point-in-time restore. Tick "multi-AZ" or "high availability" and get a synchronous standby with automatic failover. Choose a maintenance window for patches.

The trade: less control (no root on the host, limited extensions and parameters), a higher price per unit of compute than a bare VM, and some lock-in to the provider's flavour. For almost every team, the time saved is worth far more than the markup.

## The main families

| Type | AWS | Azure | GCP |
|---|---|---|---|
| Relational (MySQL, PostgreSQL, SQL Server) | RDS | Azure Database for MySQL / PostgreSQL, Azure SQL | Cloud SQL |
| Cloud-native relational | Aurora, Aurora DSQL | Azure SQL Hyperscale | AlloyDB, Spanner |
| Key-value / document | DynamoDB, DocumentDB | Cosmos DB | Firestore, Bigtable |
| In-memory cache | ElastiCache, MemoryDB | Azure Managed Redis | Memorystore |

Rough guide: start with managed PostgreSQL or MySQL unless you have a clear reason not to. Reach for a key-value or document store when access patterns are simple and scale is huge, and for a globally distributed database when users write from several continents.

## Serverless vs provisioned

**Provisioned** means you pick an instance size and pay for it every hour, busy or idle. **Serverless** options (Aurora Serverless v2, DynamoDB on-demand, Azure SQL serverless, Firestore) scale capacity with load and bill for what is used, some down to near zero when idle. Serverless suits spiky or unpredictable workloads and dev environments; steady high load is usually cheaper provisioned.

## What you still own

- **Network exposure.** Put the database in private subnets and allow only the app's security group. A publicly reachable database is one of the most common breaches.
- **Access.** Use IAM or Entra authentication where supported, and keep passwords in a secrets manager with rotation.
- **Schema, indexes and queries.** The provider will not fix a missing index.
- **Connection limits.** Serverless functions and autoscaled apps can open thousands of connections. Use a pooler (RDS Proxy, PgBouncer, built-in poolers).
- **Testing restores** and choosing retention.
- **Major version upgrades**, which usually need planning and testing even when the provider runs them.

## Common mistakes

- **Read replicas mistaken for high availability.** Replicas spread read load; a Multi-AZ or HA standby is what gives automatic failover. Some engines (Aurora) blur the line by promoting replicas.
- **Single-AZ in production** to save money.
- **Public accessibility turned on** "just to connect from my laptop".
- **No connection pooling** in front of a fleet of functions.
- **Ignoring storage autoscaling limits**, so the disk fills anyway.

## How exams test it

- "Reduce operational overhead of a self-managed MySQL on EC2" -> migrate to RDS or Aurora.
- "Automatic failover if the AZ fails" -> Multi-AZ, not read replicas.
- "Offload read-heavy reporting" -> read replicas.
- "Millisecond latency at any scale, simple key access" -> DynamoDB, Cosmos DB, Bigtable or Firestore.
- "Globally consistent relational database across regions" -> Spanner (or Aurora DSQL / Cosmos DB depending on the cloud and model).

## Go deeper

- **[SQL vs NoSQL](https://data.noblerworks.com/learn/concepts/sql-vs-nosql/)** - choosing the data model (Data Zero to Hero)
- **[Eventual consistency](https://data.noblerworks.com/learn/concepts/eventual-consistency/)** - why replicas can return stale reads (Data Zero to Hero)
- **[📖 What is Amazon RDS?](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)** - managed relational databases on AWS
- **[📖 What is Azure SQL Database?](https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview)** - Azure's PaaS SQL engine
- **[📖 Cloud SQL overview](https://cloud.google.com/sql/docs/introduction)** - managed MySQL, PostgreSQL and SQL Server on Google Cloud

## What to look at next

- **[High availability and fault tolerance](./high-availability-and-fault-tolerance.md)** - why the database is usually the hardest tier to make redundant
- **[Caching explained](./caching-explained.md)** - taking load off the database
- **[Object, block, and file storage](./object-block-file-storage.md)** - the storage underneath

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. What does the provider handle for a managed database, and what do you still own?

   <details markdown="1">
   <summary>Answer</summary>

   The provider handles installation, patching, backups, replication and failover. You still own the schema, the queries, the data and who can reach it. See: [The one-line answer](#the-one-line-answer)

   </details>

2. Which gives automatic failover if an AZ fails, a read replica or a Multi-AZ standby?

   <details markdown="1">
   <summary>Answer</summary>

   The Multi-AZ or HA standby. Read replicas spread read load and are not the same as high availability. See: [Common mistakes](#common-mistakes)

   </details>

3. Why might a fleet of serverless functions need a connection pooler?

   <details markdown="1">
   <summary>Answer</summary>

   Serverless functions and autoscaled apps can open thousands of connections, so a pooler such as RDS Proxy or PgBouncer is needed. See: [What you still own](#what-you-still-own)

   </details>

4. Which is usually cheaper for steady high load, provisioned or serverless?

   <details markdown="1">
   <summary>Answer</summary>

   Provisioned. Serverless suits spiky or unpredictable workloads and dev environments. See: [Serverless vs provisioned](#serverless-vs-provisioned)

   </details>

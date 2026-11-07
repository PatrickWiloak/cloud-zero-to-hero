---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 8 min
---

# eBPF Explained

> **8-minute read. Assumes you've read [Containers vs VMs](./containers-vs-vms.md) and [Kubernetes in 10 minutes](./kubernetes-in-10-minutes.md).**

## The one-line answer

eBPF lets you run small, checked programs inside the Linux kernel without changing the kernel or loading a kernel module. Cloud tools use it to see and control network traffic, system calls and security events at very low cost, which is why you meet it in Kubernetes networking, observability and runtime security.

## Why the kernel matters

Every container on a host shares one Linux kernel. Every network packet, file open and process start passes through it. That makes the kernel the one place that sees everything, but it was always hard to extend. Changing the kernel source takes years to reach users; a kernel module can crash the whole machine.

eBPF is the third option. The project's own definition: "eBPF is a revolutionary technology with origins in the Linux kernel that can run sandboxed programs in a privileged context." Programs are loaded at runtime and extend what the kernel does.

**[📖 What is eBPF?](https://ebpf.io/what-is-ebpf/)** - the eBPF project's introduction

## How it works

```mermaid
flowchart LR
  Src[Program in C-like code] --> Byte[Compiled to eBPF bytecode]
  Byte --> Load[Loaded with the bpf system call]
  Load --> Ver[Verifier checks safety]
  Ver --> Jit[JIT compiler to machine code]
  Jit --> Hook[Attached to a hook]
  Hook --> Maps[Maps share data with user space]
```

A program is written, compiled, checked by the verifier, then attached to an event; data flows back to user space through maps.

From the eBPF project's description:

- **Hooks.** Programs are event-driven. They run when a hook point is reached: system calls, function entry and exit, kernel tracepoints and network events. Kprobes and uprobes can attach to almost any kernel or user-space location.
- **Verifier.** Before a program runs, the verifier checks that it will not crash or harm the system, that it always terminates, and that it stays within size and complexity limits.
- **JIT compiler.** The bytecode is translated to machine instructions so it runs at speeds comparable to native kernel code.
- **Maps.** Programs share data through maps and call approved kernel helper functions.

The verifier checks that a program is safe to run, not that it does something sensible. A safe program can still be a bad idea.

## What people use it for

| Area | What eBPF gives you | Examples named by the eBPF project |
|---|---|---|
| **Networking** | Fast packet handling and load balancing without iptables chains | Cilium |
| **Observability** | Fine-grained data on applications and the kernel with low overhead, with no code change in the app | bpftrace, bcc |
| **Security** | See and block suspicious behaviour in applications and container runtimes | Security tools built on the same hooks |

Cilium, bcc and bpftrace are higher-level tools on top of eBPF. Libraries such as libbpf, the eBPF Go library, aya and libbpf-rs load and manage programs.

In Kubernetes, this is why "Cilium replaces kube-proxy" and "sidecar-free service mesh" appear in conversations (the eBPF page lists a talk titled "Liberating Kubernetes from kube-proxy and iptables"; it does not state the sidecar-free claim, which is a vendor claim not checked here): the work a sidecar proxy does per pod can sometimes be done once per node in the kernel. See [Service mesh explained](./service-mesh-explained.md).

## What it is not

- **Not a product you install and forget.** It is a mechanism; you get its benefits through tools.
- **Not available everywhere.** It needs a Linux kernel with eBPF support and enough privilege to load programs. Managed services that hide the node (some serverless container platforms) may not let you run it. Check the provider's docs before you plan around it.
- **Not free of risk.** Loading programs needs high privilege, so who can load them is a security decision.

## Common mistakes

- Assuming eBPF is a Kubernetes feature. It is Linux; Kubernetes tools happen to use it.
- Expecting it on Windows nodes or on a managed platform without checking.
- Treating "low overhead" as "no overhead". Very busy hooks still cost CPU.

## How exams test it

Cloud certs rarely test eBPF directly. It shows up in Kubernetes and platform material (CNCF-aligned exams) as the technology behind modern CNI plugins, and in security questions about runtime monitoring. If an option says "kernel-level visibility without modifying application code", that is the eBPF idea.

## Go deeper

- **[📖 What is eBPF?](https://ebpf.io/what-is-ebpf/)** - concepts, verifier, JIT, hooks, projects

## What to look at next

- **[Service mesh explained](./service-mesh-explained.md)** - where eBPF changes the sidecar story
- **[Observability basics](./observability-basics.md)** - what you do with the data
- **[Kubernetes in 10 minutes](./kubernetes-in-10-minutes.md)** - the platform most eBPF tools run on

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. What does eBPF let you do, in one sentence?

   <details markdown="1">
   <summary>Answer</summary>

   It lets you run small, checked programs inside the Linux kernel without changing the kernel or loading a kernel module. See: [The one-line answer](#the-one-line-answer)

   </details>

2. What does the verifier do, and what does it not do?

   <details markdown="1">
   <summary>Answer</summary>

   It checks that a program will not crash or harm the system, that it always terminates and that it stays within size limits. It does not check that the program does something sensible. See: [How it works](#how-it-works)

   </details>

3. Why does the page say eBPF may not be available on some managed platforms?

   <details markdown="1">
   <summary>Answer</summary>

   It needs a Linux kernel with eBPF support and enough privilege to load programs. Managed services that hide the node may not allow it. See: [What it is not](#what-it-is-not)

   </details>

4. Why is it a mistake to call eBPF a Kubernetes feature?

   <details markdown="1">
   <summary>Answer</summary>

   It is a Linux technology. Kubernetes tools happen to use it. See: [Common mistakes](#common-mistakes)

   </details>

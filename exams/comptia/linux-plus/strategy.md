---
last-updated: 2026-11-07
---

# CompTIA Linux+ (XK0-006) Study Strategy

## Study Approach

### The shape of the exam

One exam, up to 90 questions in 90 minutes, a mix of multiple choice and performance-based questions (PBQs). That is about one minute per question, so PBQs, which take several minutes each, must be managed deliberately. The passing score is 720 on a 100-900 scale.

### Weighting your time

| Domain | Weight | Suggested share of study time |
|--------|--------|-------------------------------|
| 1.0 System Management | 23% | 25% |
| 5.0 Troubleshooting | 22% | 20% (it reuses the other four, so it improves as they do) |
| 2.0 Services and User Management | 20% | 20% |
| 3.0 Security | 18% | 18% |
| 4.0 Automation, Orchestration, and Scripting | 17% | 17% |

### Phases

1. **Foundation (weeks 1-3).** Domain 1 and the file, account and process parts of Domain 2. Everything else leans on these.
2. **Services and security (weeks 4-5).** systemd, packages, containers, then firewalls, sudo, SELinux and SSH.
3. **Automation (week 6).** Read playbooks, scripts and Git commands until you can predict their behavior. This domain is mostly reading comprehension of short snippets.
4. **Troubleshooting and review (weeks 7-8).** Domain 5, then practice questions across all domains, then a final pass over the weak spots.

## Handling PBQs

- Expect a simulated terminal or a configuration task: fix a broken `fstab` line, extend a logical volume, set a firewall rule, repair a script, or order the steps of a procedure.
- **Flag them and come back.** Answer the multiple-choice questions first, then spend the remaining time on PBQs.
- Read the whole task before typing. Note the end state they ask for (persistent versus runtime, enabled versus started).
- Reach for the tool the objectives name. If the objectives list `firewall-cmd`, `lvextend` or `visudo`, that is the tool the simulation expects.
- If a simulated command line is not available, expect a pick-the-command or arrange-the-steps format.

## Multiple-choice technique

- Look for the **persistence** word: "permanently," "after reboot," "survives a restart." It separates `--permanent`, `enable`, `fstab`, `-P` and `/etc/sysctl.d` answers from their runtime twins.
- Look for the **layer** the symptom lives in before choosing a command: hardware, filesystem, network, service, security policy.
- Eliminate the dangerous answer when two options both work: disabling SELinux, `chmod 777`, running as root, using Telnet or deleting logs to free space are rarely correct.
- Distinguish look-alike tools: `modprobe` and `insmod`, `fetch` and `pull`, `kill` and `kill -9`, `su -` and `sudo -i`, `ENTRYPOINT` and `CMD`.

## Study Resources

- [Notes](README.md#notes-study-order) - the five domain notes
- [Fact Sheet](fact-sheet.md) - verified facts and quick-reference tables
- [Practice Questions](../../../resources/practice-questions/comptia-linux-plus-xk0-006.md) - 20 original questions
- **[📖 CompTIA Linux+ XK0-006 Exam Objectives (PDF, version 5.0)](https://lecbyo.files.cmp.optimizely.com/download/90b9ac985c0e11f0b004a2a93c999a21)** - The checklist: every tool named under an objective is fair game
- **[📖 CompTIA Linux+ Certification](https://www.comptia.org/en-us/certifications/linux/)** - Current exam details; re-check before booking

## Test day

CompTIA's objectives document says the example lists are not exhaustive, so a tool you have not seen may appear. When it does, use the command's name and the objective's verb ("manage," "troubleshoot") to reason out what it does, then eliminate options that cannot be right.

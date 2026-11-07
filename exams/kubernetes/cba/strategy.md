---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 4 min
---

# CBA Study Strategy

## Follow the weights

| Domain | Weight | Share of study time |
|---|---:|---|
| Backstage Development Workflow | 24% | Build and run locally, TypeScript, Yarn, Docker image |
| Backstage Infrastructure | 22% | Framework, configuration, production deployment, client-server |
| Backstage Catalog | 22% | Entities, annotations, locations, ingestion, troubleshooting |
| Customizing Backstage | 32% | Frontend and backend plugins, React, Material UI |

## Read the YAML and the folder

Many questions hand you a snippet of `app-config.yaml`, a `catalog-info.yaml` or a directory path and ask what happens. Practice naming, for each one, which process reads it (frontend, backend, catalog) and when.

## Distinctions to own

- **Frontend versus backend plugin**, and which package each installs into.
- **Provider versus processor** in the catalog.
- **Location versus entity**: a location points to entity files.
- **Static config locations** (cannot be removed through the API) versus UI-registered ones.
- **`catalog.rules` replaces the defaults**, it does not add to them.
- **Config visibility**: backend-only by default.
- **Host build versus multi-stage build** for the image.
- **New versus legacy frontend system.**

## Do not over-study

CBA is a knowledge exam. You do not need to be a React expert. You need to know where things live, what they are named and how they behave.

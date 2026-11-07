---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 10 min
---

# 01 - Backstage Development Workflow

**Domain 1: Backstage Development Workflow (24%)**

Curriculum topics: build and run Backstage projects locally; understand local development workflows; compile a Backstage project with TypeScript; download and install dependencies with NPM/Yarn; use Docker to build a container image of a Backstage project.

All commands in this note are quoted from the Backstage docs and were **not run**: creating an app downloads a large dependency tree and the docs call for at least 20 GB of disk and 6 GB of memory.

---

## What you are building

Backstage describes itself as an open source framework for building developer portals, and the docs state it is "a CNCF Incubation project after graduating from Sandbox." The point to hold on to is **framework, not product**: `create-app` gives you a TypeScript monorepo that you own, customize, build and deploy.

**[📖 What is Backstage?](https://backstage.io/docs/overview/what-is-backstage/)** - the overview and core features

---

## Prerequisites

From the getting-started guide:

| Tool | Requirement |
|---|---|
| Node.js | Active LTS; the guide says "Node 22 or 24 are recommended" |
| Yarn | Enable Corepack, then pin the version; "Backstage currently uses Yarn 4.4.1" |
| Docker | Required |
| Git | Required |
| Machine | At least 20 GB disk and 6 GB memory, Linux, macOS or WSL, a GNU-style build environment, `curl` or `wget` |
| Network | Ports 3000 and 7007 must be reachable if the host is not directly accessible |

```bash
corepack enable
yarn set version 4.4.1
```

**[📖 Getting started](https://backstage.io/docs/getting-started/)** - prerequisites, create-app, first run

---

## Creating and running an app

```bash
npx @backstage/create-app@latest
cd my-backstage-app
yarn start
```

The wizard asks for an app name and creates a subdirectory in the current directory. `yarn start` "will run both the frontend and backend as separate processes (named `[0]` and `[1]`) in the same window." When the output shows `Rspack compiled successfully`, open `http://localhost:3000`.

Ports to memorize: **3000** is the frontend dev server, **7007** is the backend (it is also the port the production container publishes).

### The layout you get

```text
app
├── app-config.yaml
├── catalog-info.yaml
├── package.json
└── packages
    ├── app
    └── backend
```

| Path | Purpose |
|---|---|
| `app-config.yaml` | The main configuration file |
| `catalog-info.yaml` | Catalog entity descriptors |
| `package.json` | Root manifest; the guide warns not to add npm dependencies here |
| `packages/` | Yarn workspaces; each directory is a separate package |
| `packages/app` | "A fully functioning Backstage frontend app" |
| `packages/backend` | Powers features such as authentication, the catalog, software templates and TechDocs |

Plugins you create with `yarn new` live under `plugins/<pluginId>` (note 04).

---

## Local development workflow

A normal inner loop looks like this:

1. Edit code or `app-config.yaml`.
2. Run `yarn start` from the repo root for the whole app, or `yarn start` inside a single plugin directory to serve that plugin alone. The docs say isolated serving gives faster startup and hot reloads and is for local development only.
3. Use `app-config.local.yaml` for personal overrides. Backstage loads `app-config.yaml` and then `app-config.local.yaml`, and local files win (full order in note 02).
4. Validate configuration with `yarn backstage-cli config:check` (note 02).

Why `yarn start` runs two processes: the frontend is a client-side application and the backend is a separate server. Locally they sit on ports 3000 and 7007; in the production image the Docker page has you open `http://localhost:7007` after `docker run`, so the app is reached through the backend's port (note 02).

---

## Compiling with TypeScript and installing dependencies

Backstage apps are TypeScript. The docs' container build uses these commands from the repo root:

```bash
yarn install --immutable   # install dependencies exactly as locked
yarn tsc                   # generate type definitions to dist-types/
yarn build:backend         # bundle the backend into packages/backend/dist
```

Reading them:

- `yarn install --immutable` fails if `yarn.lock` would change, so CI installs exactly what was reviewed.
- `yarn tsc` runs the TypeScript compiler across the workspaces and writes type definitions to `dist-types/`.
- `yarn build:backend` produces the backend bundle (`packages/backend/dist`).

Run these with the same Node version as the Docker base image. The docs name `node:24-trixie-slim`.

**[📖 Docker deployment](https://backstage.io/docs/deployment/docker/)** - host build and multi-stage build

---

## Building a container image with Docker

The docs recommend the **host build**: build on the machine (or CI runner), then copy artifacts into a small image.

```bash
yarn install --immutable
yarn tsc
yarn build:backend
docker image build . -f packages/backend/Dockerfile --tag backstage
docker run -it -p 7007:7007 backstage
```

Details from the page:

- The Dockerfile is `packages/backend/Dockerfile`. It starts from `node:24-trixie-slim`, installs `libsqlite3-dev`, runs as the non-root `node` user in `/app`, unpacks `skeleton.tar.gz`, installs production dependencies with `yarn workspaces focus --all --production`, copies `bundle.tar.gz` and `app-config*.yaml`, and sets `NODE_ENV=production`.
- Build from the **repo root**, because the build needs the root `yarn.lock` and `package.json`.
- The container starts with `node packages/backend --config app-config.yaml --config app-config.production.yaml`.
- The Dockerfile has no `EXPOSE`; the port is mapped at run time with `-p 7007:7007`.

**Multi-stage build** is the alternative for when Docker-in-Docker is unavailable or the build must run entirely in Docker. It has three stages: `packages` (collect `package.json` files for dependency caching), `build` (install, `yarn tsc`, `yarn --cwd packages/backend build`) and `final` (production install and the same command). It replaces `.dockerignore` with a multi-stage version, and the docs say it does not work inside the main Backstage repo.

Troubleshooting flags: `--progress=plain` for verbose logs, `--no-cache` for a full rebuild.

---

## Key terms

- **Backstage** - an open source framework for building developer portals, a CNCF Incubation project.
- **create-app** - the `@backstage/create-app` package that scaffolds a new Backstage monorepo.
- **Corepack** - the Node tool that provisions the pinned Yarn version.
- **Yarn workspaces** - the monorepo mechanism where each directory under `packages/` is a separate package.
- **`packages/app`** - the frontend package of a Backstage app.
- **`packages/backend`** - the backend package, the unit of deployment.
- **app-config.yaml** - the main configuration file, shared by frontend and backend.
- **Host build** - building the backend on the host, then copying the bundle into a small Docker image.
- **Multi-stage build** - a Dockerfile that builds inside Docker in separate stages.
- **dist-types** - the directory where `yarn tsc` writes generated type definitions.

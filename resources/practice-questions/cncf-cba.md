# Certified Backstage Associate (CBA) - Practice Questions

31 original questions for CBA prep, spread across the domains in proportion to their weights.

> **Cert page:** [exams/kubernetes/cba/](../../exams/kubernetes/cba/)

---

### Question 1
**Scenario:** Which runtime and package manager versions does the Backstage getting-started guide recommend?

A. Node 14 with npm 6 and a global Yarn 1 install
B. Any Node version with Bun, since Backstage ignores the runtime and does not check the engines field
C. Python 3.12 with pip, because the backend is Python-based
D. Node 22 or 24 (Active LTS) with Yarn 4.4.1 enabled through Corepack

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The guide recommends Node 22 or 24 and says Backstage currently uses Yarn 4.4.1, enabled with Corepack.
</details>

---

### Question 2
**Scenario:** After running yarn start in a new app, which URL serves the frontend?

A. http://localhost:7007/frontend
B. http://localhost:8080
C. http://localhost:3000
D. http://localhost:443

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** yarn start runs the frontend and backend as separate processes. The frontend dev server is on port 3000 and the backend is on 7007.
</details>

---

### Question 3
**Scenario:** Which directory of a freshly created Backstage app holds the frontend app?

A. packages/backend
B. packages/app
C. plugins/app
D. src/frontend

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** packages/app is the fully functioning frontend app. packages/backend holds the backend.
</details>

---

### Question 4
**Scenario:** The docs warn against adding npm dependencies in one place of a new Backstage repo. Where?

A. packages/app/package.json
B. The root package.json
C. packages/backend/package.json
D. Any plugin package.json

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The getting-started guide says not to add npm dependencies to the root manifest; dependencies belong to the individual workspace packages.
</details>

---

### Question 5
**Scenario:** Which command installs dependencies exactly as locked and fails if the lockfile would change?

A. yarn install --immutable
B. yarn upgrade --latest
C. npm install --force
D. yarn add --exact

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** yarn install --immutable is the first step of the documented container build and keeps CI aligned with the reviewed lockfile.
</details>

---

### Question 6
**Scenario:** Which command generates TypeScript type definitions into dist-types/ as part of the documented host build?

A. yarn build:backend
B. yarn new
C. yarn start
D. yarn tsc

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The host build runs yarn install --immutable, yarn tsc (type definitions to dist-types), then yarn build:backend.
</details>

---

### Question 7
**Scenario:** What is the recommended way to build the Backstage container image, according to the Docker deployment page?

A. Run yarn start inside a container and expose port 3000
B. Clone the Backstage repo into the image and run npm install at start-up
C. Host build: build the backend on the host, then docker image build with packages/backend/Dockerfile
D. Download a prebuilt image and mount app-config.yaml

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The page recommends the host build. The multi-stage build is the alternative for when Docker-in-Docker is unavailable.
</details>

---

### Question 8
**Scenario:** From which directory should docker image build be run for the Backstage image, and why?

A. packages/backend, because the Dockerfile is there and the build context is its parent folder
B. packages/app, because the frontend is bundled first
C. The repo root, because the build needs the root yarn.lock and package.json
D. Any directory; Docker finds the files automatically

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The command is docker image build . -f packages/backend/Dockerfile --tag backstage, run from the repo root.
</details>

---

### Question 9
**Scenario:** Which port does the Backstage container publish when you run it per the docs?

A. 3000, because the frontend is served from the container
B. 7007, mapped with -p 7007:7007
C. 5432, because the database is embedded
D. 80, set by an EXPOSE instruction in the Dockerfile

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The backend listens on 7007 and the Dockerfile has no EXPOSE instruction, so the port is mapped at docker run.
</details>

---

### Question 10
**Scenario:** Which database does the architecture page prefer for production?

A. PostgreSQL
B. SQLite, because it is embedded
C. Redis, because it is fast
D. MongoDB, because entities are documents

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** SQLite is mainly for in-memory testing. PostgreSQL is preferred for production. Backstage uses Knex and a separate logical database per plugin.
</details>

---

### Question 11
**Scenario:** Which of the following is a core feature (core plugin) of Backstage?

A. Terraform state storage
B. Kubernetes cluster provisioning
C. Container image registry
D. Software Catalog

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The architecture overview lists the Software Catalog, Software Templates, TechDocs, Kubernetes and Search as core features.
</details>

---

### Question 12
**Scenario:** Which config file is the only one required?

A. app-config.local.yaml
B. app-config.production.yaml
C. app-config.override.yaml
D. app-config.yaml

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Only the base app-config.yaml is required. The local and environment files are optional.
</details>

---

### Question 13
**Scenario:** A value is set in both app-config.yaml and app-config.local.yaml. Which wins?

A. The value in app-config.yaml, because it is the base file and local files only add new keys
B. Neither; Backstage refuses to start
C. The value in app-config.local.yaml, because local files load last
D. Whichever file has the later modification time

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** All non-local files load before local files, so local settings win.
</details>

---

### Question 14
**Scenario:** A secret must not be committed. Which config include reads it from an environment variable?

A. $file: MY_SECRET_KEY
B. $env: MY_SECRET_KEY
C. ${MY_SECRET_KEY} inside a quoted string
D. $secret: MY_SECRET_KEY

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** $env reads a string value from an environment variable. $file reads the contents of a text file. The Backstage docs on configuration show these two includes.
</details>

---

### Question 15
**Scenario:** What is the default visibility of configuration values?

A. Backend-only
B. Visible to the frontend
C. Visible only to administrators
D. Visible to plugins but not the backend

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Config is backend-only by default; a custom visibility keyword in a schema controls what reaches the frontend.
</details>

---

### Question 16
**Scenario:** Which command validates configuration against plugin-contributed schemas?

A. yarn backstage-cli config:check
B. yarn tsc --noEmit
C. yarn new --validate
D. yarn backstage-cli plugin:verify

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Schemas are JSON Schema, contributed by plugins and combined; config:check validates them, and config:docs prints the reference.
</details>

---

### Question 17
**Scenario:** According to the Docker page, which statement about authentication in containerized deployments is correct?

A. Guest authentication is required for containers
B. Authentication is disabled automatically when NODE_ENV=production is set in the container
C. Containers must use SQLite-backed sessions
D. The default Guest auth provider is not intended for containerized environments

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The page lists an auth provider and a Postgres database as prerequisites and warns about the default Guest provider.
</details>

---

### Question 18
**Scenario:** Which apiVersion do Backstage entity kinds such as Component use?

A. backstage.io/v2
B. catalog.backstage.io/v1
C. backstage.io/v1alpha1
D. apps/v1

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** For Backstage kinds the apiVersion is backstage.io/v1alpha1; Template uses backstage.io/v1beta2.
</details>

---

### Question 19
**Scenario:** Which spec fields are required on a Component?

A. name, namespace and title
B. type, lifecycle and owner
C. system, domain and owner
D. providesApis and consumesApis

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A Component requires type, lifecycle and owner. system, subcomponentOf, providesApis, consumesApis and dependsOn are optional.
</details>

---

### Question 20
**Scenario:** What does the annotation backstage.io/techdocs-ref point to?

A. The URL of the deployed TechDocs site, which the entity page links to from its Docs tab
B. Where the TechDocs source lives, usually a path relative to catalog-info.yaml
C. The Docker image that builds the docs
D. The owner of the documentation

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** It tells Backstage where the TechDocs source is, normally a relative path, though it can be an absolute URL.
</details>

---

### Question 21
**Scenario:** Who should write the annotation backstage.io/managed-by-location?

A. Nobody; the catalog adds it automatically
B. The entity owner, in every descriptor
C. The platform team, via a Template
D. The GitHub integration, via a webhook

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** managed-by-location is added automatically and records where the entity was fetched from. backstage.io/orphan is likewise set by the catalog, never manually.
</details>

---

### Question 22
**Scenario:** Which default entity kinds does the catalog allow before catalog.rules is set?

A. All kinds
B. Component only
C. Component, Template and Group
D. Component, API and Location

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** By default only Component, API and Location are allowed. Setting catalog.rules replaces those defaults.
</details>

---

### Question 23
**Scenario:** A team adds catalog.rules with allow: [Template] and finds their Components no longer ingest. Why?

A. Templates and Components cannot coexist in one catalog unless each kind has its own location
B. Components require a separate provider for each owner
C. Setting catalog.rules replaces the defaults, so Component was no longer listed
D. Rules apply only to file-type locations

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The docs say setting catalog.rules replaces the defaults, so any default kinds you still want must be listed.
</details>

---

### Question 24
**Scenario:** Which location type is meant only for local development, tests and example data?

A. url
B. github
C. file
D. git

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The file type is for local development, tests and example data; url is the type handled by the UrlReaderProcessor and used for repositories.
</details>

---

### Question 25
**Scenario:** What is the difference between an entity provider and a processor?

A. Processors supply entities and providers validate them
B. Providers supply entities from external sources; processors read, parse, transform and validate entity data
C. They are the same component configured in two places
D. Providers run in the browser and processors in the backend

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Providers supply raw entities and are configured under catalog.providerOptions. Processors validate and transform and are configured under catalog.processorOptions.
</details>

---

### Question 26
**Scenario:** An entity shows backstage.io/orphan: 'true'. What does it mean?

A. A parent stopped emitting it and nothing else references it; by default it is later deleted
B. The entity has no owner field
C. The entity failed schema validation
D. The entity was created by the UI and not by a file

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The stitcher adds the annotation when a parent stops emitting a child. The default orphanStrategy is delete; keep disables automatic cleanup.
</details>

---

### Question 27
**Scenario:** Which package provides automated discovery of catalog-info.yaml files in a GitHub organization?

A. @backstage/plugin-techdocs
B. @backstage/create-app
C. @backstage/theme
D. @backstage/plugin-catalog-backend-module-github

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Install it in packages/backend and add it with backend.add. It needs a GitHub integration with a PAT (repo scope) or GitHub App (Contents read-only).
</details>

---

### Question 28
**Scenario:** Which statement correctly places plugins in a Backstage repo?

A. Frontend plugins are added to the root package.json; backend plugins to the plugins/ directory of the repo workspace
B. Both kinds are added to packages/app
C. Backend plugins run in the browser through a service worker
D. Frontend UI plugins are added to the app package; backend plugins are added to the backend package

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The configure-app-with-plugins page states that frontend UI plugins go in the app package and backend plugins go in backend.
</details>

---

### Question 29
**Scenario:** In the new frontend system, which setting makes installed plugins get discovered without code changes?

A. backend.discovery: true
B. catalog.rules: all
C. app.packages: all in app-config.yaml
D. plugins.autoload: enabled

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** With app.packages set to all, plugins are discovered automatically and page plugins register their sidebar item.
</details>

---

### Question 30
**Scenario:** Which function creates a backend plugin in the new backend system?

A. createFrontendPlugin
B. createBackendPlugin
C. createServiceFactory only
D. registerPlugin

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** createBackendPlugin takes a pluginId and register(env), where env.registerInit declares deps and init.
</details>

---

### Question 31
**Scenario:** Which Material UI related function builds a Backstage theme from the base options and palettes?

A. createUnifiedTheme
B. createMuiTheme from App.tsx only
C. buildTheme
D. makeBackstageTheme

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The docs build themes with createUnifiedTheme({...createBaseThemeOptions({palette: palettes.light})}) from @backstage/theme, and register them in createApp themes with UnifiedThemeProvider.
</details>

---

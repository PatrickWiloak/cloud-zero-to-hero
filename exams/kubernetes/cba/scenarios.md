---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 6 min
---

# CBA High-Yield Scenarios

---

## Scenario 1: A catalog file registers but nothing shows up

**Scenario**: A team registers a `catalog-info.yaml` that defines a `Template`. The location registers without error, but the template never appears.

**Solution Pattern**:
- Check `catalog.rules`: by default only Component, API and Location are allowed
- Add the kind: `rules: - allow: [Component, API, Location, Template]` (setting rules replaces the defaults, so keep the ones you need)
- Check the entity status panel for processing errors

**Key Takeaway**: An allowed-kinds rule silently filters; remember rules replace defaults.

---

## Scenario 2: Entities keep disappearing and coming back

**Scenario**: An engineer deletes an entity from the UI, and it returns on the next refresh.

**Solution Pattern**:
- A parent `Location` still references it, so processing recreates it
- Remove or change the entry at the source (the repository file or the config)
- Look for the `backstage.io/orphan: 'true'` annotation to see if a parent stopped emitting it

**Key Takeaway**: Delete at the source, not in the UI.

---

## Scenario 3: The portal works locally but not in the container

**Scenario**: The app runs with `yarn start` but the container fails to sign users in and loses data on restart.

**Solution Pattern**:
- The default Guest auth provider is not intended for containers: set up a real auth provider
- Use PostgreSQL, not SQLite
- Load `app-config.production.yaml` (the container command uses two `--config` flags) and pass secrets through `$env`
- Publish port 7007 and set `backend.baseUrl` to the external URL

**Key Takeaway**: Production needs auth, a real database and production config.

---

## Scenario 4: Onboard every repository without registering each one

**Scenario**: Hundreds of repositories each carry a `catalog-info.yaml`. Registering them by hand is not an option.

**Solution Pattern**:
- Install `@backstage/plugin-catalog-backend-module-github`
- Add it with `backend.add(...)` and configure `catalog.providers.github` with organization, catalogPath, filters and schedule
- Provide a GitHub integration (PAT with `repo` scope, or a GitHub App with Contents read-only)

**Key Takeaway**: Entity providers pull on a schedule; locations are manual.

---

## Scenario 5: A value read in browser code is undefined

**Scenario**: A frontend plugin reads a setting from `app-config.yaml` and gets nothing.

**Solution Pattern**:
- Configuration is backend-only by default
- A schema with a `visibility` setting must expose the value to the frontend
- Run `yarn backstage-cli config:check` to validate

**Key Takeaway**: Visibility, not syntax, is the usual reason.

---

## Scenario 6: Add a third-party plugin

**Scenario**: The team wants the Tech Radar plugin in the portal.

**Solution Pattern**:
- `yarn --cwd packages/app add @backstage-community/plugin-tech-radar` (frontend plugins go in the app package)
- With the new frontend system and `app.packages: all`, it is discovered automatically; configure the path under `app.extensions` if needed
- A backend counterpart, if any, goes in `packages/backend`

**Key Takeaway**: Frontend in app, backend in backend, and the new system discovers plugins.

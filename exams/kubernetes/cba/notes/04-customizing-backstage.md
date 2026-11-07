---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 14 min
---

# 04 - Customizing Backstage

**Domain 4: Customizing Backstage (32%)**

Curriculum topics: understand frontend versus backend plugins; customizing Backstage plugins; make changes to React code in the Backstage App; using Material UI components.

The largest domain. YAML and TypeScript here are quoted or adapted from the docs and were **not run or compiled**; the TypeScript snippets are shown to be read, not copied blind.

> **Two frontend systems.** The Backstage docs describe a **new frontend system** (plugins are discovered and wired through extensions and blueprints) and a **legacy** one (routes and sidebar written by hand in `App.tsx` and `Root.tsx`). Several pages are marked legacy and point you to the new docs. Expect to recognize both. Check which one the exam targets.

---

## Frontend versus backend plugins

| | Frontend plugin | Backend plugin |
|---|---|---|
| Runs in | The browser, inside the app | The Backstage backend process |
| Package location | Added to `packages/app` | Added to `packages/backend` |
| Typical job | Pages, cards, tabs, entity content | APIs, data fetching, integrations, scheduled work |
| Talks to others via | Extensions, Utility APIs and routes | Extension points and core services |
| Install command | `yarn --cwd packages/app add <package>` | `yarn --cwd packages/backend add <package>` |

The install guide says frontend UI plugins go in the `app` package and backend plugins go in `backend`.

Both sides keep plugins isolated. "There can be no direct communication between plugins through code," so a backend plugin is effectively its own microservice, and a frontend plugin calls its backend over an API.

**Backend modules** extend another plugin without forking it. A module attaches to an extension point of **one** plugin and must deploy with that plugin. The catalog is the classic case: a GitHub discovery module is a module of the catalog plugin.

**[📖 Architecture overview](https://backstage.io/docs/overview/architecture-overview/)** - plugin forms, libraries, modules

---

## Customizing plugins

### Creating one

`yarn new` is the scaffolder. Select `frontend-plugin`, `backend-plugin` or `backend-module` as appropriate.

- Frontend plugins land in `plugins/<pluginId>`. Backend plugins land in `plugins/<pluginId>-backend`, and modules in `plugins/<pluginId>-backend-module-<moduleId>`.
- Serve one plugin in isolation with `yarn start` inside its directory (faster startup and hot reload, for local development only). With the full app running, the default page is at `http://localhost:3000/my-plugin`.

### A frontend plugin (new frontend system)

```ts
import { createFrontendPlugin } from '@backstage/frontend-plugin-api';

export const examplePlugin = createFrontendPlugin({
  pluginId: 'example',
  extensions: [],
});
```

- The plugin ID is "a lowercase dash-separated string"; the exported instance is the camel-cased ID plus `Plugin`.
- `src/index.ts` default-exports the plugin so integrators can install it without referencing it in code.
- Extensions come from **blueprints**. `PageBlueprint` creates a standalone page; its `params` include `routeRef`, `path`, `title`, `icon` and a lazy `loader`. The title and icon populate the sidebar automatically.
- Route references use `createRouteRef()` and are passed to the plugin's `routes` so integrators can bind external links.
- Other blueprints in the docs: `ApiBlueprint` (Utility APIs) and `EntityContentBlueprint` (a tab on an entity page).

### Installing a frontend plugin

```bash
yarn --cwd packages/app add @backstage-community/plugin-tech-radar
```

With the new system, plugins are discovered automatically when `app.packages` is `all`:

```yaml
app:
  packages: all
```

Extension configuration can be set in `app-config.yaml`:

```yaml
app:
  extensions:
    - page:tech-radar:
        config:
          path: /tech-radar
```

Manual installation passes the plugin as a feature to `createApp` from `@backstage/frontend-defaults`:

```tsx
import { createApp } from '@backstage/frontend-defaults';
import techRadarPlugin from '@backstage-community/plugin-tech-radar/alpha';

const app = createApp({
  features: [techRadarPlugin],
});

export default app.createRoot();
```

In the new system, plugins that provide a page register their sidebar item automatically. To reorder, group or add entries you override the built-in `app/nav` extension.

### A backend plugin and a module

```ts
import {
  createBackendPlugin,
  coreServices,
} from '@backstage/backend-plugin-api';

export const examplePlugin = createBackendPlugin({
  pluginId: 'example',
  register(env) {
    env.registerInit({
      deps: {
        logger: coreServices.logger,
        httpRouter: coreServices.httpRouter,
      },
      async init({ logger, httpRouter }) {
        logger.info('Hello from example plugin');
        // httpRouter.use(router) mounts the plugin's routes
      },
    });
  },
});
```

- `createBackendPlugin` takes a `pluginId` and a `register(env)` function. Inside it, `env.registerInit` declares `deps` (core services or extension points) and an `init` function that receives them.
- `coreServices.logger` and `coreServices.httpRouter` are plugin-scoped: the logger may tag messages with the plugin ID.
- Read configuration by depending on `coreServices.rootConfig` and calling methods such as `config.getOptionalString('example.value')`.
- A module uses `createBackendModule` with the target `pluginId` and its own `moduleId`, and should depend on the target's library package (such as `@backstage/plugin-catalog-node`) and not on the plugin package.
- Module rules: each module package contains a single module; modules deploy in the same backend as the plugin they extend; register HTTP handlers under `/modules/<module-id>`.
- A plugin exposes its own extension point with `createExtensionPoint` and `env.registerExtensionPoint`.

The docs' backend page does not cover installing with `backend.add`; the catalog GitHub discovery docs (note 03) show the pattern: `backend.add(import('@backstage/plugin-catalog-backend-module-github'));`.

**[📖 Building frontend plugins](https://backstage.io/docs/frontend-system/building-plugins/index)** - createFrontendPlugin, blueprints

**[📖 Building backend plugins and modules](https://backstage.io/docs/backend-system/building-plugins-and-modules/index)** - createBackendPlugin, modules, extension points

**[📖 Configure your app with plugins](https://backstage.io/docs/getting-started/configure-app-with-plugins/)** - install and discovery

---

## React code in the Backstage app

The app package (`packages/app`) is an ordinary React and TypeScript application. Your changes go there:

- **Entry and wiring:** `packages/app/src/App.tsx` creates the app. In the new system that is `createApp` from `@backstage/frontend-defaults` with `features`; in the legacy system `createApp` from the app API takes `apis`, `components` and `themes`.
- **Themes:** register them in `createApp`. The docs warn that your list overrides the default themes, so provide both `light` and `dark`:

```tsx
const app = createApp({
  apis,
  components,
  themes: [
    {
      id: 'light',
      title: 'Light theme',
      variant: 'light',
      icon: <LightIcon />,
      Provider: ({ children }) => (
        <UnifiedThemeProvider theme={lightTheme} children={children} />
      ),
    },
    // dark theme entry follows the same shape
  ],
});
```

- **Plugin pages and routes:** in the legacy system these are `<Route>` elements in `App.tsx` and sidebar entries in `Root.tsx`; the docs mark that guide as legacy. In the new system, a plugin's `PageBlueprint` supplies both.
- **Entity pages:** extra tabs are contributed with `EntityContentBlueprint` in the new system.
- Per the architecture page, **extensions** are the building blocks of the app's visual and non-visual structure, arranged in an app extension tree; **extension overrides** are high-priority extensions that can replace existing ones; **routes** let plugins link to each other without knowing URL paths.

---

## Material UI components and theming

Backstage's UI is built on Material UI (MUI) and is moving toward Backstage UI (BUI). The customization page says both exist: the legacy system uses MUI with JS-based theming, and Backstage UI "uses CSS variables and tokens." Inspect a component's class names: a `bui-` prefix means you style it with BUI tokens.

### MUI theme with `createUnifiedTheme`

```ts
import {
  createBaseThemeOptions,
  createUnifiedTheme,
  palettes,
} from '@backstage/theme';

export const lightTheme = createUnifiedTheme({
  ...createBaseThemeOptions({
    palette: palettes.light,
  }),
  fontFamily: 'Comic Sans MS',
  defaultPageTheme: 'home',
});
```

- Override palette colors by spreading `palettes.light` and replacing keys such as `primary`, `secondary`, `background` and `navigation` (background, indicator, color, selectedColor).
- Typography is overridden inside `createBaseThemeOptions`; spread `defaultTypography` to change only some settings.
- Custom fonts are declared as `@font-face` entries under `components.MuiCssBaseline.styleOverrides`.
- Component overrides target Backstage components by name, for example `BackstageHeader` with `styleOverrides`.
- If MUI v5 class names are missing the `v5-` prefix, configure `ClassNameGenerator` before any MUI components load.

### Backstage UI tokens

Create a CSS file, import it in `App.tsx`, and target modes with `data-theme-mode`:

```css
[data-theme-mode='light'] {
  --bui-bg-app: #f8f8f8;
  --bui-fg-primary: #000;
}

[data-theme-mode='dark'] {
  --bui-bg-app: #333333;
  --bui-fg-primary: #fff;
}
```

Key tokens: `--bui-bg-app`, `--bui-bg-neutral-1`, `--bui-bg-solid`, `--bui-fg-primary`, `--bui-fg-solid`, `--bui-border-2`, `--bui-font-regular`, `--bui-space` (default `0.25rem`) and `--bui-radius-1` to `--bui-radius-6`. The `@backstage/plugin-mui-to-bui` plugin generates BUI variables from your MUI themes; the docs call its output best-effort, so review it.

**[📖 User interface customization](https://backstage.io/docs/conf/user-interface/)** - MUI themes, BUI tokens, overrides

---

## Key terms

- **Frontend plugin** - a package that adds UI features to the Backstage app.
- **Backend plugin** - a package that adds server-side features to the Backstage backend.
- **Backend module** - a package that extends a single plugin through its extension points.
- **Extension** - a building block of the app's visual or non-visual structure in the new frontend system.
- **Blueprint** - a helper such as `PageBlueprint` that creates an extension of a given kind.
- **Utility API** - an interface frontend plugins use to share functionality or let integrators customize behavior.
- **Route ref** - a handle for a page route that lets plugins link without hard-coded URLs.
- **Core service** - a backend utility such as the logger, HTTP router or root config.
- **registerInit** - the call where a backend plugin declares its dependencies and init function.
- **Material UI (MUI)** - the React component library behind Backstage's legacy UI and themes.
- **createUnifiedTheme** - the `@backstage/theme` function that builds a Backstage theme for MUI.
- **Backstage UI (BUI)** - the newer component system styled with CSS variables and tokens.

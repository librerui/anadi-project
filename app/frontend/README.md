# Frontend

This frontend is built with Vue 3, Vite, Pinia, PrimeVue and Axios. It provides the interactive dashboard for selecting PTDs, running predictions, and simulating charger installations.

## What the frontend does

- Loads PTD metadata from the backend
- Lets users select real PTDs by district and municipality
- Auto-populates model features from selected PTD data
- Runs predictions for classification and regression
- Displays model output, confidence, and probabilities
- Supports charger load simulation for feasibility checks

## Setup

From the `app` directory:

```sh
make frontend-install
```

Or from the frontend folder directly:

```sh
cd app/frontend
npm install
```

## Development

Start the frontend dev server from the app root:

```sh
make frontend-dev
```

Or directly:

```sh
cd app/frontend
npm run dev
```

The frontend expects the backend API at `http://localhost:8000/api/v1` by default. To override it, set `VITE_API_BASE_URL` in a `.env` file.

## Build

From the app root:

```sh
make frontend-build
```

Or from the frontend folder:

```sh
npm run build
```

## Type checking

From the app root:

```sh
make frontend-typecheck
```

Or directly in the frontend folder:

```sh
npm run type-check
```

## Recommended editor setup

- VS Code with [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar)
- Use the `vue-tsc` command for accurate Vue/TS diagnostics

## Troubleshooting

- If the UI can’t reach the API, check that the backend is running and accessible at `http://localhost:8000/api/v1`.
- If PTD options are missing, restart the backend and frontend so startup preload and API routes refresh.

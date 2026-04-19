# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## Linting & Formatting

This project uses [oxlint](https://oxc.rs/docs/guide/usage/linter) for linting and [oxfmt](https://oxc.rs/docs/guide/usage/formatter) for formatting.

```bash
# Lint
bun run lint
bun run lint:fix   # Auto-fix issues

# Format
bun run fmt
bun run fmt:check  # Check formatting
```

Configuration:
- `.oxlintrc.json` - Linter configuration
- `.oxfmtrc.json` - Formatter configuration

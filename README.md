# Oblivion Engine

A visual terminal application built with Electron that combines a real terminal emulator with clickable command panels, ASCII animations, and a built-in warning system for dangerous commands.

## What It Does

- **Command Panels** - Clickable buttons for common Git, Node.js, Python, and Docker commands so you don't have to memorize them
- **Live Terminal** - Full terminal emulator (xterm.js + node-pty) running your actual shell
- **Explanation Panel** - Hover over or click a command to see what it does before running it
- **ASCII Animations** - Animated visuals that react to command success/failure states
- **Warning System** - Catches dangerous commands (like `rm -rf`) and shows a confirmation overlay with risk level
- **Custom Commands** - Add your own commands through the built-in form

## Prerequisites

Before cloning, make sure you have the following installed:

| Tool | Minimum Version | Check With |
|------|----------------|------------|
| **Node.js** | v18+ | `node -v` |
| **npm** | v9+ | `npm -v` |
| **Git** | any | `git --version` |

### macOS

You need Xcode Command Line Tools for compiling the native `node-pty` module:

```bash
xcode-select --install
```

### Windows

You need a C++ build toolchain for compiling the native `node-pty` module:

1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. During installation, select the **"Desktop development with C++"** workload
3. Restart your terminal after installation

If you already have Visual Studio 2019 or newer with the C++ workload, you're all set.

### Linux (Debian/Ubuntu)

```bash
sudo apt install build-essential python3
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Positivitty/OblivionEngine.git
cd OblivionEngine
```

### 2. Install dependencies

```bash
npm install
```

This will also run `electron-rebuild` automatically (via the `postinstall` script) to compile `node-pty` for your version of Electron.

> **If `npm install` fails** with errors about `node-pty` or native modules, try:
> ```bash
> npm cache clean --force
> rm -rf node_modules package-lock.json
> npm install
> ```

### 3. Run the app

```bash
npm start
```

This launches the Electron app in development mode with DevTools open.

## Project Structure

```
OblivionEngine/
├── src/
│   ├── main/            # Electron main process
│   │   ├── index.ts     # App entry point, window creation
│   │   ├── shell-manager.ts    # PTY shell management
│   │   ├── warning-engine.ts   # Dangerous command detection
│   │   ├── config-manager.ts   # User config persistence
│   │   ├── project-detector.ts # Auto-detect project type
│   │   ├── ipc-handlers.ts     # Main ↔ Renderer communication
│   │   ├── logger.ts           # File-based logging
│   │   └── constants.ts        # Default config values
│   ├── preload/         # Secure bridge between main & renderer
│   │   └── index.ts
│   ├── renderer/        # UI (runs in browser context)
│   │   ├── index.ts            # Renderer entry, initialization
│   │   ├── terminal-renderer.ts # xterm.js terminal
│   │   ├── command-panel.ts    # Clickable command buttons
│   │   ├── explanation-panel.ts # Command descriptions
│   │   ├── animation-engine.ts # ASCII animation playback
│   │   ├── warning-overlay.ts  # Danger confirmation modal
│   │   ├── custom-command-form.ts # Add custom commands
│   │   ├── event-bus.ts        # Internal event system
│   │   ├── logger.ts           # Console logger
│   │   └── styles/             # CSS stylesheets
│   └── shared/          # Types & data shared across processes
│       ├── types.ts            # All TypeScript interfaces
│       ├── ipc-channels.ts     # IPC channel name constants
│       └── default-commands.ts # Built-in command definitions
├── assets/
│   └── animations/      # ASCII animation frame files (JSON)
│       ├── default/     # Default theme animations
│       └── minimal/     # Minimal theme animations
├── index.html           # Renderer HTML entry
├── forge.config.ts      # Electron Forge build config
├── vite.*.config.ts     # Vite build configs (main, preload, renderer)
├── tsconfig*.json       # TypeScript configs
└── package.json
```

## Available Scripts

| Command | What It Does |
|---------|-------------|
| `npm start` | Launch the app in development mode |
| `npm run package` | Package the app for your OS (no installer) |
| `npm run make` | Build a distributable installer for your OS |

## Tech Stack

- **Electron** - Desktop app framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Electron Forge** - Build, package, and distribute
- **xterm.js** - Terminal emulator in the browser
- **node-pty** - Native pseudo-terminal for real shell access
- **Catppuccin Mocha** - Dark color theme

## Troubleshooting

### `npm install` fails with node-pty errors

`node-pty` is a native module that needs to be compiled. Make sure you have the build tools for your OS installed (see Prerequisites above).

> **Windows users:** If you see `node-gyp failed to rebuild` errors, make sure Visual Studio Build Tools are installed with the "Desktop development with C++" workload, then delete `node_modules` and run `npm install` again.

### App launches but terminal is blank

The shell might have failed to spawn. Check the DevTools console (automatically opens in dev mode) for error messages. Common causes:
- Shell path not found - try setting a custom shell path in config
- Permissions issue on macOS - make sure Terminal has disk access in System Settings > Privacy

### `electron-rebuild` errors

If the postinstall rebuild fails:

```bash
npx electron-rebuild
```

If that still fails, delete `node_modules` and reinstall:

```bash
rm -rf node_modules
npm install
```

## License

MIT

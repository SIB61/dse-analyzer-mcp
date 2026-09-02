# UV Migration Guide

## Overview

This project has been migrated from `pip` + `requirements.txt` to **[UV](https://docs.astral.sh/uv/)** — a faster, more reliable Python package manager written in Rust.

## What Changed

### Before (pip)
```bash
pip install -r requirements.txt
```

### After (uv)
```bash
uv sync
```

## Files Added/Modified

| File | Status | Purpose |
|------|--------|---------|
| `pyproject.toml` | ✨ NEW | Project metadata + dependencies (UV standard) |
| `uv.lock` | ✨ NEW | Locked dependency versions (reproducible builds) |
| `.python-version` | ✨ NEW | Python version pin (3.12) |
| `requirements.txt` | 📦 KEPT | Still available for compatibility |
| `.venv/` | 📦 UPDATED | Now managed by UV |

## Installation & Setup

### Install UV (one-time)

```bash
# On macOS/Linux/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
irm https://astral.sh/uv/install.ps1 | iex
```

### Setup This Project

```bash
cd dse-analyst-mcp

# Sync dependencies
uv sync

# Run server
.venv/bin/python3 server_http.py --transport http --host 0.0.0.0 --port 7000
```

## Common UV Commands

```bash
# Sync dependencies (install/update)
uv sync

# Sync with refresh (clear cache)
uv sync --refresh

# Add a new dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Lock dependencies
uv lock

# Show dependency tree
uv tree

# Run command in venv
uv run python3 -m mymodule

# Start shell with venv
uv venv
source .venv/bin/activate
```

## Benefits Over pip

✅ **5-10x faster** — Written in Rust, optimized C code
✅ **Lock file** — `uv.lock` ensures reproducible builds across machines
✅ **Deterministic** — Same versions installed every time
✅ **No venv activation needed** — `.venv/` auto-managed
✅ **Better dependency resolution** — Handles complex dependency trees better
✅ **Modern tooling** — Supports `pyproject.toml` natively

## Dependency Constraints

```toml
dependencies = [
    "mcp>=1.0.0,<2.0.0",     # Pinned to v1.x (FastMCP API)
    "bdshare>=0.1.0",
    "pandas>=1.5.0",
    "numpy>=1.24.0",
    "uvicorn>=0.27.0",
]
```

**Important:** `mcp` is pinned to `<2.0.0` because version 2.x changed the API (FastMCP → MCPServer).

## Python Version

- **Required:** Python 3.12+
- **Set in:** `.python-version` (contains `3.12`)
- **Set in:** `pyproject.toml` (`requires-python = ">=3.12"`)

## Migration Notes

### For Developers

1. **First clone:** Run `uv sync` instead of `pip install -r requirements.txt`
2. **Add dependencies:** Use `uv add package-name` instead of pip
3. **Run scripts:** Use `.venv/bin/python3` (or `uv run python3`)
4. **Commit:** Both `pyproject.toml` and `uv.lock` should be committed

### For CI/CD

```bash
# Instead of:
# pip install -r requirements.txt

# Use:
uv sync
```

### Backward Compatibility

`requirements.txt` is still maintained for compatibility with older tools, but UV is the recommended method going forward.

## Project Configuration

```toml
[project]
name = "dse-analyst-mcp"
version = "0.1.0"
description = "DSE Analysis MCP Server — live Dhaka Stock Exchange data + technical analysis engine"
requires-python = ">=3.12"
dependencies = [
    "mcp>=1.0.0,<2.0.0",
    "bdshare>=0.1.0",
    "pandas>=1.5.0",
    "numpy>=1.24.0",
    "uvicorn>=0.27.0",
]

[project.scripts]
dse-analyst-mcp = "server_http:main"
```

## Troubleshooting

**"Command not found: uv"**
→ Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
→ Or add to PATH: `export PATH="$HOME/.local/bin:$PATH"`

**"Python version incompatible"**
→ Update Python: `uv python pin 3.12`

**"Dependency resolution failed"**
→ Clear cache: `uv sync --refresh`

**"Module not found"**
→ Ensure venv is active: `source .venv/bin/activate`
→ Or use: `.venv/bin/python3 script.py`

## Further Reading

- [UV Documentation](https://docs.astral.sh/uv/)
- [PEP 508 Dependency Specifications](https://peps.python.org/pep-0508/)
- [pyproject.toml Reference](https://packaging.python.org/en/latest/specifications/pyproject-toml/)

## Status

✅ **Migration Complete**
- Pyproject.toml configured
- UV lock file created
- Dependencies resolved
- Server tested and running

### Next Steps

1. Run `uv sync` on first setup
2. Use UV for dependency management
3. Commit `pyproject.toml` and `uv.lock`
4. Enjoy faster, more reliable builds! 🚀

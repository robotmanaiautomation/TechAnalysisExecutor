# Shared finance documentation

- `docs/` is a Git submodule of `myFinancesApi-docs`, shared by PortfolioManager,
  infoGetherAPI, and TechAnalysisExecutor.
- Edit shared documents only in the sibling `../myFinancesApi-docs/` repository,
  never directly inside this project's `docs/` checkout.
- Before work, from the common parent directory run
  `python3 myFinancesApi-docs/scripts/sync_workspace.py`.
  For stale copies, run the same command with `--sync --fetch`.
- After committing shared documents, run `--sync`, commit updated `docs` pointers
  in all three parent projects, push canonical docs first, then parent projects.
- On a new workstation, install the shared pre-push check using `--install-hooks`.
- Preserve dirty worktrees and divergent commits. Never reset or force-push them
  to make synchronization pass. See `../myFinancesApi-docs/README.md`.

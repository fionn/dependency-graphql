Repository Dependency Graphs
----------------------------

Creates dependency trees for GitHub repositories.

Generate a personal access token with `repo_scope` and export it as the environment variable `GITHUB_TOKEN`.

Install with `make install` or `make install_dev`.

Example usage: `dependency-graphql fionn/dependency-graphql`. This would return something like

```
fionn/dependency-graphql
└── requirements.txt
    ├── c0fec0de/anytree = 2.8.0
    │   └── ⋯
    └── psf/requests = 2.27.1
        └── ⋯
```

where the ellipsis implies sub-dependencies. Add `--recursion-depth x` to recurse `x` levels deep.

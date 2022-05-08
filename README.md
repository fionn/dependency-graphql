# Repository Dependency Graphs

Create dependency trees for GitHub repositories.

## Authentication

Generate a personal access token with `repo.public_repo` scope and export it as `GITHUB_TOKEN`.

## Installation

Install with `make install` or `make install_dev`.

## Usage

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

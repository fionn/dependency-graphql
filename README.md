Repository Dependency Graphs
----------------------------

Generates (shallow) dependency trees for GitHub repositories.

Generate a personal access token with `repo_scope` and make a `credentials.py` file with `TOKEN = your_token`.

Example usage: `./dependency_graphql.py iamfionn/dependency-graphql`. This would return

```
iamfionn/dependency-graphql
└── requirements.txt
    ├── c0fec0de/anytree >= 2.4.3
    │   └── ⋯
    └── requests/requests >= 2.19.1
        └── ⋯
```

where the ellipsis implies sub-dependencies.


#!/usr/bin/env python3

import argparse
import requests
from anytree import Node, RenderTree
import credentials

class GraphAPI:

    def __init__(self, token: str,
                 endpoint: str = "https://api.github.com/graphql") -> None:
        self.endpoint = endpoint
        authentication_header = {"Authorization": "bearer {}".format(token)}
        preview_header = {"Accept": "application/vnd.github.hawkgirl-preview, "
                                    "application/vnd.github.vixen-preview"}
        self.header = {**authentication_header, **preview_header}

    def run_query(self, query: str) -> dict:
        response = requests.post(self.endpoint, json={"query": query},
                                 headers=self.header)
        response.raise_for_status()
        return response.json()

    def rate_limit(self) -> dict:
        query = """{
            rateLimit
            {
                limit
                cost
                remaining
                resetAt
            }
        }"""
        response = self.run_query(query)
        return response["data"]["rateLimit"]

class DependencyGraph:

    def __init__(self, api: GraphAPI) -> None:
        self._api = api

    def shallow_dependencies(self, repo: str) -> dict:
        owner, name = repo.split("/")
        query = """{
            repository(owner: \"%s\", name: \"%s\")
            {
                vulnerabilityAlerts(first: 100)
                {
                    nodes
                    {
                        affectedRange
                    }
                }
                dependencyGraphManifests(first: 100)
                {
                    nodes
                    {
                        blobPath
                        dependencies(first: 100)
                        {
                            nodes
                            {
                                packageName
                                requirements
                                hasDependencies
                                repository
                                {
                                    nameWithOwner
                                }
                                packageManager
                            }
                        }
                    }
                }
            }
        }""" % (owner, name)
        return self._api.run_query(query)

    def dependency_tree(self, repo: str):
        data = self.shallow_dependencies(repo)
        package_node = Node(repo)
        for manifest in data["data"]["repository"]["dependencyGraphManifests"]["nodes"]:
            manifest_node = Node(manifest["blobPath"].split("/")[-1])
            manifest_node.parent = package_node
            for dependency in manifest["dependencies"]["nodes"]:
                dependency_id = None
                try:
                    dependency_id = dependency["repository"]["nameWithOwner"]
                # Sometimes repositories don't exist.
                except TypeError:
                    dependency_id = dependency["packageName"]
                dependency_node = Node("{} {}".format(dependency_id,
                                                      dependency["requirements"]))
                dependency_node.parent = manifest_node
                if dependency["hasDependencies"]:
                    Node("⋯ ").parent = dependency_node
        return package_node

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate dependency graph")
    parser.add_argument("repository", help="the GitHub owner/repository")
    args = parser.parse_args()

    api = GraphAPI(token=credentials.TOKEN)
    dependencies = DependencyGraph(api)
    tree = dependencies.dependency_tree(args.repository)

    for pre, _, node in RenderTree(tree):
        print("{}{}".format(pre, node.name))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Dependency graphs from the GitHub API"""

import os
import sys
import argparse

import requests
from anytree import Node, RenderTree

class GraphAPI:
    """Interface for the GitHub API"""

    def __init__(self, token: str,
                 endpoint: str = "https://api.github.com/graphql") -> None:
        self.endpoint = endpoint
        self.session = requests.Session()
        authentication_header = {"Authorization": f"bearer {token}"}
        preview_header = {"Accept": "application/vnd.github.hawkgirl-preview"}
        self.session.headers.update({**authentication_header, **preview_header})

    def run_query(self, query: str) -> dict:
        """Make a generic GraphQL query"""
        response = self.session.post(self.endpoint, json={"query": query})
        response.raise_for_status()
        return response.json()

    def rate_limit(self) -> dict:
        """Check API usage"""
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
    """Wrapper for generating dependency trees"""

    def __init__(self, api: GraphAPI) -> None:
        self._api = api

    def _shallow_dependencies(self, repo: str) -> dict:
        owner, name = repo.split("/")
        query = """{
            repository(owner: \"%s\", name: \"%s\")
            {
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

    def dependency_tree(self, repo: str, limit: int, depth: int = 0) -> Node:
        """Query and generate a tree from the response"""
        data = self._shallow_dependencies(repo)
        if data.get("errors"):
            print(data.get("errors"))
            sys.exit(1)
        package_node = Node(repo)
        manifests = data["data"]["repository"]["dependencyGraphManifests"]
        for manifest in manifests["nodes"]:
            manifest_node = Node(manifest["blobPath"].split("/")[-1])
            if manifest["dependencies"]["nodes"]:
                manifest_node.parent = package_node
            for dependency in manifest["dependencies"]["nodes"]:
                try:
                    dependency_id = dependency["repository"]["nameWithOwner"]
                # Sometimes dependency repositories don't exist.
                except TypeError:
                    dependency_id = dependency["packageName"]
                dependency_node = Node(f"{dependency_id} {dependency['requirements']}")
                dependency_node.parent = manifest_node
                if dependency["hasDependencies"]:
                    if depth >= limit:
                        Node("⋯ ").parent = dependency_node
                    else:
                        self.dependency_tree(dependency_id,
                                             limit, depth + 1).parent = dependency_node
        return package_node

def main() -> None:
    """Entry point"""
    parser = argparse.ArgumentParser(description="Generate dependency graph")
    parser.add_argument("repository", help="the GitHub owner/repository")
    parser.add_argument("-r", "--recursion-depth", type=int, default=0)
    args = parser.parse_args()

    api = GraphAPI(token=os.environ["GITHUB_TOKEN"])
    dependencies = DependencyGraph(api)
    tree = dependencies.dependency_tree(args.repository, limit = args.recursion_depth)

    for pre, _, node in RenderTree(tree):
        print(f"{pre}{node.name}")

if __name__ == "__main__":
    main()

""" Summarize all repositories found into one file

    Take all topic lists created by GitHubRepoFinderByTopic.py.
    Generate a list containing each unique repository.
    Just a short intermediate script for further processing.
"""

import os

# avoid duplicates
repo_names = set()

script_path = os.path.dirname(os.path.realpath(__file__))

for filename in os.listdir(os.path.join(script_path, "Searching", "ReposByTopic")):
    input_file = open(os.path.join(script_path, "Searching",
                                   "ReposByTopic", filename), "r")
    oer_repos = input_file.readlines()

    for repo in oer_repos:
        repo_names.add(repo)

file = open(os.path.join(script_path, "Crawling", "Repositories.txt"), "w")

for repo in repo_names:
    file.write(repo)

file.close()

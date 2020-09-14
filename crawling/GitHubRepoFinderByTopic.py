""" Find suitable repositories on Github, given a list of relevant topics.

    Potentially interesting topics are listed in the topics list in the searching folder.
    This script communicates with the Github API to request all known repositories, that are tagged with at least one of the given topics.
    For each topic a file is created, that contains the found repositories.
    To call this script with some basic authentication, it accepts a Github user name and the corresponding passwort or token.
"""

import os
import sys
import time

import requests
from github import Github, GithubException, RateLimitExceededException

# call this script via 'python3 GitHubRepoFinderByTopic.py <GitHub user name> <GitHub user password>'
g = Github(sys.argv[1], sys.argv[2])

script_path = os.path.dirname(os.path.realpath(__file__))

input_file = open(os.path.join(
    script_path, "Searching", "Topics.txt"), "r")

topics = input_file.readlines()

input_file.close()

base_URL = "https://api.github.com/search/repositories?q=topic:"

i = 0
# iterate over all topics, to request all corresponding repositories
while i < len(topics):

    try:
        # remove unnecessary whitespace from topic
        topic = topics[i].strip()

        # current page counter for repsonses split up by pagination
        page_counter = 1
        # get maximum possible results in one response via per_page = 100
        response = requests.get(base_URL + topic + "&page=" +
                                str(page_counter) + "&per_page=100")
        repos = response.json()

        file = open(os.path.join(script_path, "Searching", "ReposByTopic", topic + ".txt"),
                    "w")

        print("Searching repos tagged with '" + topic + "'...")

        for repo in repos["items"]:
            git_repo = g.get_repo(repo["full_name"])
            file.write(
                str(git_repo.full_name) + ";" + str(git_repo.html_url) + ";\n")

        file.close()

        while len(repos["items"]) == 100:
            page_counter += 1
            response = requests.get(base_URL + topic + "&page=" +
                                    str(page_counter) + "&per_page=100")
            repos = response.json()

            if repos["items"]:
                file = open(
                    os.path.join(script_path, "Searching",
                                 "ReposByTopic", topic + ".txt"),
                    "a")

                for repo in repos["items"]:
                    git_repo = g.get_repo(repo["full_name"])
                    file.write(
                        str(git_repo.full_name) + "; " + str(git_repo.html_url) +
                        ";\n")

                file.close()

        i += 1

    except RateLimitExceededException:
        print("Rate Limit exceeded")
        print("Going to sleep for 15 min before restarting")
        print("zzz...")
        # sleep 15 min to reset rate limits
        time.sleep(900)

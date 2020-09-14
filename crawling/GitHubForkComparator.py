""" Get additional information to compare base repositories and their forks.

    Take a list of all potentially relevant repositories generated by GitHubForkFinder.py.
    Generates a list containing additional information provided by the Github API.
    To call this script with some basic authentication, it accepts a Github user name and the corresponding passwort or token.
"""

import os
import sys
import time

from github import Github, GithubException, UnknownObjectException, RateLimitExceededException

# call this script via 'python3 GithubOerRepoCrawler.py <GitHub user name> <GitHub user password>'
g = Github(sys.argv[1], sys.argv[2])

script_path = os.path.dirname(os.path.realpath(__file__))

input_file = open(os.path.join(
    script_path, "Crawling", "RepositoriesAndForks.txt"), "r")
oer_repos_raw = input_file.readlines()
oer_repos = [repo.split(";")[0].strip() for repo in oer_repos_raw]
input_file.close()

output_file = open(
    os.path.join(script_path, "Crawling",
                 "ForkInfos.txt"), "w")

output_file.write(
    "Name;Is fork;Parent;Commits ahead;Commits behind;Pull requests external;\n")

i = 0

while i < len(oer_repos):
    try:
        try:
            try:

                print("Crawling " + oer_repos[i])

                git_repo = g.get_repo(oer_repos[i])

                # Seperate API requests from output writing to avoid broken information lines
                # in case of Rate Limit exceptions
                repo_information = []

                # Connection failures, timeouts or missing information could lead to exceptions
                # when requesting against the Github API.
                # Actually most information should be available, so exceptions are expected to
                # represent connection errors. Probably results could be improved by implementing
                # retry and timeouts for requests.
                repo_information.append(str(git_repo.full_name) + ';')
                repo_information.append(str(git_repo.fork) + ';')

                if git_repo.fork:

                    base_repo = git_repo.parent
                    repo_information.append(str(base_repo.full_name + ';'))

                    base_username = base_repo.full_name.split("/")[0].strip()

                    base = base_repo.default_branch
                    head = git_repo.default_branch

                    try:
                        fork_comparison = git_repo.compare(
                            base, str(base_username) + ':' + head)

                        repo_information.append(
                            str(fork_comparison.ahead_by) + ';'
                        )

                        repo_information.append(
                            str(fork_comparison.behind_by) + ';'
                        )
                    except GithubException:
                        repo_information.append(
                            "No common history;No common history;"
                        )

                else:
                    repo_information.append(
                        "None;None;None;"
                    )

                pull_requests = git_repo.get_pulls(state="all")

                counter = 0
                for pr in pull_requests:
                    if pr.head == pr.base:
                        pass
                    else:
                        counter += 1

                repo_information.append(str(counter) + ';')

                i += 1

            except ConnectionError:
                print("Connection error")
                print("Going to sleep for 5 min before restarting")
                print("zzz...")
                # sleep 5 min before retry
                time.sleep(300)

        except UnknownObjectException:
            i += 1

    except RateLimitExceededException:
        print("Rate Limit exceeded")
        print("Going to sleep for 15 min before restarting")
        print("zzz...")
        # sleep 15 min to reset rate limits
        time.sleep(900)

    for info in repo_information:
        output_file.write(info)

    output_file.write("\n")

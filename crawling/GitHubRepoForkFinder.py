""" Add all repositories' forks to the list of interesting repositories

    Take the Repositories.txt in the Crawling directory created by GitHubRepoSummarizer.py.
    Check every repository for forks and write all repositories to RepositoriesAndForks.txt.
"""
import os
import sys
import time

from github import Github, GithubException, UnknownObjectException, RateLimitExceededException

# call this script via 'python3 GithubOerRepoCrawler.py <GitHub user name> <GitHub user password>'
g = Github(sys.argv[1], sys.argv[2])

script_path = os.path.dirname(os.path.realpath(__file__))

input_file = open(os.path.join(
  script_path, "Crawling", "Repositories.txt"), "r")
oer_repos_raw = input_file.readlines()
oer_repos = [fork.split(";")[0].strip() for fork in oer_repos_raw]
input_file.close()

output_file = open(
    os.path.join(script_path, "Crawling",
                 "RepositoriesAndForks.txt"), "w")

i = 0
while i < len(oer_repos):
  try:
    try:
      
        git_repo = g.get_repo(oer_repos[i])
        forks = git_repo.get_forks()

        output_file.write(str(git_repo.full_name) + ";" + str(git_repo.html_url) + ";\n")
        
        for fork in forks:
            output_file.write(str(fork.full_name) + ";" + str(fork.html_url) + ";\n")

        i += 1

    except UnknownObjectException:
      i += 1

  except RateLimitExceededException:
    print("Rate Limit exceeded")
    print("Going to sleep for 15 min before restarting")
    print("zzz...")
    # sleep 15 min to reset rate limits
    time.sleep(900)

import os
import subprocess
import sys
import time

from github import Github, GithubException

script_path = os.path.dirname(os.path.realpath(__file__))

# call this script via 'python3 GithubTopicCrawlerRunner.py <GitHub user name> <GitHub user password>'
user = sys.argv[1]
password = sys.argv[2]

print("Searching repos for the given topics...")
subprocess.run("python3 GitHubRepoFinderByTopic.py " +
               user + " " + password, shell=True)
print("Summarizing all repos found...")
subprocess.run("python3 GitHubRepoSummarizer.py", shell=True)
print("Searching all forks of repos found...")
subprocess.run("python3 GitHubRepoForkFinder.py " +
               user + " " + password, shell=True)
print("Crawling all relevant information for potential oer repos...")
subprocess.run("python3 GitHubRepoCrawler.py " +
               user + " " + password, shell=True)
print("Analyzing file types used in these repos...")
subprocess.run("python3 GitHubRepoFileTypeAnalyzer.py", shell=True)

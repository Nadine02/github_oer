# Overview

## Scripts

- Topics (selection): [topics.txt](https://github.com/Nadine02/github_oer/blob/master/analysis/topics.txt)
- To run through every script call python3 GitHubCrawlerRunner.py <GitHub user name> <GitHub password>
- GitHubRepoFinderByTopic.py
  - read the topics.txt and create a text file per topic containing all found repositories tagged with the given topic
- GitHubRepoSummarizer.py
  - generate a list of all found repositories
  - this list is used for further processing
- GitHubRepoForkFinder.py
  - read all found repositories, search for their forks
- GitHubRepoCrawler.py
  - read the results of the GitHubRepoForkFinder script
  - for the given repositories information are requested
- GitHubRepoFileTypeAnalyzer.py
  - download the found repositories, analyze the used file extensions
- GitHubForkComparator.py
  - requests additional information are requested
  
  ## Data
  
  Scripts used above generate txt-files with requested information to repositories.
  These files were anonymised to avoid conclusions to names of specific repos. All other relevant figures used for evaluation are provided in the original as csv-files.
 - Repos_Infos.csv -> Data of identified Repos (stars, forks, commits, branches, contributors, watchers, issues, topics, licenses)
 - Repos_Filetypes.csv -> Filetypes of identified Repos
 - Forks_Infos.csv -> Data of Forks (Commits ahead, Pull requests external)

""" Add information on used file types for every repository.

    This information is not provided by the Github API.
    Therefore, literally all found repos are cloned into local storage.
    Pay attention to memory limitation as this can easily take up multiple GB.
"""

import os
import shutil
import subprocess
import sys

script_path = os.path.dirname(os.path.realpath(__file__))

input_file = open(os.path.join(
    script_path, "Crawling", "RepositoriesInformation.txt"), "r")
oer_repos = input_file.readlines()
input_file.close()

output_file = open(os.path.join(
    script_path, "Crawling", "RepositoriesInformationWithFiletypes.txt"), "w")

# result file's headline
output_file.write(
    "full name;stars;is fork;forks;commits;branches;pull requests all;pull requests open;pull requests closed;contributors;watchers;issues;topics;license name;license description;file types;\n")

# skip headline of input file
for repo in oer_repos[1:]:
    os.mkdir("ReposClonedTmp")

    clone_process = subprocess.run("git -C ReposClonedTmp clone " + "https://github.com/" +
                                   repo.split(';')[0] + ".git", shell=True)

    extension_list = set()
    for root, dirs, files in os.walk(os.path.join(script_path, "ReposClonedTmp")):
        for file in files:
            extension_list.add(os.path.splitext(file)[1])

    extensions = ""
    for ext in extension_list:
        extensions += ext + " "
    extensions = extensions.strip() + ";\n"

    output_file.write(repo.replace('\n', '') + extensions)

    shutil.rmtree("ReposClonedTmp", ignore_errors=True)

output_file.close()

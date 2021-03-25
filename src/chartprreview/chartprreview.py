import re
import os
import sys
import subprocess
import argparse

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_modified_charts():
    commit = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], capture_output=True)
    commit_hash = commit.stdout.strip()
    files = subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash], capture_output=True)
    pattern = re.compile("charts/(\w+)/([\w-]+)/([\w-]+)/([\w\.]+)/.*")
    count = 0
    for line in files.stdout.decode("utf-8").split('\n'):
        m = pattern.match(line)
        if m:
            category, organization, chart, version = m.groups()
            return category, organization, chart, version
    return "", "", "", ""


def verify_user(username, category, organization, chart, version):
    data = open(os.path.join("charts", category, organization, chart, "owner.yaml")).read()
    out = yaml.load(data, Loader=Loader)
    if username not in out['usernames']:
        print("User doesn't exist in list of owners:", username)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--verify-user", dest="username", type=str, required=True,
                                        help="check if the user can update the chart")
    args = parser.parse_args()
    category, organization, chart, version = get_modified_charts()
    print(category, organization, chart, version)
    verify_user(args.username, category, organization, chart, version)

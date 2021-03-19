import re
import subprocess

def get_modified_charts():
    commit = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], capture_output=True)
    commit_hash = commit.stdout.strip()
    files = subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash], capture_output=True)
    pattern = re.compile("charts/(\w+)/([\w-]+)/([\w-]+)/([\w\.]+)/.*")
    count = 0
    for line in files.stdout.decode("utf-8").split('\n'):
        print(line)
        m = pattern.match(line)
        breakpoint()
        if m:
            category, organization, chart, version = m.groups()
            return category, organization, chart, version
    return "", "", "", ""

def prepare_chart_for_release(category, organization, chart, version):
    pass

def push_chart_release():
    pass

def create_index():
    pass

def push_index():
    pass

def main():
    category, organization, chart, version = get_modified_charts()
    prepare_chart_for_release(category, organization, chart, version )

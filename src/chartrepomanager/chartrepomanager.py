import shutil
import os
import re
import subprocess

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

def prepare_chart_for_release(category, organization, chart, version):
    path = os.path.join("charts", category, organization, chart, version)
    out = subprocess.run(["helm", "package", path], capture_output=True)
    p = out.stdout.decode("utf-8").strip().split(":")[1].strip()
    chartname = os.path.basename(p)
    try:
        os.remove(os.path.join(os.path.dirname(p), ".cr-release-packages", chartname))
    except FileNotFoundError:
        pass
    shutil.move(p, ".cr-release-packages")
    return chartname

def push_chart_release():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        subprocess.run(["cr", "upload", "-o", "baijum", "-r", "charts", "-t", token], capture_output=True)

def create_index():
    token = os.environ.get("GITHUB_TOKEN")
    #data = {"apiVersion": "v1", "generated": 
    #generated: "2021-03-24T11:25:56.578317012+05:30"

    #out = yaml.dump({"1": "ok"}, Dumper=Dumper)
    print(out)
    #if token:
    #    subprocess.run(["cr", "index", "-c", "https://baijum.github.io/charts/", "-o", "baijum", "-r", "charts", "-t", token, "--push"], capture_output=True)

def update_chart_annotation(chartname):
    subprocess.run(["tar", "zxvf", os.path.join(".cr-release-packages", chartname)], capture_output=True)

def main():
    category, organization, chart, version = get_modified_charts()
    chartname = prepare_chart_for_release(category, organization, chart, version )
    push_chart_release()
    update_chart_annotation(chartname)
    create_index()

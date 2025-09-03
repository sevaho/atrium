#! /usr/bin/python

import asyncio
import requests
import yaml

from pathlib import Path

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Application:
    chart: str
    repo: str
    target_revision: str


def check_latest_chart_version(chart: str, repo: str):
    r = requests.get(repo + "/index.yaml")
    content = yaml.unsafe_load(r.text)
    entries = content["entries"][chart]
    latest = sorted(entries, key=lambda x: datetime.fromisoformat(x["created"]), reverse=True)[0]
    return latest


async def main():
    root_path = Path(".")
    applications = []

    # rglob('*') recursively looks for all files and directories
    for file in root_path.rglob('*'):  # '*' matches all files
        if file.is_file():  # Ensure that it's a file (not a directory)
            if file.name == "application.yaml":
                # it can happen that there are multiple documents in 1 file
                documents = yaml.full_load_all(file.open())
                for document in documents:
                    if document.get("kind") == "Application":

                        if source := document["spec"].get("source"):
                            if chart := source.get("chart"):
                                applications.append(Application(chart=chart, repo=source["repoURL"], target_revision=source["targetRevision"]))
                        elif sources := document["spec"].get("sources"):
                            # multiple sources support (argocd application sources)
                            pass
                        else:
                            raise Exception(f"Unable to find source in {document}")

    # check versions
    for app in applications:
        latest = check_latest_chart_version(app.chart, app.repo)
        print(f"app: {app.chart} current: {app.target_revision} latest: {latest['version']}")


        # break

asyncio.run(main())

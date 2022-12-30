from api import getUserProjects, getUserProjectWorks
from common import elapsed_time_str
import datetime
import json
import os


def makeLogFile(user):
    user_projects = getUserProjects(user)
    logs = []
    for project in user_projects:
        project_works = getUserProjectWorks(project["id"])
        works_log = []
        for work in project_works:
            start_time = datetime.datetime.strptime(
                work["start_time"], '%Y-%m-%dT%H:%M:%S')
            end_time = None
            time = None
            if not end_time is None:
                end_time = datetime.datetime.strptime(
                    work["end_time"], '%Y-%m-%dT%H:%M:%S')
                time = start_time-end_time
            work_log = {
                "start": work["start_time"],
                "end": work["end_time"],
                "time": time,
                "description": work["description"]}
            works_log.append(work_log)
        log = {
            "project": project["name"],
            "total": elapsed_time_str(project["total_seconds"]),
            "works": works_log
        }
        logs.append(log)
    print(logs)
    filepath = './work_file/'+str(user)+".json"
    with open(filepath, 'w') as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)

    return filepath


def rmLogFile(filepath):
    os.remove(filepath)

from api import getUserProjects, getUserProjectWorks
from common import elapsed_time_str
import json
import os


def makeLogFile(user):
    user_projects = getUserProjects(user)
    logs = []
    for project in user_projects:
        project_works = getUserProjectWorks(project["id"])
        works_log = []
        for work in project_works:
            start_time = work["start_time"]
            end_time = None
            time = None
            if not end_time is None:
                end_time = work["end_time"]
                time = start_time-end_time
            work_log = {
                "start": str(work["start_time"]),
                "end": str(work["end_time"]),
                "time": time,
                "description": work["description"]}
            works_log.append(work_log)
        log = {
            "project": project["name"],
            "total": elapsed_time_str(project["total_seconds"]),
            "works": works_log
        }
        logs.append(log)
    filepath = './work_file/'+str(user)+".json"
    with open(filepath, 'w') as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)

    return filepath


def rmLogFile(filepath):
    os.remove(filepath)

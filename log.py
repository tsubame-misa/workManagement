from api import getUserProjects, getUserProjectWorks
from common import elapsed_time_str
import datetime
import json


def makeLogFile(user):
    user_projects = getUserProjects(user)
    logs = []
    for project in user_projects:
        project_works = getUserProjectWorks(project["id"])
        works_log = []
        for work in project_works:
            start_time = datetime.datetime.strptime(
                work["start_time"], '%Y-%m-%dT%H:%M:%S')
            end_time = datetime.datetime.strptime(
                work["end_time"], '%Y-%m-%dT%H:%M:%S')
            work_log = {
                "start": start_time,
                "end": end_time,
                "time": start_time-end_time}
            works_log.append(work_log)
        log = {
            "project": project["name"],
            "total": elapsed_time_str(project["total"]),
            "works": works_log
        }
        logs.append(log)
    with open('./work_file/'+user+".json", 'w') as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)


makeLogFile("misato#1137")

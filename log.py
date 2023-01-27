from api import getUserProjects, getUserProjectWorks
from common import elapsed_time_str, getWorkingTime
import json
import os


def makeLogFile(user):
    user_projects = getUserProjects(user)
    logs = []
    for project in user_projects:
        project_works = getUserProjectWorks(project["id"])
        description_dict = {"詳細なし": 0}
        works_log = []
        for work in project_works:
            time = getWorkingTime(work["start_time"], work["end_time"])
            work_log = {
                "start": str(work["start_time"]),
                "end": str(work["end_time"]),
                "time": elapsed_time_str(time),
                "description": work["description"]}
            works_log.append(work_log)

            time = getWorkingTime(work["start_time"], work["end_time"])
            if work["description"] is None:
                description_dict["詳細なし"] += time
            elif work["description"] in description_dict:
                description_dict[work["description"]] += time
            else:
                description_dict[work["description"]] = time

        for key in description_dict:
            description_dict[key] = elapsed_time_str(description_dict[key])

        log = {
            "project": project["name"],
            "description": description_dict,
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

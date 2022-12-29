from api import getUserProjects, getUserProjectWorks
import csv


def makeLogFile(user):
    user_projects = getUserProjects(user)
    for project in user_projects:
        print("total", project["total_seconds"])
        project_works = getUserProjectWorks(project["id"])
        for work in project_works:
            print(work)


makeLogFile("misato#1137")

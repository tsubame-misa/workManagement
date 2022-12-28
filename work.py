import datetime

start_time = None
total_time = datetime.timedelta(seconds=0)


def getDate():
    date = datetime.datetime.now()
    return date


def formatDate(date):
    return date.strftime('%Y/%m/%d %H:%M:%S')


def elapsed_time_str(seconds):
    """秒をhh:mm:ss形式の文字列で返す

    Parameters
    ----------
    seconds : float
        表示する秒数

    Returns
    -------
    str
        hh:mm:ss形式の文字列
    """
    seconds = int(seconds + 0.5)    # 秒数を四捨五入
    h = seconds // 3600             # 時の取得
    m = (seconds - h * 3600) // 60  # 分の取得
    s = seconds - h * 3600 - m * 60  # 秒の取得

    return f"{h:02}:{m:02}:{s:02}"  # hh:mm:ss形式の文字列で返す


def startWork(user):
    global start_time
    start_time = getDate()
    return start_time


def stopWork(user):
    global start_time, total_time
    if start_time is None:
        return None
    end_time = getDate()
    work_time = end_time-start_time
    total_time += work_time
    start_time = None
    print(total_time)
    return {"end_time": end_time, "work_time":  elapsed_time_str(work_time.total_seconds()), "total_time": elapsed_time_str(total_time.total_seconds())}

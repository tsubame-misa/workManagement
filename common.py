import datetime


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


def getDate():
    date = datetime.datetime.now()
    return date


def formatDate(date):
    return date.strftime('%Y/%m/%d %H:%M:%S')

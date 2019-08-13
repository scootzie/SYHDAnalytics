import os
from datetime import datetime
import importlib


def createSection(folderName):
    subfolderName = folderName + '/Reminder Frequency Stats'
    os.mkdir(subfolderName)
    import teamx_metrics_x as x
    x.saveFile(subfolderName)
    import teamx_metrics_w as w
    w.saveFile(subfolderName)
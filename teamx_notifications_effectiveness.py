import os
from datetime import datetime
import importlib


def createSection(folderName):
    subfolderName = folderName + '/Notifications Effectiveness'
    os.mkdir(subfolderName)
    import teamx_metrics_n1 as n1
    n1.saveFile(subfolderName)
    import teamx_metrics_n2 as n2
    n2.saveFile(subfolderName)
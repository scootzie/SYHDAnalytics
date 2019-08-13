import os
from datetime import datetime
import importlib


def createSection(folderName):
    subfolderName = folderName + '/Search Connections Stats'
    os.mkdir(subfolderName)
    import teamx_metrics_r as r
    r.saveFile(subfolderName)
    import teamx_metrics_s as s
    s.saveFile(subfolderName)
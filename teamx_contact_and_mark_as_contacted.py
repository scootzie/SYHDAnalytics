import os
from datetime import datetime
import importlib


def createSection(folderName):
    subfolderName = folderName + '/Contact Connection AND Mark as Contacted Stats'
    os.mkdir(subfolderName)
    import teamx_metrics_k as k
    k.saveFile(subfolderName)
    import teamx_metrics_l as l
    l.saveFile(subfolderName)
    import teamx_metrics_o as o
    o.saveFile(subfolderName)
    import teamx_metrics_aa as aa
    aa.saveFile(subfolderName)
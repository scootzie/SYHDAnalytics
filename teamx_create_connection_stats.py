import os
from datetime import datetime
import importlib


def createSection(folderName):
    subfolderName = folderName + '/Create Connection Stats'
    os.mkdir(subfolderName)
    import teamx_metrics_g as g
    g.saveFile(subfolderName)
    import teamx_metrics_m as m
    m.saveFile(subfolderName)
    import teamx_metrics_ad as ad
    ad.saveFile(subfolderName)
    import teamx_metrics_an as an
    an.saveFile(subfolderName)
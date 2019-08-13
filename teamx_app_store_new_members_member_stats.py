import os
from datetime import datetime
import importlib


def createSection(folderName):
    subfolderName = folderName + '/App Store, New Members, and Member Stats'
    os.mkdir(subfolderName)
    import teamx_metrics_f as f
    f.saveFile(subfolderName)
    import teamx_metrics_j as j
    j.saveFile(subfolderName)
    import teamx_metrics_i as i
    i.saveFile(subfolderName)
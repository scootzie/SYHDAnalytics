import os
from datetime import datetime
import importlib


def createSection(folderName):
    subfolderName = folderName + '/App Usage, Retention, and Demographics'
    os.mkdir(subfolderName)
    b2e = importlib.import_module("teamx_metrics_b-e")
    b2e.saveFile(subfolderName)
    import teamx_metrics_v as v
    v.saveFile(subfolderName)
    v.saveFile2(subfolderName)
    import teamx_metrics_t as t
    t.saveFile(subfolderName)
    import teamx_metrics_u as u
    u.saveFile(subfolderName)
    import teamx_metrics_ac as ac
    ac.saveFile(subfolderName)
    import teamx_metrics_p as p
    p.saveFile(subfolderName)
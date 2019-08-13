import os
from datetime import datetime
import importlib


def createSection(folderName):
    subfolderName = folderName + '/Impact of Due Connections and Ideal State'
    os.mkdir(subfolderName)
    import teamx_metrics_ai as ai
    ai.saveFile(subfolderName)
    import teamx_metrics_ah as ah
    ah.saveFile(subfolderName)
    import teamx_metrics_z as z
    z.saveFile(subfolderName)
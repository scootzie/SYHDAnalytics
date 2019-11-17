import importlib
import os


def create_section(folder_name):
    subfolder_name = folder_name + '/App Usage, Retention, and Demographics'
    os.mkdir(subfolder_name)
    b2e = importlib.import_module("teamx_metrics_b-e")
    b2e.saveFile(subfolder_name)
    import teamx_metrics_v as v
    v.saveFile(subfolder_name)
    v.saveFile2(subfolder_name)
    import teamx_metrics_t as t
    t.saveFile(subfolder_name)
    import teamx_metrics_u as u
    u.saveFile(subfolder_name)
    import teamx_metrics_ac as ac
    ac.saveFile(subfolder_name)
    import teamx_metrics_p as p
    p.saveFile(subfolder_name)
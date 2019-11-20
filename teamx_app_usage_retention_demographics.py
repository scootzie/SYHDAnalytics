import importlib
import os


def create_section(folder_name):
    subfolder_name = folder_name + '/App Usage, Retention, and Demographics'
    os.mkdir(subfolder_name)
    b2e = importlib.import_module("teamx_metrics_b-e")
    b2e.plot_to_folder(subfolder_name)
    import teamx_metrics_v as v
    v.plot_to_folder(subfolder_name, 1)
    v.plot_to_folder(subfolder_name, 2)
    import teamx_metrics_t as t
    t.plot_to_folder(subfolder_name)
    import teamx_metrics_u as u
    u.plot_to_folder(subfolder_name)
    import teamx_metrics_ac as ac
    ac.plot_to_folder(subfolder_name)
    import teamx_metrics_p as p
    p.plot_to_folder(subfolder_name)

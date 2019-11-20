import os


def create_section(folder_name):
    subfolder_name = folder_name + '/Search Connections Stats'
    os.mkdir(subfolder_name)
    import teamx_metrics_r as r
    r.plot_to_folder(subfolder_name)
    import teamx_metrics_s as s
    s.plot_to_folder(subfolder_name)

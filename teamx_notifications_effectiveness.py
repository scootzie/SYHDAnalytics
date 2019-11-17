import os


def create_section(folder_name):
    subfolder_name = folder_name + '/Notifications Effectiveness'
    os.mkdir(subfolder_name)
    import teamx_metrics_n1 as n1
    n1.saveFile(subfolder_name)
    import teamx_metrics_n2 as n2
    n2.saveFile(subfolder_name)

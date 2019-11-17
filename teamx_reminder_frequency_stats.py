import os


def create_section(folder_name):
    subfolder_name = folder_name + '/Reminder Frequency Stats'
    os.mkdir(subfolder_name)
    import teamx_metrics_x as x
    x.saveFile(subfolder_name)
    import teamx_metrics_w as w
    w.saveFile(subfolder_name)
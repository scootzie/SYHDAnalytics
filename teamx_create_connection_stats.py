import os


def create_section(folder_name):
    subfolder_name = folder_name + '/Create Connection Stats'
    os.mkdir(subfolder_name)
    import teamx_metrics_g as g
    g.saveFile(subfolder_name)
    import teamx_metrics_m as m
    m.saveFile(subfolder_name)
    import teamx_metrics_ad as ad
    ad.saveFile(subfolder_name)
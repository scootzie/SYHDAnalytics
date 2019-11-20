import os


def create_section(folder_name):
    subfolder_name = folder_name + '/Create Connection Stats'
    os.mkdir(subfolder_name)
    import teamx_metrics_g as g
    g.plot_to_folder(subfolder_name)
    import teamx_metrics_m as m
    m.plot_to_folder(subfolder_name)
    import teamx_metrics_ad as ad
    ad.plot_to_folder(subfolder_name)
    import teamx_metrics_an as an
    an.plot_to_folder(subfolder_name)

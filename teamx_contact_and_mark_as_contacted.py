import os


def create_section(folder_name):
    subfolder_name = folder_name + '/Contact Connection AND Mark as Contacted Stats'
    os.mkdir(subfolder_name)
    import teamx_metrics_k as k
    k.plot_to_folder(subfolder_name)
    import teamx_metrics_l as l
    l.plot_to_folder(subfolder_name)
    import teamx_metrics_o as o
    o.plot_to_folder(subfolder_name)
    import teamx_metrics_aa as aa
    aa.plot_to_folder(subfolder_name)

import os


def create_section(folder_name):
    subfolder_name = folder_name + '/App Store, New Members, and Member Stats'
    os.mkdir(subfolder_name)
    import teamx_metrics_f as f
    f.plot_to_folder(subfolder_name)
    import teamx_metrics_j as j
    j.plot_to_folder(subfolder_name)
    import teamx_metrics_i as i
    i.plot_to_folder(subfolder_name)

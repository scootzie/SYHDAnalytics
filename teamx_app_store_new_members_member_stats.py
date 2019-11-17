import os


def create_section(folder_name):
    subfolder_name = folder_name + '/App Store, New Members, and Member Stats'
    os.mkdir(subfolder_name)
    import teamx_metrics_f as f
    f.saveFile(subfolder_name)
    import teamx_metrics_j as j
    j.saveFile(subfolder_name)
    import teamx_metrics_i as i
    i.saveFile(subfolder_name)

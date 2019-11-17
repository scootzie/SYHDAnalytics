import os


def create_section(folder_name):
    subfolder_name = folder_name + '/Impact of Due Connections and Ideal State'
    os.mkdir(subfolder_name)
    import teamx_metrics_ai as ai
    ai.saveFile(subfolder_name)
    import teamx_metrics_ah as ah
    ah.saveFile(subfolder_name)
    import teamx_metrics_z as z
    z.saveFile(subfolder_name)
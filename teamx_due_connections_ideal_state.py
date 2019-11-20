import os


def create_section(folder_name):
    subfolder_name = folder_name + '/Impact of Due Connections and Ideal State'
    os.mkdir(subfolder_name)
    import teamx_metrics_ai as ai
    ai.plot_to_folder(subfolder_name)
    import teamx_metrics_ah as ah
    ah.plot_to_folder(subfolder_name)
    import teamx_metrics_z as z
    z.plot_to_folder(subfolder_name)

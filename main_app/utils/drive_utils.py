from main_app.Constants import designation_drivefolder_mapping


def get_folder_id(designation):
    return designation_drivefolder_mapping.FOLDER[designation]
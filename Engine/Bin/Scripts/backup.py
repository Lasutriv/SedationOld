import shutil
import os
# Set up
path_dir_working = os.path.dirname(os.path.realpath(__file__))
path_dir_working = path_dir_working.strip('\Scripts')

# Files to back up
path_settings = path_dir_working + '\settings.py'

# Location to back up to
path_dir_backup = path_dir_working + '\Backup'

# Perform load
option = input('Keep old? (Y/N): ')
if option is 'Y' or option is 'y' or option is 'Yes' or option is 'yes':
    count = 0
    for the_file in os.listdir(path_dir_backup):
        count += 1
    # Copy files
    shutil.copy2(path_settings, path_dir_backup + '\settings' + str(count) + '.py')
else:
    for the_file in os.listdir(path_dir_backup):
        file_path = os.path.join(path_dir_backup, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    # Copy files
    shutil.copy2(path_settings, path_dir_backup)
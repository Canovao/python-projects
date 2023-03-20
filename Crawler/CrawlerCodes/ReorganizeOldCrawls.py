import os
import shutil

def reorganizeOldCrawls():
    source_path = 'Crawler\\UnstoredCrawls'
    destination_path = 'Crawler\\OldCrawls'

    files = os.listdir(source_path)

    for f in files:
        source_file_path = os.path.join(source_path, f)
        destination_file_path = os.path.join(destination_path, f)
        shutil.move(source_file_path, destination_file_path)
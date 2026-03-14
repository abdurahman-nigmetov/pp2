import shutil

usage = shutil.disk_usage('.')
print(f'Total space: {usage.total // (1024**3)} GB')
print(f'Free space: {usage.free // (1024**3)} GB')

source = "path/to/current/file.txt"
destination = "path/to/new/directory/"
shutil.move(source, destination)
import os
import shutil
import argparse
import zipfile

parser = argparse.ArgumentParser(description='Import image assets from a folder or zip file into an Android project')
parser.add_argument('--source',
                    dest='source',
                    help='Path to source zip file or directory containing assets',
                    required=True)
parser.add_argument('--android_project_dir',
                    dest='android_project_dir',
                    help='Path to Android project directory',
                    required=True)
parser.add_argument('--drawable_directory',
                    dest='drawable_directory',
                    help='Path to directory in Android project containing drawable directories (drawable-xxhdpi, drawable-xhdpi, etc.)',
                    default='src/main/res/')
args = parser.parse_args()
file_list = []

def copy_to_android_project(file=None, file_object=False):
    filename, extension = os.path.splitext(os.path.basename(file))
    destination_filename = filename.split('@')[0] + extension
    resolution = filename.split('@')[1]
    destination_path = os.path.normpath(os.path.join(args.android_project_dir, args.drawable_directory, 'drawable-' + resolution, destination_filename))
    print 'Copying asset "%s" to "%s"...' %(file, destination_path)
    if file_object:
        print 'file_object', file_object
        with open(destination_path, "wb") as fdest:
            shutil.copyfileobj(file_object, fdest)
    else:
        shutil.copyfile(file, destination_path)
    print 'Done'

if zipfile.is_zipfile(args.source):
    print 'Zip file!'
    archive = zipfile.ZipFile(args.source)
    exclude_prefixes = ('.', '__MACOSX')
    files = [f for f in archive.namelist() if not f.startswith(exclude_prefixes)]
    for file in files:
        with archive.open(file) as f:
            copy_to_android_project(file, f)
else:
    for path, subdirs, files in os.walk(args.source):
        for name in files:
            copy_to_android_project(os.path.join(path, name))
print 'Successfully finished copying all assets!'

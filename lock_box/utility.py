import sys
import zipfile
import os
import tempfile
import epub


def get_epub_info(filepath):
    book = epub.open_epub(filepath)
    contents = []
    for item in book.opf.manifest.values():
        # read the content
        contents.append(item.href)
    return contents


def read_line():
    return sys.stdin.readline().strip()


def update_zip(zipname, filename, data):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment  # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as out_zip:
        out_zip.writestr(filename, data)

# pre-processing epub to zip file


def preprocess(filepath):
    if filepath[-4:] != "epub":
        print("invalid file type")
        sys.exit(0)
    else:
        os.rename(filepath, filepath[0:-4]+"zip")
        return filepath[0:-4]+"zip"

# post-processing zip file to epub


def postprocess(filepath):
    if filepath[-3:] != "zip":
        print("invalid file type")
        sys.exit(0)
    else:
        os.rename(filepath, filepath[0:-3]+"epub")
        return filepath[0:-3]+"epub"
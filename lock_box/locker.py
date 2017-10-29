import crypto as c
import sys
import zipfile
import os
import tempfile

def read_line():
    return sys.stdin.readline().strip()


def main():
    running = True
    while running:
        option = input("Input mode (e)ncrypt (d)ecrypt (q)uit\n")
        if option == "e":
            encrypt()
        elif option == "d":
            decrypt()
        elif option == "q":
            running = False

        else:
            print("Invalid Operation")


def updateZip(zipname, filename, data):
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


def preprocess(filepath):
    if filepath[-4:] != "epub":
        print("invalid file type")
        sys.exit(0)
    else:
        os.rename(filepath, filepath[0:-4]+"zip")
        return filepath[0:-4]+"zip"


def postprocess(filepath):
    if filepath[-3:] != "zip":
        print("invalid file type")
        sys.exit(0)
    else:
        os.rename(filepath, filepath[0:-3]+"epub")
        return filepath[0:-3]+"epub"


def encrypt():
    print("Please enter path to file")
    file_path = read_line()
    print("Please enter Encryption pass phrase")
    password = read_line()
    key = c.create_key(password)
    zip_name = preprocess(file_path)
    with zipfile.ZipFile(zip_name, mode='r') as myzip:
        for name in myzip.namelist():
                if name.endswith(".xhtml") or name.endswith(".css") or name.endswith(".opf") or name.endswith(".ncx") :
                    with myzip.open(name) as in_file:
                        contents = in_file.read()
                        out = c.encrypt_AES(key, contents)
                    updateZip(zip_name, name, out)
                else:
                    with myzip.open(name) as in_file:
                        contents = in_file.read()
                        updateZip(zip_name, name, contents)

    postprocess(zip_name)


def decrypt():
    print("Please enter path to file")
    file_path = read_line()
    print("Please enter Encryption pass phrase")
    password = read_line()
    key = c.create_key(password)
    zip_name = preprocess(file_path)
    with zipfile.ZipFile(zip_name, mode='r') as myzip:
        for name in myzip.namelist():
                if name.endswith(".xhtml") or name.endswith(".css") or name.endswith(".opf") or name.endswith(".ncx") :
                    with myzip.open(name) as in_file:
                        contents = in_file.read()
                        out = c.decrypt_AES(key, contents)
                    updateZip(zip_name, name, out)
                else:
                    with myzip.open(name) as in_file:
                        contents = in_file.read()
                        updateZip(zip_name, name, contents)

    postprocess(zip_name)




if __name__=="__main__":
    main()
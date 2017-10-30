import crypto as c
import utility as u
import zipfile


# simple menu interface will update in future
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



def encrypt():
    print("Please enter path to file")
    file_path = u.read_line()
    print("Please enter Encryption pass phrase")
    password = u.read_line()
    manifest = u.get_epub_info(file_path)
    actual_content = []
    # generating AES cipher using inputted password
    key = c.create_key(password)
    # turning .epub into .zip for ease of use
    zip_name = u.preprocess(file_path)
    with zipfile.ZipFile(zip_name, mode='r') as myzip:
        for name in myzip.namelist():
            if name.startswith("OEBPS/"):
                actual_content.append(name[6:])
            # encrypt only the files that require encryption, ignore meta and image files
            if name.endswith(".xhtml") or name.endswith(".css") or name.endswith(".opf") or name.endswith(".ncx") :
                with myzip.open(name) as in_file:
                    contents = in_file.read()
                    out = c.encrypt_AES(key, contents)
                u.update_zip(zip_name, name, out)
            else:
                with myzip.open(name) as in_file:
                    contents = in_file.read()
                    u.update_zip(zip_name, name, contents)

    # Compare the file manifest to files found
    for item in manifest:
        if item in actual_content:
            actual_content.remove(item)

    # Must remove this file as it isn't tracked in the actual manifest
    # actual_content.remove("package.opf")
    # actual_content.remove("")
    
    if len(actual_content) > 0:
        print(len(actual_content))
        print("[WARN] Following items not listed in manifest")
        for item in actual_content:
            print(item)

    u.postprocess(zip_name)


def decrypt():
    # Its importanr to note that we do not check for a successful decryption or correct password
    # If intercepted we do not want to give attackers the ability to discern correct from incorrect attempts
    print("Please enter path to file")
    file_path = u.read_line()
    print("Please enter Encryption pass phrase")
    password = u.read_line()
    # generating AES cipher using inputted password
    key = c.create_key(password)
    # turning .epub into .zip for ease of use
    zip_name = u.preprocess(file_path)
    with zipfile.ZipFile(zip_name, mode='r') as myzip:
        for name in myzip.namelist():
                if name.endswith(".xhtml") or name.endswith(".css") or name.endswith(".opf") or name.endswith(".ncx") :
                    with myzip.open(name) as in_file:
                        contents = in_file.read()
                        out = c.decrypt_AES(key, contents)
                    u.update_zip(zip_name, name, out)
                else:
                    with myzip.open(name) as in_file:
                        contents = in_file.read()
                        u.update_zip(zip_name, name, contents)

    u.postprocess(zip_name)




if __name__=="__main__":
    main()
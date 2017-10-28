import crypto as c
import sys
import base64
def read_line():
    return sys.stdin.readline().strip()


def main():
    print("Please enter path to file")
    file_path = read_line()
    with open(file_path, 'rb') as f:
        contents = f.read()
    contents = base64.b64encode(contents)

    print("Please enter Encryption pass phrase")
    password = read_line()
    out = c.encrypt_AES(c.create_key(password), contents)

    ef = open('encrypted.zip', 'rb+')
    ef.write(out)


if __name__=="__main__":
    main()
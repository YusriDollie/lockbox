import crypto as c
import sys
import base64
def read_line():
    return sys.stdin.readline().strip()


def main():
    running = True
    while running:
        option = input("Input mode (e)ncrypt (d)ecrypt (q)uit")
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
    file_path = read_line()
    with open(file_path, 'rb') as f:
        contents = f.read()
    print(contents)
    contents = base64.b64encode(contents)
    print(contents)
    print("Please enter Encryption pass phrase")
    password = read_line()
    out = c.encrypt_AES(c.create_key(password), contents)

    ef = open('encrypted', 'w+')
    ef.write(out)
    ef.close()

def decrypt():
    print("Please enter path to file")
    file_path = read_line()
    with open(file_path, 'rb') as f:
        contents = f.read()
    print(contents)
    print("Please enter Encryption pass phrase")
    password = read_line()
    out = c.decrypt_AES(c.create_key(password), contents)
    ef = open('decrypted', 'w+')
    print(out)
    ef.write(out)
    ef.close()


if __name__=="__main__":
    main()
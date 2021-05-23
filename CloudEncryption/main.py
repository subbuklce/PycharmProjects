import os
import getpass
import re
import datetime

def check_password(password):
    if 8 < len(password) < 25:
        return False
    if password == "\n" or password == " ":
        return False
    if re.search(r'(.)\1\1', password):
        print(' The password contains two or more duplicate characters in sequence')
        return False
    if re.search(r'(..)(.*?)\1', password):
        print(' Two more words repeated, same string pattern')
        return False
    return True


def create_new_encrypted_file(absolute_path,individual_file_name):
    global userpassword, dst_path
    full_command = "openssl aes-256-cbc -e -in " + absolute_path + " -out " +dst_path + "/"+ individual_file_name+".enc -md md5 -pass pass:"+userpassword
    returnunicode = os.system(full_command)
    print(" The return code is{} ".format(returnunicode))


def decrypt_encrypted_file(absolute_path,individual_file_name):
    global userpassword,dst_path
    full_command = "openssl aes-256-cbc -d -in " + absolute_path + " -out " + dst_path + "/"+individual_file_name[:-4]+" -md md5 -pass pass:"+userpassword
    returnunicode = os.system(full_command)
    print(" The return code is{} ".format(returnunicode))


def encryption():
    global directoryname
    for dir_paths, dir_names, filenames in os.walk(directoryname):
        for each_file in filenames:
            if ".enc" not in each_file:
                print('The file name is:', each_file)
                absolute_path = os.path.join(dir_paths,  each_file)
                create_new_encrypted_file(absolute_path,each_file)


def decryption():
    global directoryname
    for dir_paths, dir_names, filenames in os.walk(directoryname):
        for each_file in filenames:
            if ".enc" in each_file:
                print('The file name is:', each_file)
                absolute_path = os.path.join(dir_paths,  each_file)
                decrypt_encrypted_file(absolute_path,each_file)
            else:
                print(" Ignoring the file {}".format(each_file))


if __name__ == '__main__':
    print("\n Remember for easiness this program places encrypted/decrypted files into /tmp/date location")
    dirname = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    global dst_path
    dst_path = "/tmp/" + dirname
    cmd = "mkdir -p /tmp/" + dirname
    os.system(cmd)
    global directoryname, userpassword
    directoryname = input('Please enter the directory name (full path) or .(current dir):')
    userpassword = getpass.getpass(prompt='Provide the password:')
    choice = int(input("1.Encryption\n2.Decryption\n\n"))
    if choice == 1:
        encryption()
    elif choice == 2:
        decryption()
    else:
        print("\n You entered wrong choice\n")



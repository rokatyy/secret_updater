import sys, os
import shutil
import subprocess
import base64
from Crypto.Cipher import _AES
import cx_Freeze
import time

sys_file = 'sys.info'
default_vector = 16 * '\x00'
key = 'secret'
REG_PATH = 'HKCU\\Software\\ANN_KAT'
set_readonly_command = 'ATTRIB +R +S {file}'
set_reg_command = 'reg add {REG_PATH} /t REG_DWORD /d {key} /f '


def check_dir(directory):
    if os.path.isdir(directory):
        return True
    else:
        raise AssertionError("[ERROR] Directory {} doesn't exist".format(directory))


def main():
    dir_for_sysinfo = input("Print directory:")
    try:
        check_dir(dir_for_sysinfo)
    except Exception as e:
        print(e)
    current_file = os.path.abspath(__file__)
    intruder_filename = os.path.join(dir_for_sysinfo, 'notepad.exe')
    filesys_full_path = os.path.join(dir_for_sysinfo, sys_file)
    if not os.path.isfile(filesys_full_path):
        command = ["powershell.exe", 'systeminfo', '>>', '{file}'.format(file=filesys_full_path)]
        shutil.copy(current_file, intruder_filename)
        run_powershell_command(command)
        time.sleep(20)
        encrypt_file(filesys_full_path, key)
        os.system(set_readonly_command.format(file=intruder_filename))
        os.system(set_readonly_command.format(file=filesys_full_path))
        os.system(set_reg_command.format(REG_PATH=REG_PATH, key=key))
    else:
        text = decrypt_text(filesys_full_path, key)
        print(text)


def run_powershell_command(command):
    p = subprocess.Popen(command, bufsize=-1, stdout=sys.stdout)


def encrypt_file(filename, key, vector=default_vector):
    file_text = open(filename, 'r').read()
    encrypted_txt = encrypt_text(file_text, key, vector)
    f = open(filename, 'wb')
    f.write(encrypted_txt)


def encrypt_text(text, key, vector=default_vector):
    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode, IV=vector)
    return encryptor.encrypt(text)


def decrypt_file(filename, key):
    file_text = open(filename, 'rb')
    file_text = file_text.read()
    decrypted_txt = decrypt_text(file_text, key)
    return decrypt_text(decrypted_txt)


def decrypt_text(text, key):
    cipher = base64.b64decode(text)
    return cipher


if __name__ == "__main__":
    main()

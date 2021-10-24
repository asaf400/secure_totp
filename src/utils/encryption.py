from pathlib import Path
import platform
import keyring

try:
    import win32crypt
except:
    pass


class Encryption(object):
    def __init__(self):
        local_system = platform.system()
        if local_system == 'Windows':
            self.encryptor = Win32Encryption()
        elif local_system == 'Linux':
            import keyring

class LinuxEncryption(object):
    def __init__(self):
        pass

    def decrypt(self):
        return keyring.get_password('system','safer_totp.db.json')

    def encrypt(self,data):
        return keyring.set_password('system','safer_totp.db.json', data)

class Win32Encryption(object):
    def __init__(self):
        pass

    def decrypt(self, data=None):
        encrypted_data = data
        clear_data = win32crypt.CryptUnprotectData(encrypted_data, None, None, None, 0)
        # replaced=clear_data[1].replace(b'\x02', b' ').replace(b'\x03', b' ')
        return str(clear_data[1], 'UTF-8')

    def encrypt(self, data):
        if hasattr(data, 'encode'):
            clear_data = data.encode('UTF-8')
        else:
            clear_data = data
        encrypted_data = win32crypt.CryptProtectData(clear_data, None, None, None, None, 0)
        return encrypted_data


if __name__ == '__main__':
    stor = Win32Encryption()
    print(stor.encrypt("HelloWorld"))
    print(stor.decrypt(stor.encrypt("HelloWorld")))
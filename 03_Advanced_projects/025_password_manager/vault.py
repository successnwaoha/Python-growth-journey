import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# 1. The "Key Maker"
# This turns your Master Password into a complex 32-byte key
def derive_key(master_password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

# 2. The Vault Class
class ZenVault:
    def __init__(self, master_password):
        self.password_file = "vault.json.enc"
        self.salt_file = "salt.key"
        
        # We need a "Salt" to make the encryption unique
        if os.path.exists(self.salt_file):
            with open(self.salt_file, "rb") as f:
                self.salt = f.read()
        else:
            self.salt = os.urandom(16)
            with open(self.salt_file, "wb") as f:
                f.write(self.salt)
        
        # Derive the key and initialize the "encrypter" (Fernet)
        self.key = derive_key(master_password, self.salt)
        self.fernet = Fernet(self.key)

    def save_passwords(self, data):
        # Convert dictionary to JSON string, then encrypt it
        json_data = json.dumps(data).encode()
        encrypted_data = self.fernet.encrypt(json_data)
        with open(self.password_file, "wb") as f:
            f.write(encrypted_data)

    def load_passwords(self):
        if not os.path.exists(self.password_file):
            return {}
        try:
            with open(self.password_file, "rb") as f:
                encrypted_data = f.read()
            # Decrypt the data and turn it back into a dictionary
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception:
            # If the password is wrong, decryption will fail
            return None

# 3. The CLI Interface
def main():
    mp = input("Enter Master Password: ")
    vault = ZenVault(mp)
    
    data = vault.load_passwords()
    if data is None:
        print("❌ Wrong Master Password! Access Denied.")
        return

    while True:
        choice = input("\n1. Add Password\n2. Get Password\n3. List All\n4. Exit\nChoice: ")
        
        if choice == "1":
            site = input("Website: ")
            pwd = input(f"Password for {site}: ")
            data[site] = pwd
            vault.save_passwords(data)
            print("✅ Saved!")
            
        elif choice == "2":
            site = input("Website: ")
            print(f"Password: {data.get(site, 'Not found')}")
            
        elif choice == "3":
            for site in data:
                print(f"- {site}")
        
        elif choice == "4":
            break

if __name__ == "__main__":
    main()
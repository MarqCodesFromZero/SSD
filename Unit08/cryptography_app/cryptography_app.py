
from cryptography.fernet import Fernet
import os

def generate_key():
    """
    Generates and saves an encryption key to a file.
    Justification: A secure encryption key is necessary for encrypting and decrypting files.
    """
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    print("Encryption key has been generated and saved as 'key.key'.")

def load_key():
    """
    Loads the encryption key from the file.
    Justification: To perform encryption or decryption, the saved key must be retrieved.
    Ensures the file exists before attempting to read it.
    """
    if not os.path.exists('key.key'):
        print("Key file not found! Please generate a key first.")
        return None
    with open('key.key', 'rb') as key_file:
        return key_file.read()

def encrypt_file(file_path):
    """
    Encrypts the specified file using the loaded encryption key.
    Justification: Encryption ensures sensitive data is protected against unauthorized access.
    """
    key = load_key()  # Retrieve the encryption key
    if not key:
        return

    fernet = Fernet(key)  # Create a Fernet cipher with the key

    # Read the contents of the file
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
    except FileNotFoundError:
        print("File not found!")  # Notify the user if the file doesn't exist
        return

    # Encrypt the file data
    encrypted_data = fernet.encrypt(data)

    # Save the encrypted data to a new file
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print(f"File encrypted successfully and saved as '{encrypted_file_path}'.")

def main():
    """
    Provides a menu interface for the user to perform actions such as generating a key,
    encrypting a file, or exiting the program.
    Justification: Simplifies interaction by guiding the user through available functionalities.
    """
    while True:
        print("\nOptions:")
        print("1. Generate Encryption Key")
        print("2. Encrypt a File")
        print("3. Exit")
        
        choice = input("Select an option (1/2/3): ")

        if choice == '1':
            generate_key()  # Generate and save a new encryption key
        elif choice == '2':
            file_path = input("Enter the path to the file you want to encrypt: ")
            encrypt_file(file_path)  # Encrypt the specified file
        elif choice == '3':
            print("Exiting program.")  # Exit the application
            break
        else:
            print("Invalid option. Please try again.")  # Handle invalid inputs

if __name__ == '__main__':
    main()

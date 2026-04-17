
# Cryptography App

This is a Python application that provides basic cryptography functionalities. 
It allows users to generate encryption keys and encrypt files securely.

## Features

- **Generate Encryption Key**: Creates and saves a cryptographic key to a file.
- **Encrypt Files**: Encrypts specified files using the generated key.
- **Interactive Menu**: Provides an easy-to-use interface for the user.

## Prerequisites

- Python 3.6 or higher
- `cryptography` library (`pip install cryptography`)

## Usage

1. Clone or download this repository.
2. Install the required dependencies by running:
   ```bash
   pip install cryptography
   ```
3. Run the application:
   ```bash
   python cryptography_app.py
   ```

## Instructions

1. **Generate Encryption Key**: 
   - Select option `1` from the menu.
   - A new file named `key.key` will be created to store the encryption key.

2. **Encrypt a File**:
   - Select option `2` from the menu.
   - Provide the path to the file you want to encrypt.
   - An encrypted version of the file will be saved with the extension `.encrypted`.

3. **Exit**:
   - Select option `3` from the menu to exit the application.

## Notes

- Ensure the `key.key` file is kept secure as it is required for decryption (not included in this app).
- The application does not currently include decryption functionality.



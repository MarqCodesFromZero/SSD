"""Module to encode or decode text using a Caesar cipher."""

import string

def caesar_cipher(choice, word, shift=3):
    """Encode or decode text using a Caesar cipher."""
    letters = string.ascii_letters + string.punctuation + string.digits
    encoded = ''
    
    if choice == "encode":
        for letter in word:
            if letter == ' ':
                encoded += ' '
            else:
                x = letters.index(letter) + shift
                encoded += letters[x]
    elif choice == "decode":
        for letter in word:
            if letter == ' ':
                encoded += ' '
            else:
                x = letters.index(letter) - shift
                encoded += letters[x]
    
    return encoded

if __name__ == "__main__":
    choice = input("Would you like to encode or decode? ")
    word = input("Please enter text: ")
    print(caesar_cipher(choice, word))
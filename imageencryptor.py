from cryptosteganography import CryptoSteganography
import os
from typing import Optional

class ImageEncryptor:
    """
    A class for encrypting and hiding messages or files within images using steganography.
    Uses the CryptoSteganography library for encryption and steganographic operations.
    """

    def __init__(self, key: str):
        """
        Initialize the ImageEncryptor with an encryption key.
        
        Args:
            key (str): The encryption key used for hiding and retrieving data
        """
        self.crypto = CryptoSteganography(key)
    
    def encrypt_message(self, message: str, image: str) -> Optional[str]:
        """
        Encrypt and hide a text message within an image.
        
        Args:
            message (str): The message to hide in the image
            image (str): Path to the input image file
            
        Returns:
            str: Path to the output encrypted image, or None if encryption fails
        """
        # Create an encrypted image filename by appending '_encrypted.png'
        print ("encrypting")
        filename, extension = os.path.splitext(image)
        print (filename)
        output_filename = filename + "_encrypted.png"
        
        try:
            # Hide the message inside the image using steganography
            self.crypto.hide(input_filename=image, 
                            output_filename=output_filename, 
                            data=message)
            return output_filename
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def decrypt_message(self, image: str) -> Optional[str]:
        """
        Retrieve and decrypt a hidden message from an image.
        
        Args:
            image (str): Path to the encrypted image file
            
        Returns:
            str: The decrypted message, or None if decryption fails
        """
        try:
            # Extract and decrypt the hidden message from the image
            decrypted_message = self.crypto.retrieve(input_image_file=image)
            if decrypted_message:
                return decrypted_message
            else:
                print("No message found in the image.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

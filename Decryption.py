from PIL import Image
import hashlib

def decrypt_image(image_path, password):
    """Decrypts text from an image with password protection."""
    try:
        img = Image.open(image_path).convert('RGBA')
        data = list(img.getdata())
        binary_data = ''

        for r, g, b, a in data:
            binary_data += str(b & 1)

        all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]

        decoded_text = ''
        for byte in all_bytes:
            try:
                char_code = int(byte, 2)
                if 32 <= char_code <= 126:
                    decoded_text += chr(char_code)
                else:
                    break
            except ValueError:
                break

        parts = decoded_text.split(":", 1) #split only at the first colon
        if len(parts) != 2:
          print("Invalid encrypted data, or incorrect password")
          return

        hashed_password_from_image, encrypted_message = parts

        hashed_input_password = hashlib.sha256(password.encode()).hexdigest()

        if hashed_password_from_image == hashed_input_password:
            print("Decrypted text:", encrypted_message)
        else:
            print("Incorrect password.")

    except FileNotFoundError:
        print("Image file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    image_path = input("Enter the encrypted image path: ")
    password = input("Enter the password: ")
    decrypt_image(image_path, password)
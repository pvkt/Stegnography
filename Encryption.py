from PIL import Image
import hashlib

def encrypt_image(image_path, text, output_path, password):
    """Encrypts text within an image with password protection."""
    try:
        img = Image.open(image_path).convert('RGBA')
        width, height = img.size
        data = list(img.getdata())

        if len(text) * 3 > width * height * 3:
            raise ValueError("Text too large to hide in image.")

        # Password hashing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        text_with_password = f"{hashed_password}:{text}"  # Prepend hash

        text_bin = ''.join(format(ord(char), '08b') for char in text_with_password)
        text_len = len(text_bin)
        data_index = 0

        for bit in text_bin:
            r, g, b, a = data[data_index]
            if bit == '1':
                b = b | 1
            else:
                b = b & ~1
            data[data_index] = (r, g, b, a)
            data_index += 1

        img.putdata(data)
        if output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
            img = img.convert("RGB")
        img.save(output_path)
        print(f"Text encrypted and saved to {output_path}")

    except FileNotFoundError:
        print("Image file not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    image_path = input("Enter the image path: ")
    text = input("Enter the text to hide: ")
    password = input("Enter the password: ")
    output_path = input("Enter the output image path(save as .png): ")
    encrypt_image(image_path, text, output_path, password)
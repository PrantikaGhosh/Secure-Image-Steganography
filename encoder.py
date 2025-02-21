import cv2
import os

# Load Image
image_path = r"C:\Users\prant\OneDrive\Desktop\Stego\laptop.jpg"  # Change this to your actual image path
img = cv2.imread(image_path)

if img is None:
    print("Error: Could not read the image. Check the file path.")
    exit()

# Input Secret Message and Password
msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Ensure the message can fit in the image
max_capacity = (img.shape[0] * img.shape[1] * 3) - 1  # Reserve space for length storage
if len(msg) > max_capacity:
    print("Error: Message too large for image!")
    exit()

# Encode Message Length in the First Pixel (R, G, B)
msg_len = len(msg)
img[0, 0] = (msg_len % 256, msg_len // 256, 0)  # Store length in 2 bytes

# Encoding Process
m, n, z = 1, 0, 0  # Start from (0,1) to avoid overwriting length
for char in msg:
    img[n, m, z] = ord(char)  # Store character as pixel value
    z += 1
    if z == 3:  # Move to next pixel
        z = 0
        m += 1
        if m >= img.shape[1]:  # Move to next row
            m = 0
            n += 1

# Save Encoded Image as PNG (to prevent pixel alteration)
encoded_image_path = r"C:\Users\prant\OneDrive\Desktop\Stego\encryptedImage.png"
cv2.imwrite(encoded_image_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])  # No compression

# Save Password for Decoding
with open("password.txt", "w") as file:
    file.write(password)

print("Message encoded successfully! Image saved as:", encoded_image_path)

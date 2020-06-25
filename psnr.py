# Calculate PSNR of the original image and the stegcontainer image
from PIL import Image
import math

def psnr(input_image, output_image):
    output_image = Image.open(output_image, mode='r')
    width, height = output_image.size
    # Decode the first 8 bits to get the length (a number of characters) of the secret message
    binary_length = ''
    binary_length_index = 0
    for y in range(height):
        for x in range(width):
            pixel = output_image.getpixel((x, y))
            for i in range(len(pixel)):
                if binary_length_index < 8:
                    if pixel[i] % 2 == 0:
                        binary_length += '0'
                        binary_length_index += 1
                    elif pixel[i] % 2 == 1:
                        binary_length += '1'
                        binary_length_index += 1
                else:
                    break
    # Number of channels need to be calculated
    channel_number = int(binary_length, 2) * 8 + 8
    # Calculate PSNR of the {length * 8} bits, skip the first 8 bits
    input_image = Image.open(input_image, mode='r')
    current_channel_number = 0
    I_K_2 = 0
    for y in range(height):
        for x in range(width):
            output_pixel = output_image.getpixel((x, y))
            input_pixel = input_image.getpixel((x, y))
            for i in range(len(pixel)):
                if current_channel_number < channel_number:
                    subtraction = input_pixel[i] - output_pixel[i]
                    if (subtraction != 0):
                        I_K_2 += 1
                    current_channel_number += 1
                else:
                    break
    mse = I_K_2 / (width * height * 3)
    psnr = 10 * math.log(pow(255, 2) / mse, 10)
    return psnr

# The main program
if __name__ == '__main__':
    print(psnr('input_image.bmp', 'output_image50.bmp'))



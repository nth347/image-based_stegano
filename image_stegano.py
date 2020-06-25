# Python program implementing image-based steganography
from PIL import Image

# This function converts character string into binary string
def str_2_bin(secret_message):
    binary_message = ''
    for character in secret_message:
        binary_message += bin(ord(character))[2:].zfill(8)
    return binary_message

# This function converts binary string into character string
def bin_2_str(binary_message):
    secret_message = ''
    for i in range(0, len(binary_message), 8):
        secret_message += chr(int(binary_message[i:i+8], 2))
    return secret_message

# This function embeds the secret message into the input image, then saves the output image
def encode(filename_in, secret_message, filename_out):
    binary_message = str_2_bin(secret_message)
    binary_length = bin(len(secret_message))[2:].zfill(8)
    total_data = binary_length + binary_message
    #print(total_data)

    image = Image.open(fp=filename_in, mode='r')
    width, heigth = image.size
    data_index = 0
    total_data_length = len(total_data)
    #while(data_index < total_data_length):
    for y in range(heigth): # y
        for x in range(width): # x
            pixel = list(image.getpixel((x, y))) # x, y
            for k in range(len(pixel)):
                if data_index < total_data_length:
                    # Replace the LSB value
                    new_pixel = int(bin(pixel[k])[2:].zfill(8)[:-1] + total_data[data_index], 2)
                    pixel[k] = new_pixel
                    data_index += 1
                else:
                    break
            image.putpixel((x, y), tuple(pixel))
    image.save(filename_out)
    image.close()

# This function extract the secret message from the image
def decode(filename_in):
    image_in = Image.open(filename_in, mode='r')
    width, height = image_in.size
    # Decode the first 8 bits to get the length (a number of characters) of the secret message
    binary_length = ''
    binary_length_index = 0
    for y in range(height):
        for x in range(width):
            pixel = image_in.getpixel((x, y))
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
    length = int(binary_length, 2)
    # Continue decode {length} characters of the secret message, skip the first 8 bits
    binary_message = ''
    binary_message_index = 0
    for y in range(height):
        for x in range(width):
            pixel = image_in.getpixel((x, y))
            for i in range(len(pixel)):
                if binary_message_index < 8:
                    binary_message_index += 1
                    continue
                elif binary_message_index >= 8 and len(binary_message) < length * 8:
                    if pixel[i] % 2 == 0:
                        binary_message += '0'
                    elif pixel[i] % 2 == 1:
                        binary_message += '1'
                else:
                    break
    #print(binary_message)
    secret_message = bin_2_str(binary_message)
    return secret_message

# The main program
if __name__ == '__main__':
    """ encode('input_image.bmp', 'The Government of the Socialist Republic of Vietnam is the executive arm of the Vietnamese state, and the members of the Government are elected by the National Assembly of Vietnam. The Government of the Socialist Republic of Vietnam is the executive arm o', 'output_image.bmp')
    decode('output_image.bmp') """
    operation = input('1. Encode, 2. Decode: ')
    if operation == '1':
        print('ENCODING ...')
        input_text = input('Input text file (input_text.txt): ')
        src_image = input('Source image file (input_image.bmp): ')
        dst_image = input('Destination image file (output_image.bmp): ')
        f = open(file=input_text, mode='r', encoding='utf8')
        secret_message = f.read()
        f.close()
        encode(src_image, secret_message, dst_image)
        print("Encoded successfully")
    elif operation == '2':
        print('DECODING ...')
        encoded_image = input('Input image file (output_image.bmp): ')
        output_text = input('Output text file (output_text.txt): ')
        secret_message = decode(encoded_image)
        f = open(file=output_text, mode='w', encoding='utf8')
        f.write(secret_message)
        f.close()
        print("Decoded successfully")
    else:
        exit()
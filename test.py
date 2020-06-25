from PIL import Image

image_in = Image.open('output_image.bmp', mode='r')
width, height = image_in.size

count = 0
for y in range(height):
    for x in range(width):
        pixel = image_in.getpixel((x, y))
        if count < 6:
            print(pixel)
            count += 1
        else:
            break
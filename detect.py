# Detect image-based steganography
from PIL import Image

def detect(encoded_image, detected_image):
    image = Image.open(fp=encoded_image, mode='r')
    width, heigth = image.size
    for y in range(heigth):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for k in range(len(pixel)):
                if pixel[k] % 2 == 0:
                    pixel[k] = 1
                elif pixel[k] % 2 == 1:
                    pixel[k] = 255
            image.putpixel((x, y), tuple(pixel))
    image.save(detected_image)
    image.close()
    
# The main program
if __name__ == '__main__':
    sample_image = input('Image file name that you want to analyze: ')
    detected_image = input('New image file name: ')
    detect(sample_image, detected_image)
    
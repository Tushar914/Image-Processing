# pylint: disable=C
from PIL import Image

def convert_to_grunge(img_url, threshold=128, save_image=False):
    img_orig = Image.open(img_url)
    width, height = img_orig.size
    print("Width: ", width, " | Height: ", height)
    
    img_new = Image.new(mode="RGB", size=(width, height))

    for w in range(width):
        for h in range(height):
            current_pixel = img_orig.getpixel((w, h))
            condition = (current_pixel[0] > threshold) or (current_pixel[1] > threshold) or (current_pixel[2] > threshold)
            if condition:
                img_new.putpixel((w, h), (255, 255, 255))
            else:
                img_new.putpixel((w, h), (0, 0, 0))

    img_new.show()

    if save_image:
        img_new.save("".join(img_orig.filename.split('.')[:-1]) + " altered.png")

convert_to_grunge('images/asphalt.png', 32, True)
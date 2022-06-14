# pylint: disable=C
from PIL import Image

def get_pixel_neighbours(x, y):
    neighbour_offset_lst = [(-1, -1), (0, -1), (1, -1),
                            (-1,  0), (0,  0), (1,  0), (-1,  1), (0,  1), (1,  1)]
    neighbour_lst = []
    for neighbour_offset in neighbour_offset_lst:
        neighbour = (x + neighbour_offset[0], y + neighbour_offset[1])
        neighbour_lst.append(neighbour)

    return neighbour_lst


def image_filter(img_url, save_image=False, grayscale=False, effect_strength=1):
    img_orig = Image.open(img_url)
    width, height = img_orig.size
    print("Width: ", width, " | Height: ", height)

    effect = [1, 0, -1, 2, 0, -2, 1, 0, -1]
    img_new = Image.new(mode="RGB", size=(width, height))

    for w in range(0, width):
        for h in range(0, height):
            n_list = get_pixel_neighbours(w, h)
            effect_idx = 0
            all_rgb = []
            for n_pixel in n_list:
                if (n_pixel[0] >= width) or (n_pixel[1] >= height) or (n_pixel[0] <= 0) or (n_pixel[1] <= 0):
                    #print("Neighbour: ", n_pixel, " out of bounds")
                    continue
                pixel_rgb = img_orig.getpixel(n_pixel)
                new_rgb = apply_effect_to_rgb(pixel_rgb, effect[effect_idx])
                effect_idx += 1
                all_rgb.append(new_rgb)
            if(grayscale):
                img_new.putpixel((w, h), convert_rgb_to_grayscale(average_rgb(all_rgb, absolute=True), strength=effect_strength))
            else:
                img_new.putpixel((w, h), average_rgb(all_rgb, absolute=True, strength=effect_strength))
            
    img_new.show()
    if save_image:
        img_new.save(img_orig.filename + " altered.png")

def apply_effect_to_rgb(rgb, filter_val):
    new_rgb = tuple(x * filter_val for x in rgb)
    return (int(new_rgb[0]), int(new_rgb[1]), int(new_rgb[2]))

def check_img_w_h():
    img_orig = Image.open('images/leaves.jpg')
    width, height = img_orig.size
    print(width, height)

def convert_rgb_to_grayscale(x, strength=1):
    total = 0
    for num in x:
        total += num

    return tuple([int(abs(total/len(x))) * strength]) * 3

def average_rgb(rgb, absolute=False, strength=1):
    r, g, b = 0, 0, 0
    for num in rgb:
        r += num[0]
        g += num[1]
        b += num[2]
    if absolute:
        return (
            abs(int(r/len(rgb))) * strength, abs(int(g/len(rgb))) * strength, abs(int(b/len(rgb)) * strength)
        )
    
    return (
        int(r/len(rgb)) * strength, int(g/len(rgb)) * strength, int(b/len(rgb) * strength)
    )


image_filter('images/Screenshot (18).png', save_image=False, grayscale=False, effect_strength=10)

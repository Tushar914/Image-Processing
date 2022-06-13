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


def image_proc(img_url):
    img_orig = Image.open(img_url)
    width, height = img_orig.size
    print("Width: ", width, " | Height: ", height)

    effect_strength = 1/128
    effect = [effect_strength] * 9
    all_rgb = []
    img_new = Image.new(mode="RGB", size=(width, height))

    for w in range(0, width):
        for h in range(0, height):
            n_list = get_pixel_neighbours(w, h)
            effect_idx = 0
            for n_pixel in n_list:
                if (n_pixel[0] >= width) or (n_pixel[1] >= height) or (n_pixel[0] <= 0) or (n_pixel[1] <= 0):
                    #print("Neighbour: ", n_pixel, " out of bounds")
                    continue
                pixel_rgb = img_orig.getpixel(n_pixel)
                new_rgb = apply_effect_to_rgb(pixel_rgb, effect[effect_idx])
                effect_idx += 1
                all_rgb.append(new_rgb)
                # if(n_pixel == (10, 10)):
                #     return
            # print("All rgb: ", average(all_rgb))
            img_new.putpixel((w, h), apply_effect_to_rgb(max(all_rgb), 1/effect_strength))
            all_rgb = []
            
    img_new.show()


def apply_effect_to_rgb(rgb, filter_val):
    new_rgb = tuple(x * filter_val for x in rgb)
    return (int(new_rgb[0]), int(new_rgb[1]), int(new_rgb[2]))

def check_img_w_h():
    img_orig = Image.open('images/leaves.jpg')
    width, height = img_orig.size
    print(width, height)

def average(rgb, absolute=False):
    r, g, b = 0, 0, 0
    for num in rgb:
        r += num[0]
        g += num[1]
        b += num[2]
    if absolute:
        return (
            abs(int(r/len(rgb))), abs(int(g/len(rgb))), abs(int(b/len(rgb)))
        )
    
    return (
        int(r/len(rgb)), int(g/len(rgb)), int(b/len(rgb))
    )


image_proc('images/Screenshot (18).png')
# image_proc('images/leaves.jpg')
#apply_effect_to_rgb((220, 110, 55), 1/9)

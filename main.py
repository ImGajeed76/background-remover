from tkinter import Tk, filedialog

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm


def equal(a, min, max):
    if (min[0] <= a[0] <= max[0]) and (min[1] <= a[1] <= max[1]) and (min[2] <= a[2] <= max[2]):
        return True
    return False


print("Please select your image...")

root = Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', True)
image_path = filedialog.askopenfile(filetypes=[('Image', '*.png')]).name

img = cv2.imread(image_path)
rows, cols, _ = img.shape
remove_color_min = [50, 50, 50]
remove_color_max = [255, 255, 255]

if input("Custom setting? (y/N): ") == "y":
    print()
    print("RGB (Separate colors with ',')")
    c_min = input("Remove color min: ").split(",")
    c_max = input("Remove color max: ").split(",")

    remove_color_min[0] = float(c_min[0])
    remove_color_min[1] = float(c_min[1])
    remove_color_min[2] = float(c_min[2])

    remove_color_max[0] = float(c_max[0])
    remove_color_max[1] = float(c_max[1])
    remove_color_max[2] = float(c_max[2])

print()
print(f"Min: {remove_color_min}")
print(f"Max: {remove_color_max}")

if img.ndim == 3:
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

first = True

for i in tqdm(range(rows)):
    for j in range(cols):
        k = img[i, j].tolist()
        if equal(k, remove_color_min, remove_color_max):
            img[i, j] = np.array([0, 0, 0, 0])

pil_img = Image.fromarray(img)
pil_img.save(f"{image_path.split('.')[0]}-bg_removed.png")
pil_img.show()

print()
print(f"saved in {image_path.split('.')[0]}-bg_removed.png")

from io import BytesIO
from PIL import ImageDraw, ImageFilter
import cairosvg
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import io
mapping = {
    0: 'Man1',
    1: 'Man2',
    2: 'Man3',
    3: 'Man4',
    4: 'Man5',
    5: 'Man6',
    6: 'Man7',
    7: 'Man8',
    8: 'Man9',
    9: 'Pin1',
    10: 'Pin2',
    11: 'Pin3',
    12: 'Pin4',
    13: 'Pin5',
    14: 'Pin6',
    15: 'Pin7',
    16: 'Pin8',
    17: 'Pin9',
    18: 'Sou1',
    19: 'Sou2',
    20: 'Sou3',
    21: 'Sou4',
    22: 'Sou5',
    23: 'Sou6',
    24: 'Sou7',
    25: 'Sou8',
    26: 'Sou9',
    27: 'Ton',
    28: 'Nan',
    29: 'Sha',
    30: 'Pei',
    31: 'Haku',
    32: 'Hatsu',
    33: 'Chun'
}
def load_tile(tile):
    """Load an image from a file (SVG or other formats) and return it as a PIL Image object."""
    row = tile // 9
    col = tile % 9
    image = Image.open("Tiles.png")
    width, height = image.size
    tile_width = width // 9
    tile_height = height // 4
    left = col * tile_width
    top = row * tile_height
    right = left + tile_width
    bottom = top + tile_height
    tile_image = image.crop((left, top, right, bottom))
    return tile_image


def load_tile1(tile, border_color='white'):
    path = "Export/Regular/" + mapping[tile] + ".png"
    img = Image.open(path)

    # Resize the image
    target_size = (60*2,80*2)
    img = img.resize(target_size)
    data = img.getdata()
    new_data = []
    for item in data:
        # Check if the pixel is black (you can adjust the threshold if needed)
        if item[0] < 50 and item[1] < 50 and item[2] < 50:
            new_data.append((240, 240, 255, item[3]))  # Replace with white
        else:
            new_data.append(item)
    img.putdata(new_data)
    # Create a new image with the border color
    border_width = 2
    bordered_width = target_size[0] + 2 * border_width
    bordered_height = target_size[1] + 2 * border_width
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    # Create an image with the border color
    bordered_img = Image.new('RGB', (bordered_width, bordered_height), color='white')

    # Paste the resized image onto the bordered image
    bordered_img.paste(img, (border_width, border_width))

    return bordered_img

def create_tile_image(tiles):
    """Create an image containing multiple tiles."""
    tile_images = [load_tile1(tile) for tile in tiles]

    # Assuming all tiles are the same size
    tile_width, tile_height = tile_images[0].size

    # Calculate the dimensions of the combined image
    num_tiles = len(tile_images)
    total_width = (tile_width) * num_tiles
    total_height = tile_height

    # Create a new image with the calculated size
    combined_image = Image.new('RGB', (total_width, total_height))

    # Paste each tile into the combined image
    for i, tile_image in enumerate(tile_images):
        combined_image.paste(tile_image, (i * (tile_width), 0))

    return combined_image






import cv2
import numpy as np


import matplotlib.pyplot as plt

def display_images_with_labels(predicted_image_path, expected_image_path):
    # Read images
    predicted_image = predicted_image_path
    expected_image = expected_image_path

    # Convert images from BGR to RGB

    # Create a figure and a set of subplots
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Display the predicted image with label
    axs[0].imshow(predicted_image)
    axs[0].set_title('Predicted')
    axs[0].axis('off')

    # Display the expected image with label
    axs[1].imshow(expected_image)
    axs[1].set_title('Expected')
    axs[1].axis('off')

    # Show the plot
    plt.show()


def tiles_to_image(predicted,expected):
    predicted_image = create_tile_image(predicted)
    expected_image = create_tile_image(expected)
    display_images_with_labels(predicted_image, expected_image)

#example_use:
#tiles = [22,33]
#tile2 = [33,22]
#tiles_to_image(tiles,tile2)
def main():
    x = input("give us your tiles:")
    create_tile_image(x)
if __name__ == "__main__":
    main()


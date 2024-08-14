from PIL import Image
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
    29: 'Shaa',
    30: 'Pei',
    31: 'Haku',
    32: 'Hatsu',
    33: 'Chun'
}

def load_tile1(tile, border_color='white'):
    path = "Export/Regular/" + mapping[tile] + ".png"
    img = Image.open(path)
    target_size = (60 * 2, 80 * 2)
    img = img.resize(target_size)
    border_width = 2
    background = Image.new('RGBA', (target_size[0] + 2 * border_width, target_size[1] + 2 * border_width),
                           color=border_color)
    if img.mode == 'RGBA':
        background.paste(img, (border_width, border_width), img)
    else:
        img = img.convert('RGBA')
        background.paste(img, (border_width, border_width))
    final_img = background.convert('RGB')
    return final_img

def create_tile_image(tiles):
    """Create an image containing multiple tiles."""
    tile_images = [load_tile1(tile) for tile in tiles]
    tile_width, tile_height = tile_images[0].size
    num_tiles = len(tile_images)
    total_width = (tile_width) * num_tiles
    total_height = tile_height
    combined_image = Image.new('RGB', (total_width, total_height))
    for i, tile_image in enumerate(tile_images):
        combined_image.paste(tile_image, (i * (tile_width), 0))
    return combined_image
import matplotlib.pyplot as plt

def display_images_with_labels(predicted_image_path, expected_image_path):
    predicted_image = predicted_image_path
    expected_image = expected_image_path
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(predicted_image)
    axs[0].set_title('Predicted')
    axs[0].axis('off')
    axs[1].imshow(expected_image)
    axs[1].set_title('Expected')
    axs[1].axis('off')
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


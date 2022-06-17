import glob
from PIL import Image
import numpy as np
from scipy import spatial


main_image_path = "main_photo_2.jpg"
tile_photos_path = "tiles/**"
tile_size = (50, 50)

tile_paths = []
for file in glob.glob(tile_photos_path):
    tile_paths.append(file)

tiles = []
for path in tile_paths:
    tile = Image.open(path)
    tile = tile.resize(tile_size)
    tiles.append(tile)

colors = []
for tile in tiles:
    mean_color = np.array(tile).mean(axis=0).mean(axis=0)
    colors.append(mean_color)

main_photo = Image.open(main_image_path)

width = int(np.round(main_photo.size[0] / tile_size[0]))
height = int(np.round(main_photo.size[1] / tile_size[1]))

resized_photo = main_photo.resize((width, height))

tree = spatial.KDTree(colors)

closest_tiles = np.zeros((width, height), dtype=np.uint32)

for i in range(width):
    for j in range(height):
        pixel = resized_photo.getpixel((i, j))
        closest = tree.query(pixel)
        closest_tiles[i, j] = closest[1]

output = Image.new('RGB', main_photo.size)

for i in range(width):
    for j in range(height):
        x, y = i*tile_size[0], j* tile_size[1]
        index = closest_tiles[i, j]
        output.paste(tiles[index], (x, y))

output.save('output.jpg')
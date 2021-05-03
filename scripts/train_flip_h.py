import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import glob
import pathlib

data_dir = pathlib.Path('images/')

image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)


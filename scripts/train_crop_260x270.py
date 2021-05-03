"""This module implements data feeding and training loop to create model
to classify X-Ray chest images as a lab example for BSU students.
"""

__author__ = 'Alexander Soroka, soroka.a.m@gmail.com'
__copyright__ = """Copyright 2020 Alexander Soroka"""


import argparse
import glob
import numpy as np
import tensorflow as tf
import time
from tensorflow.python import keras as keras
from tensorflow.python.keras.callbacks import LearningRateScheduler
from tensorflow.keras.applications import EfficientNetB0

# Avoid greedy memory allocation to allow shared GPU usage
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
  tf.config.experimental.set_memory_growth(gpu, True)


LOG_DIR = 'logs'
BATCH_SIZE = 32
NUM_CLASSES = 101
RESIZE_TO = 224
TRAIN_SIZE = 101000
SCALE_TO_W = 260
SCALE_TO_H = 270

def parse_proto_example(proto):
  keys_to_features = {
    'image/encoded': tf.io.FixedLenFeature((), tf.string, default_value=''),
    'image/label': tf.io.FixedLenFeature([], tf.int64, default_value=tf.zeros([], dtype=tf.int64))
  }
  example = tf.io.parse_single_example(proto, keys_to_features)
  example['image'] = tf.image.decode_jpeg(example['image/encoded'], channels=3)
  example['image'] = tf.image.convert_image_dtype(example['image'], dtype=tf.uint8)
  example['image'] = tf.image.resize(example['image'], tf.constant([SCALE_TO_W, SCALE_TO_H]))
  return example['image'], tf.one_hot(example['image/label'], depth=NUM_CLASSES)
  
  
def create_dataset(filenames, batch_size):
  """Create dataset from tfrecords file
  :tfrecords_files: Mask to collect tfrecords file of dataset
  :returns: tf.data.Dataset
  """
  return tf.data.TFRecordDataset(filenames)\
    .map(parse_proto_example, num_parallel_calls=tf.data.AUTOTUNE)\
    .batch(batch_size)\
    .prefetch(tf.data.AUTOTUNE)


def build_model():
  inputs = tf.keras.Input(shape=(SCALE_TO_W, SCALE_TO_H, 3))
  x = tf.keras.layers.experimental.preprocessing.RandomCrop(RESIZE_TO, RESIZE_TO)(inputs)
  x = EfficientNetB0(include_top=False, input_tensor = x, pooling ='avg', weights='imagenet')
  x.trainable = False
  x = tf.keras.layers.Flatten()(x.output)
  outputs = tf.keras.layers.Dense(NUM_CLASSES, activation=tf.keras.activations.softmax)(x)
  return tf.keras.Model(inputs=inputs, outputs=outputs)


def main():
  args = argparse.ArgumentParser()
  args.add_argument('--train', type=str, help='Glob pattern to collect train tfrecord files, use single quote to escape *')
  args = args.parse_args()

  dataset = create_dataset(glob.glob(args.train), BATCH_SIZE)
  train_size = int(TRAIN_SIZE * 0.7 / BATCH_SIZE)
  train_dataset = dataset.take(train_size)
  validation_dataset = dataset.skip(train_size)

  model = build_model()

  initial_rate = 0.001
  first_decay_steps = 5000
  t_mul = 2.0
  m_mul = 0.75

  learning_rate_CDWR = tf.keras.experimental.CosineDecayRestarts(initial_rate, first_decay_steps, t_mul, m_mul)

  model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=learning_rate_CDWR),
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=[tf.keras.metrics.categorical_accuracy],
  )

  log_dir='{}/f101-{}'.format(LOG_DIR, time.time())
  model.fit(
    train_dataset,
    epochs=22,
    validation_data=validation_dataset,
    callbacks=[
      tf.keras.callbacks.TensorBoard(log_dir)
    ]
  )


if __name__ == '__main__':
    main()

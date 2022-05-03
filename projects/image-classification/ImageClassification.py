import os
import tensorflow as tf

assert tf.__version__.startswith('2')
from tflite_model_maker import image_classifier
from tflite_model_maker.image_classifier import DataLoader

image_path = tf.keras.utils.get_file(
    'flower_photos.tgz',
    'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
    extract=True)
image_path = os.path.join(os.path.dirname(image_path), 'flower_photos')

# 查看数据集下载位置
# /home/server/.keras/datasets/flower_photos
print(image_path)

data = DataLoader.from_folder(image_path)
train_data, test_data = data.split(0.9)

model = image_classifier.create(train_data)

loss, accuracy = model.evaluate(test_data)

# 导出模型在当前目录下：model.tflite
model.export(export_dir='.')

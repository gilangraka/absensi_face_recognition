import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Memuat model yang telah disimpan
model = tf.keras.models.load_model('trained_mahasiswa.keras')

# Persiapan data uji
test_datagen = ImageDataGenerator(
    rescale = 1./225,
    rotation_range = 20,
    horizontal_flip = True,
    shear_range = 0.2,
    fill_mode = 'nearest')

test_generator = test_datagen.flow_from_directory(
    'data_mhs/val',  # Ubah ini ke direktori data uji Anda
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

# Melakukan prediksi pada data uji
test_loss, test_accuracy = model.evaluate(test_generator, steps=5)
print(f'Test accuracy: {test_accuracy}')

# Melakukan prediksi pada satu gambar
img_path = 'FotoGilang.jpg'  # Ubah ini ke path gambar Anda
img = tf.keras.preprocessing.image.load_img(img_path, target_size=(150, 150))
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 225.0

prediction = model.predict(img_array)
predicted_class = np.argmax(prediction)

list_dir = os.listdir('data_mhs')
nim = list_dir[predicted_class]

print(f'The predicted class is: {predicted_class}')

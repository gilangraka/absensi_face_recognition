import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os
import shutil

list_dir = os.listdir('data_mhs')
base_dir = 'data_mhs'

train_dir = os.path.join(base_dir, 'train')
val_dir   = os.path.join(base_dir, 'val')

if not os.path.exists(train_dir):
    os.mkdir(train_dir)
if not os.path.exists(val_dir):
    os.mkdir(val_dir)


data_dir = {}
train_x_dir = {}
val_x_dir = {}
train_x = {}
val_x = {}
for i in list_dir:
    if(i == 'val' or i == 'train'):
        continue
    data_dir[i] = os.path.join(base_dir, i)
    train_x_dir[i], val_x_dir[i] = train_test_split(os.listdir(data_dir[i]), test_size=0.2)
    train_x[i] = os.path.join(train_dir, i)
    val_x[i] = os.path.join(val_dir, i)
    if not os.path.exists(train_x[i]) :
        os.mkdir(train_x[i])
    if not os.path.exists(val_x[i]) :
        os.mkdir(val_x[i])

    for k in train_x_dir[i]:
        shutil.copy(os.path.join(data_dir[i], k), os.path.join(train_x[i],k))
    for k in val_x_dir[i]:
        shutil.copy(os.path.join(data_dir[i],k), os.path.join(val_x[i],k))
    
train_datagen = ImageDataGenerator(
    rescale = 1./255,
    rotation_range = 20,
    horizontal_flip = True,
    shear_range = 0.2,
    fill_mode = 'nearest')

test_datagen = ImageDataGenerator(
    rescale = 1./255,
    rotation_range = 20,
    horizontal_flip = True,
    shear_range = 0.2,
    fill_mode = 'nearest')

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size =(150,150),
    batch_size = 32,
    class_mode = 'categorical'
)

validation_generator = test_datagen.flow_from_directory(
    val_dir,
    target_size = (150,150),
    batch_size = 32,
    class_mode = 'categorical'
)

# membuat model
model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(32, (3,3), activation = 'relu', input_shape= (150,150,3)),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(64,(3,3), activation= 'relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(128,(3,3), activation= 'relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(256,(3,3), activation= 'relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(512, activation= 'relu'),
  tf.keras.layers.Dense(len(os.listdir(train_dir)), activation= 'softmax'),
  tf.keras.layers.Dropout(0.5)
])

model.compile(loss = 'categorical_crossentropy',
              optimizer = tf.optimizers.Adam(),
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    steps_per_epoch = 25,
    epochs = 20,
    validation_data = validation_generator,
    validation_steps = 5,
    verbose=2
)

model.save('trained_mahasiswa.keras')
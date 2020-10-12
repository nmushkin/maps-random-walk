import os
from random import shuffle, choice

from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing import image_dataset_from_directory
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.experimental.preprocessing import RandomFlip, RandomRotation
from keras.layers.experimental.preprocessing import Rescaling
from keras.layers.normalization import BatchNormalization
from keras.layers import Dense, Dropout, Flatten, MaxPooling2D, Conv2D
from keras.losses import SparseCategoricalCrossentropy
import matplotlib.pyplot as plt

# from PIL import Image
# import numpy as np

IMAGE_SIZE = 200
IMAGE_DIR = './data/images'
TEST_DIR = './data/test_images'
TRAIN_SAMPLES = 500

def load_dataset():
    batch_size = 32
    
    image_generator = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.4,
        height_shift_range=0.4,
        zoom_range=0.4,
        horizontal_flip=True,
        validation_split=0.2
    )
    val_generator = ImageDataGenerator(
        validation_split=0.1
    )
    train_ds = image_generator.flow_from_directory(
        IMAGE_DIR,
        target_size=(200, 200),
        color_mode="grayscale",
        class_mode="categorical",
        batch_size=batch_size,
        shuffle=True,
        subset="training",
        seed=2,
        interpolation="nearest",
    )
    val_ds = val_generator.flow_from_directory(
        IMAGE_DIR,
        target_size=(200, 200),
        color_mode="grayscale",
        class_mode="categorical",
        batch_size=batch_size,
        subset="validation",
        shuffle=True,
        seed=2,
        interpolation="nearest",
    )
    
    # plt.figure(figsize=(10, 10))
    # for images, _ in train_ds.take(1):
    #     for i in range(9):
    #         # augmented_images = data_augmentation(images)
    #         ax = plt.subplot(3, 3, i + 1)
    #         # plt.imshow(augmented_images[0].numpy().astype("uint8"))
    #         plt.imshow(images[i].numpy().astype("uint8"))
    #         plt.axis("off")
    # plt.show()
    # print(train_ds.class_names)
    return (train_ds, val_ds)

def get_model():
    model = Sequential([
        # Rescaling(1./255),
        Conv2D(64, (3, 3), activation='relu', input_shape=(IMAGE_SIZE, IMAGE_SIZE, 1)),
        BatchNormalization(momentum=.8),
        MaxPooling2D(pool_size=(2, 2), strides=(2,2)),
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(momentum=.8),
        MaxPooling2D(pool_size=(2, 2), strides=(2,2)),
        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(momentum=.8),
        MaxPooling2D(pool_size=(2, 2), strides=(2,2)),
        Flatten(),
        Dense(16, activation='relu'),
        Dropout(0.5),
        Dense(2, activation='softmax'),
    ])
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy'],
    )
    return model


def train_save_model():
    print('Loading Data')
    train, val = load_dataset()
    print(train.classes)
    print("Creating model")
    model = get_model()
    print("Model Summary")
    print(model.summary())
    print("Fitting model")
    steps_train = train.n // train.batch_size
    steps_val = val.n // val.batch_size
    history = model.fit(train, validation_data=val, epochs=50, verbose=1, steps_per_epoch=steps_train, validation_steps=steps_val)
    print("Saving model")
    model.save("cam_model_7.h5")
    plot_model_history(history)

def plot_model_history(history):
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    # plt.ylim([0.5, 1])
    plt.legend(loc='lower right')
    plt.show()


# def get_vec_label(name):
# if name == 'cameras':
#     return np.array([1, 0])
# else:
#     return np.array([0, 1])

# def gray_rsz_image(path):
#     img = Image.open(path)
#     img = img.convert('L')
#     img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
#     return img

# def load_images():
#     print('loading images...')
#     training_data = []
#     dirs = next(os.walk(IMAGE_DIR))[1]
#     for dirname in dirs:
#         dir_path = os.path.join(IMAGE_DIR, dirname)
#         print(dir_path)
#         filenames = next(os.walk(dir_path))[2]
#         print(len(filenames))
#         label = get_vec_label(dirname)
#         for im in range(TRAIN_SAMPLES):
#             image_name = choice(filenames)
#             full_path = os.path.join(dir_path, image_name)
#             if "DS_Store" in full_path:
#                 continue
#             img = gray_rsz_image(full_path)
#             training_data.append([np.array(img), label])

#     return training_data

# def label_images(model, paths):
#     images = np.array([np.array(gray_rsz_image(path)) for path in paths])
#     input_arrays = images.reshape(-1, IMAGE_SIZE, IMAGE_SIZE, 1)
#     labels = model.predict(input_arrays)
#     return labels

# def test_model():
#     model = load_model('cam_model_3.h5')
#     real_labels = []
#     predicted_labels = []
#     paths = []
#     dirs = next(os.walk(TEST_DIR))[1]
#     for dirname in dirs:
#         dir_path = os.path.join(TEST_DIR, dirname)
#         print(dir_path)
#         filenames = next(os.walk(dir_path))[2]
#         full_paths = [os.path.join(dir_path, f) for f in filenames]
#         if len(full_paths) > 0:
#             paths.extend(full_paths)
#             label = get_vec_label(dirname)
#             real_labels.extend([label] * len(full_paths))
#             model_labels = label_images(model, full_paths)
#             predicted_labels.extend(model_labels)
#     predicted_labels = np.array(np.round(predicted_labels))
#     print(paths)
#     print(real_labels)
#     print(predicted_labels)

# load_dataset()
# train_save_model()
# test_model()

import tensorflow as tf
import os

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from tensorflow.keras.layers.experimental.preprocessing import RandomFlip
from tensorflow.keras.layers.experimental.preprocessing import RandomRotation
from tensorflow.keras.layers.experimental.preprocessing import RandomZoom
from tensorflow.keras.layers import Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import matplotlib.pyplot as plt
import numpy as np

filters = {
    "-blur2.jpg": " -blur 2 ",
    "-blur5.jpg": " -blur 5 ",
    "-contrast.jpg": " +contrast +contrast +contrast +contrast +contrast ",
    "-laplacian.jpg": " +noise laplacian +noise laplacian ",
    # "-multiplicative.jpg": " +noise multiplicative +noise multiplicative ",
    # "-poisson.jpg": " +noise poisson +noise poisson "
}

model = Sequential()

class_names = ['AUT-B-', 'AUT-BO', 'BEL-BO', 'BGR-BO', 'CYP-BO', 'CZE-BO', 'DEU-BO', 'DEU-BP', 'ESP-BO', 'EST-BO', 'FIN-BO', 'FIN-BP', 'FRA-BO', 'GRC-BO', 'GRC-BS', 'HRV-BO', 'HUN-BO', 'HUN-BP', 'ITA-BO', 'LTU-BO', 'LUX-BO', 'LVA-BO', 'MLT-BO', 'NLD-BO', 'POL-BF', 'POL-BO', 'PRT-BO', 'ROU-BO', 'ROU-BP', 'SVK-BO', 'SWE-BO']
epochs = 5


def main():
    train_ds = tf.keras.preprocessing.image_dataset_from_directory("new_img_2",
                                                                   validation_split=0.2,
                                                                   subset="training",
                                                                   seed=123,
                                                                   image_size=(220, 154),
                                                                   batch_size=32)

    validation_ds = tf.keras.preprocessing.image_dataset_from_directory("new_img_2",
                                                                   validation_split=0.2,
                                                                   subset="validation",
                                                                   seed=123,
                                                                   image_size=(220, 154),
                                                                   batch_size=32)

    # print(train_ds)
    global class_names
    class_names = train_ds.class_names
    print(class_names)
    class_names = validation_ds.class_names
    print(class_names)

    AUTOTUNE = tf.data.experimental.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    validation_ds = validation_ds.cache().prefetch(buffer_size=AUTOTUNE)

    num_classes = len(class_names)

    no_of_filters = 64
    size_of_filters3 = (3, 3)
    size_of_pool = (2, 2)
    no_of_node = 512

    global model
    model = Sequential()
    # model.add(data_augmentation)
    # model.add(RandomFlip("horizontal",
    #                              input_shape=(220,154,3))),
    # model.add(RandomRotation(0.1))
    model.add(Rescaling(1./255, input_shape=(220, 154, 3)))
    # model.add(RandomFlip("horizontal", input_shape=(220,154,3)))
    # model.add(RandomRotation(0.1))
    # model.add(RandomZoom(0.1))

    model.add((Conv2D(no_of_filters, size_of_filters3, input_shape=(220, 154, 3),
                      activation="relu")))
    model.add((Conv2D(no_of_filters, size_of_filters3, activation="relu")))
    model.add(MaxPooling2D(pool_size=size_of_pool))
    model.add((Conv2D(no_of_filters, size_of_filters3, activation="relu")))
    model.add(MaxPooling2D(pool_size=size_of_pool))
    model.add((Conv2D(no_of_filters, size_of_filters3, activation="relu")))
    model.add(MaxPooling2D(pool_size=size_of_pool))

    model.add(Flatten())
    model.add(Dense(no_of_node, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation="softmax"))
    model.compile(
        loss = tf.keras.losses.SparseCategoricalCrossentropy(),
        optimizer='Adam',

        metrics=['accuracy']
    )
    # model.compile(Adam(lr=0.001), loss="categorical_crossentropy", metrics=["accuracy"])

    model.summary()
    history = model.fit(
        train_ds,
        validation_data=validation_ds,
        batch_size=16,
        epochs=epochs
    )

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

    model.save("dokumenciki" + str(epochs))


def predict():

    print("Loading model")
    reconstructed_model = tf.keras.models.load_model("dokumenciki" + str(epochs))

    print("Prediction:")
    # TODO jak wyciągnąć class_names z zapisanego modelu
    my_array = np.zeros((len(class_names), len(class_names)))
    my_true_counter = np.zeros((1, len(class_names)))

    subfolders = os.listdir("new_img_2")
    print(subfolders)
    for subfolder in subfolders:
        imgs = os.listdir(os.path.join("new_img_2", subfolder))
        for img in imgs:
            id_path = os.path.join("new_img_2", subfolder, img)
            print(id_path)
            im = tf.keras.preprocessing.image.load_img(
                id_path, target_size=(220, 154)
            )
            # print(img)

            img_array = tf.keras.preprocessing.image.img_to_array(im)
            img_array = tf.expand_dims(img_array, 0) # Create a batch
            # class_index = int(model.predict_classes(img_array))
            # print(model.predict_classes(img_array), class_index)
            predictions = reconstructed_model.predict(img_array)
            score = tf.nn.softmax(predictions[0])
            print(np.amax(predictions), np.argmax(predictions))

            my_array[np.argmax(predictions)][class_names.index(img[:6])] += 1
            my_true_counter[0, class_names.index(img[:6])] += 1

            print(im,
                  "This image most likely belongs to {} with a {:.2f} percent confidence."
                  .format(class_names[np.argmax(score)], 100 * np.amax(predictions))
                  )

    print(my_array.sum())
    print(my_array)
    for i in range(my_array.shape[0]):
        my_array[i, :] /= my_true_counter[0, i]
    print(my_array)

    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(len(class_names)), labels = class_names)
    ax.set_yticks(np.arange(len(class_names)), labels = class_names)
    im = ax.imshow(my_array, cmap='hot')
    plt.show()

def predict2():
    reconstructed_model = tf.keras.models.load_model("dokumenciki" + str(epochs))

    imgs = [
        ('tumulec.png', tf.keras.preprocessing.image.load_img("tumulec.png", target_size=(220, 154))),
        ('gogos.jpg', tf.keras.preprocessing.image.load_img("gogos.jpg", target_size=(220, 154))),
        ('fikus.jpg', tf.keras.preprocessing.image.load_img("fikus.jpg", target_size=(220, 154))),
        ('julka.jpg', tf.keras.preprocessing.image.load_img("julka.jpg", target_size=(220, 154))),
    ]

    for im in imgs:
        img_array = tf.keras.preprocessing.image.img_to_array(im[1])
        img_array = tf.expand_dims(img_array, 0) # Create a batch
        # class_index = int(model.predict_classes(img_array))
        # print(model.predict_classes(img_array), class_index)
        predictions = reconstructed_model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        print(np.amax(predictions), np.argmax(predictions))
        print(
            "Image {} most likely belongs to {} with a {:.2f} percent confidence."
            .format(im[0], class_names[np.argmax(score)], 100 * np.amax(predictions))
            )

        # for i, pr in enumerate(predictions[0]):
        #     print(f"{i} - {pr*100:.2f}")

def apply_filters():
    main_src_folder = "new_img_2"
    convert = "C:\Programy\ImageMagick-7.1.0-Q16-HDRI\convert "
    folders = os.listdir(main_src_folder)
    for folder in folders:
        print("FOLDER", folder)
        images = os.listdir(os.path.join(main_src_folder, str(folder)))
        for image in images:
            current_file_path = os.path.join(main_src_folder, folder, image)
            print(current_file_path)
            for k, v in filters.items():
                os.system(convert + current_file_path + v + current_file_path.replace(".jpg", k))


if __name__ == '__main__':
    # apply_filters()
    # main()
    # predict()
    predict2()
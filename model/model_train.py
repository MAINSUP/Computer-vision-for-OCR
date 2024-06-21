import os
import click
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras import layers

IMG_HEIGHT = 180
IMG_WIDTH = 180
BATCH_SIZE = 32
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--epochs", "-e", multiple=False, default=200)
@click.argument('foldername', type=click.Path(exists=True))
def main(foldername, epochs):
    """
    Basic usage of model_train is as follows:
    madel_train.py -e 100 PATH,
    where -e defines the number of training epochs (default is 200),
    PATH is the path to the training images folder.
    Folder should contain subfolders of each class. Names of those
    subfolders will define class names in the resulting dataset.
    Sourced images will be split for training & validation with ratio 80/20%.
    """
    train_ds, val_ds, num_classes = make_dataset(foldername)
    model = build_model(num_classes)
    history = model_train(model, train_ds, val_ds, epochs)
    plot_loss(history, '', 0)


def make_dataset(foldername):
    # getting images and building datasets for training and validation
    train_ds = keras.utils.image_dataset_from_directory(
        directory=foldername,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE)

    val_ds = keras.utils.image_dataset_from_directory(
        directory=foldername,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE)
    class_names = train_ds.class_names
    num_classes = len(class_names)
    print("Clas names:", class_names)

    # plotting few pictures from dataset
    plt.figure(figsize=(10, 10))
    for images, labels in train_ds.take(1):
        for i in range(9):
            plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.suptitle("Training dataset examples", fontsize=20)
            plt.axis("off")
    # dataset processing optimization
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    return train_ds, val_ds, num_classes


def build_model(num_classes):
    # for a better feature extraction, there are few image processing techniques are used
    data_augmentation = keras.Sequential([
        # layers.RandomFlip("horizontal"),  # not in use
        # layers.RandomRotation(0.2),    # not in use
        layers.RandomZoom(  # random image zoom
            height_factor=0.25,
            width_factor=0.15,
            fill_mode='reflect',
            interpolation='bilinear',
            seed=None,
            fill_value=0.0),
        layers.RandomTranslation(height_factor=0.2, width_factor=0.2)  # random image translation
    ])
    # typical CNN neural network with data rescaling and augmentation layers
    model = keras.Sequential([
        layers.Rescaling(1. / 255),
        data_augmentation,
        layers.Conv2D(128, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(512, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(),
        layers.Conv2D(512, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(),
        layers.Dropout(0.3),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),

        layers.Dense(num_classes)
    ])
    # defining optimizer function
    model.compile(
        optimizer='adam',
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])

    model.build((None, IMG_HEIGHT, IMG_WIDTH, 3))
    model.summary()
    return model


def model_train(model, train_ds, val_ds, epochs):
    model_file = os.path.join(os.getcwd(), 'best_weights')
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss',          # early stopping method
                                               patience=20,                 # is used to avoid not improving
                                               restore_best_weights=False)  # training epochs.

    checkpoint = keras.callbacks.ModelCheckpoint(model_file,                      # checkpoint, in its turn
                                                 monitor="val_loss", mode="min",  # allows saving best weights
                                                 save_best_only=True, verbose=1)  # irrespective to early stopping call
    # training the model
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[early_stop, checkpoint]
    )
    # loading the best weights obtained at defined checkpoint
    model.load_weights(model_file)
    # saving model to disk
    model.save(os.getcwd())
    return history


def plot_loss(history, label, n):
    plt.rcParams['figure.figsize'] = (12, 5)
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    # Use a log scale on y-axis to show the wide range of values.
    plt.plot(history.epoch, history.history['loss'],
             color=colors[n], label='Training' + label)
    plt.plot(history.epoch, history.history['val_loss'],
             color=colors[n], label='Validation' + label,
             linestyle="--")
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()


if __name__ == '__main__':
    main()

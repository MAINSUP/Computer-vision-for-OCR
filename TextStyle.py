import keras
import os
import numpy as np
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')


def text_style(segment, confidence):
    class_names = ['Cursive', 'Print']
    img_height = 100
    img_width = 600
    model = keras.models.load_model(os.getcwd())
    probability_model = keras.Sequential([model, keras.layers.Softmax()])
    segment = tf.convert_to_tensor(segment)
    input_tensor = tf.image.resize(segment, [img_height, img_width])
    predictions = probability_model.predict(tf.expand_dims(input_tensor, axis=0))
    np.argmax(predictions)
    probability = np.max(predictions)
    if probability < confidence:
        return class_names[np.argmin(predictions)]
    else:
        return class_names[np.argmax(predictions)]

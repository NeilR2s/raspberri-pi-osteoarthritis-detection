import tensorflow as tf
from tensorflow import keras
from tensorflow import dtypes
import cv2 as cv
import numpy as np

def predict(image_dir: str ):

    DEFAULT_FUNCTION_KEY = 'serving_default'
    model = tf.saved_model.load('cnn-arthritis/my_model')
    inference_func = model.signatures[DEFAULT_FUNCTION_KEY]

    image_shape = (224,224)
    image = cv.imread(image_dir)
    tensor = tf.convert_to_tensor(image, dtype=dtypes.float32)
    # resized_image = cv.resize(src = image, dsize= image_shape, interpolation=1)
    prediction = inference_func(tensor)
    prediction_label = np.argmax(prediction['dense_17'])
    prediction_label_encoded = int(prediction_label)

    if prediction_label_encoded == 0 or prediction_label_encoded == 1:
        message = 'The xray belongs to KL category 0-1. The xray shows no (or doubtful) evidence of osteoarthritis.'

    if prediction_label_encoded == 2:
        message = 'The xray belongs to KL category 2. The xray shows definite osteophytes, more noticeable bone spurs, and possible joint narrowing.'

    if prediction_label_encoded == 3 :
        message = 'The xray belongs to KL category 3-4. The xray shows large osteophytes, and clear narrowing of the joint space.'


    return message



print(predict('cnn-arthritis/auto_test/2/9988921_1.png')) # category 2
print(predict('cnn-arthritis/auto_test/3/9952664_1.png')) # category 3
print(predict('cnn-arthritis/auto_test/4/9541124_2.jpg')) # category 4



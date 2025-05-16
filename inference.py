import tensorflow as tf
from tensorflow import keras
from tensorflow import dtypes
import cv2 as cv
import numpy as np
import os
import cv2


DEFAULT_FUNCTION_KEY = 'serving_default'
MODEL_PATH = 'tf-osteo' 


    
try:
    model: tf.saved_model = tf.saved_model.load(MODEL_PATH)
    inference_func = model.signatures[DEFAULT_FUNCTION_KEY]
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model from {MODEL_PATH}: {e}")
    inference_func = None

def predict(image_dir: str ):
    
    image_shape = (224,224)

    if not os.path.exists(image_dir):
        return f"Error: Image file not found at {image_dir}"

    image = cv.imread(image_dir)

    if image is None:
        return f"Error: Could not read image from {image_dir}"
    

    image_rgb = cv.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv.resize(src=image_rgb, dsize=image_shape, interpolation=cv.INTER_LINEAR) 
    tensor = tf.convert_to_tensor(resized_image, dtype=dtypes.float32)
    tensor_batch = tf.expand_dims(tensor, axis=0)
    preprocessed_tensor = tf.keras.applications.mobilenet_v3.preprocess_input(tensor_batch)

    try:
        prediction = inference_func(preprocessed_tensor)
        print(f'Prediction Keys: {prediction.keys()}')

        prediction_output = prediction['dense_1']

        prediction_label = np.argmax(prediction_output.numpy(), axis=1)[0] # Convert tensor to numpy for argmax

        prediction_label_encoded = int(prediction_label)

        if prediction_label_encoded == 0:
            message = 'The thermal image belongs to KL category 0. The image shows no (or doubtful) evidence of osteoarthritis.'
        elif prediction_label_encoded == 1:
            message = 'The thermal image belongs to KL category 1. The image shows doubtful evidence of osteoarthritis'        
        elif prediction_label_encoded == 2:
            message = 'The thermal image belongs to KL category 2. The image shows some evidence of osteoarthritis'
        elif prediction_label_encoded == 3:
            message = 'The thermal image belongs to KL category 3. The image shows definite signs of osteoarthritis.'
        else:
            message = f'Unexpected prediction label: {prediction_label_encoded}'

        return message

    except Exception as e:
        return f"Error during inference: {e}"

if __name__ == '__main__':
    
    while True:
        try:
            image_directory = str(input('Enter the directory of the image you want to predict: '))
            result = predict(image_directory)
            print(result)
        except Exception as e:
            print(f'Error running inference on the model. Ensure the directories are correct {e}')

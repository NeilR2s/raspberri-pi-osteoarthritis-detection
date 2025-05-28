import os
import logging 
import numpy as np
import tensorflow as tf
from tensorflow import dtypes
import cv2

logger = logging.getLogger(__name__) 
logging.basicConfig(level=logging.DEBUG)

MODEL_PATH:str = "tf-osteo.keras"
# DEFAULT_FUNCTION_KEY = "serving_default" 
    
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    # inference_func = model.signatures[DEFAULT_FUNCTION_KEY]
    logger.info(f"Model loaded successfully from {MODEL_PATH}")

except Exception as e:
    logger.error(f"Error loading model from {MODEL_PATH}: {e}")

def predict(image_dir: str ):
    """
    Preprocesses image to desired tensor shape, then runs inference. Output is decoded using argmax.
    Args:
        - image_dir (str): a string referencing a valid directory pointing to a thermal image of a knee
    Returns:
        - a dict[str,str] object containing KL information about the image
    Exceptions:
        - ValueError: exceptions for failures in file handling (most likely a relative directory issue)
        - Exception: general exception for unexpected errors (most likely tensor shape errors)
    """
    image_shape = (224,224)

    if not os.path.exists(image_dir):
        raise ValueError(f"Error: Image file not found at {image_dir}")

    image = cv2.imread(image_dir)

    if image is None:
        raise ValueError(f"Error: Could not read image from {image_dir}")
    

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    resized_image = cv2.resize(src=image_rgb, dsize=image_shape, interpolation=cv2.INTER_LINEAR) 
    logger.info(f"Input image shape: {tf.shape(resized_image)}")
    tensor = tf.convert_to_tensor(resized_image, dtype=dtypes.float32)
    logger.info(f"Input tensor shape: {tf.shape(tensor)}")
    tensor_batch = tf.expand_dims(tensor, axis=0)
    logger.info(f"Preprocessed tensor shape: {tf.shape(tensor_batch)}")
    preprocessed_tensor = tf.keras.applications.mobilenet_v3.preprocess_input(tensor_batch)

    try:
        prediction = model.predict(preprocessed_tensor)
        logger.debug(f"Prediction Keys: {prediction}")
        prediction_label = np.argmax(prediction, axis=1)[0] 

        prediction_label_encoded = prediction_label

        if prediction_label_encoded == 0:
            message = "The thermal image belongs to KL category 0. The image shows no (or doubtful) evidence of osteoarthritis."
        elif prediction_label_encoded == 1:
            message = "The thermal image belongs to KL category 1. The image shows doubtful evidence of osteoarthritis"        
        elif prediction_label_encoded == 2:
            message = "The thermal image belongs to KL category 2. The image shows some evidence of osteoarthritis"
        elif prediction_label_encoded == 3:
            message = "The thermal image belongs to KL category 3. The image shows definite signs of osteoarthritis."
        else:
            message = f"Unexpected prediction label: {prediction_label_encoded}"

        return {str(prediction_label_encoded):message} 

    except ValueError as ve:
        return ve

    except Exception as e:
        return f"Error during inference: {e}"

if __name__ == "__main__":
    
    while True:
        try:
            image_directory = str(input("Enter the directory of the image you want to predict: "))
            result = predict(image_directory)
            print(result)
        except Exception as e:
            print(f"Error running inference on the model. Ensure the directories are correct {e}")

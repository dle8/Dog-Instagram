from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from tqdm import tqdm
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

# define ResNet50 model
ResNet50_mod = ResNet50(weights='imagenet')


def expand_tensor(img):
    # Convert image type to 3D tensor
    x = image.img_to_array(img)
    # Convert 3D tensor to 4D tensor and return
    return np.expand_dims(x, axis=0)


def resNet50_predict_labels(img_path):
    # returns prediction vector for image located at img_path
    img = preprocess_input(expand_tensor(img_path))
    return np.argmax(ResNet50_mod.predict(img))


def dog_included(img_path):
    prediction = resNet50_predict_labels(img_path)
    return (prediction <= 268) & (prediction >= 151)

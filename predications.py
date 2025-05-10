import tensorflow as tf 
import numpy as np 
import os 
import io
from google import genai
from PIL import Image,ImageDraw
from google.genai import types
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from api import *
client = genai.Client(api_key="AIzaSyCjO937NhE9WdRlwoG3r3ACqDOzcVBEFJw")


def tumor(contents,model,loc):
    image = tf.keras.preprocessing.image.load_img(io.BytesIO(contents),target_size=(299,299))
    img = Image.open(f"saved_images\{loc}")
    image =  tf.keras.preprocessing.image.img_to_array(image)
    image  = np.expand_dims(image,axis=0)
    image = image/255
    pred = model.predict(image)
    pred = np.argmax(pred)
    if pred == 0:
        tu = "glioma"
    elif pred == 1:
        tu = "meningioma"
        
    elif pred == 2:
        tu = "no_tumor"
    else: 
        tu = "pituitary"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents= [img,f"Tumor Type:{tu}"],
        config=types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.1,system_instruction="You are a radiologist that need to genrate a report for the given type of tumor "
            )

        )
    save_grid(f"saved_images\{loc}","grid_imt.jpg")
    save_pdf(response.text,"grid_imt.jpg","tumor.pdf")

def alz(contents,model,loc):
    image = tf.keras.preprocessing.image.load_img(io.BytesIO(contents),target_size=(299,299))
    img = Image.open(f"saved_images\{loc}")
    image =  tf.keras.preprocessing.image.img_to_array(image)
    image  = np.expand_dims(image,axis=0)
    image = image/255
    pred = model.predict(image)
    pred = np.argmax(pred)
    if pred == 0:
        tu = "mild demented"
    elif pred == 1:
        tu = "moderate demented"
        
    elif pred == 2:
        tu = "non demented"
    else: 
        tu = "very mild demented"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents= [img,f"alzhimer type:{tu}"],
        config=types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.1,system_instruction="You are a radiologist that need to genrate a report for the given type of alzhimer "
            )

        )
    save_grid(f"saved_images\{loc}","grid_imga.jpg")
    save_pdf(response.text,"grid_imga.jpg","alzhmier.pdf")






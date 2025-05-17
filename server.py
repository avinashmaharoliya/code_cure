import tensorflow as tf 
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io
import nest_asyncio
from predications import *
import shutil
import os 

import requests

def download_model(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)

download_model("https://huggingface.co/avinashmaharoliya/tumor/resolve/main/model_tumor.h5","model_tumor.h5")


tmkc = tf.keras.models.load_model("model_tumor.h5")




users_db = {}
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods={"*"}
)

@app.post("/tumor")
async def analyze_tumor(file:UploadFile=File(...)):
    contents= await file.read()
    os.makedirs("saved_images", exist_ok=True)

    save_path = os.path.join("saved_images", file.filename)

    with open(save_path, "wb") as f:
        f.write(contents)

    

    prediction = tumor(contents,tmkc,file.filename)
    
    file_path = "tumor.pdf"  
    if os.path.exists(file_path):
        return FileResponse(path=file_path, media_type='application/pdf', filename="report.pdf")
    else:
        return {"error": "File not found"}
    
nest_asyncio.apply()
if __name__ =="__main__":
    import uvicorn
    import os

    # Use port from environment or fallback to 5000
    port = int(os.environ.get("PORT", 5000))

    # Use 0.0.0.0 for external access on hosting platforms like Render
    uvicorn.run(app, host="0.0.0.0", port=port)

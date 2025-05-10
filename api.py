
from google import genai
from PIL import Image
from google.genai import types
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image,ImageDraw
import textwrap
from reportlab.lib.utils import ImageReader

def save_grid(image_path, output_path, rows=5, cols=10):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Vertical lines
    for i in range(1, cols):
        x = i * width // cols
        draw.line([(x, 0), (x, height)], fill="black", width=1)

    # Horizontal lines
    for j in range(1, rows):
        y = j * height // rows
        draw.line([(0, y), (width, y)], fill="black", width=1)

    img.save(output_path)
    print(f"Image with grid saved at {output_path}")


def save_pdf(text, image_path, filename="model_output.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    page_width, page_height = A4

    # Load and resize image
    img = Image.open(image_path)
    img_width, img_height = img.size
    aspect = img_height / img_width

    max_width = page_width - 100  # 50pt margins
    max_height = page_height / 3

    if img_width > max_width:
        img_width = max_width
        img_height = img_width * aspect
    if img_height > max_height:
        img_height = max_height
        img_width = img_height / aspect

    img_x = (page_width - img_width) / 2
    img_y = page_height - img_height - 50

    c.drawImage(ImageReader(img), img_x, img_y, width=img_width, height=img_height)

    # Set up text wrapping
    text_y = img_y - 40
    text_x = 50
    wrap_width = 90  # Number of characters per line, adjust as needed

    for line in text.split('\n'):
        wrapped_lines = textwrap.wrap(line, width=wrap_width)
        for wrap_line in wrapped_lines:
            c.drawString(text_x, text_y, wrap_line)
            text_y -= 20

    c.save()
    print(f"Centered image PDF saved as {filename}")

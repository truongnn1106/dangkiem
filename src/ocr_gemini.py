from dotenv import load_dotenv
import os
import google.generativeai as genai
import io
import PIL.Image as Image
import numpy as np
load_dotenv()


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def load_image(image_path):
    if image_path is not None:
        im = Image.open(image_path)
        pil_im = Image.fromarray(np.uint8(im))
        b = io.BytesIO()
        pil_im.save(b, format='PNG')
        image = b.getvalue()
        
        image_parts = [
            {
                "data": image,
                "mime_type": "image/png",
            }
        ]
        return image_parts
    else:
        raise ValueError("Image path is empty")

if __name__ == "__main__":
    input = "A photo of a captcha"
    image = load_image("captcha2.png")
    prompt = 'You are an expert in understanding captcha. You will receive an input image as captcha. You will output is a text in image. Dont explain any more. I need to a text in ""'
    text = get_gemini_response(input, image, prompt)
    text = cleanup_text(text)
    # Output: "9b8XY"
    text = text.replace('"', '')
    print(text)

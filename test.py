import base64
import requests
from io import BytesIO
from PIL import Image

model_inputs = {
    'prompt': "an astronaut riding a (horse:motorcycle:0.5) on the moon",
    "negative_prompt": "cartoonish, low quality, EasyNegative",
    "steps": 25,
    "sampler_name": "Euler a",
    "cfg_scale": 7.5,
    "seed": 42,
    "batch_size": 1,
    "n_iter": 1,
    "width": 512,
    "height": 512,
    "tiling": False
}
res = requests.post('http://localhost:8000/', json = model_inputs)
print(res.json())
base64_output = res.json()["base64_output"]
image_encoded = base64_output.encode('utf-8')
image_bytes = BytesIO(base64.b64decode(image_encoded))
image = Image.open(image_bytes)
image.save("output.jpg")

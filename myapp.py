# import asyncio
# import aiohttp
# import cv2
# import numpy as np
# from sanic import Sanic, response

# app = Sanic(__name__)

# async def fetch_image(session, url):
#     try:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 image_data = await response.read()
#                 return cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
#             else:
#                 return None
#     except Exception as e:
#         return None

# async def create_composite_image():
#     async with aiohttp.ClientSession() as session:
#         base_url = 'https://api.slingacademy.com/v1/sample-data/photos'
#         image_size = (32, 32)
#         num_images = 132
#         composite_image = np.zeros((image_size[1] * 12, image_size[0] * 11, 3), dtype=np.uint8)

#         tasks = []
#         for i in range(num_images):
#             image_url = f"{base_url}?limit=1&offset={i}"
#             task = fetch_image(session, image_url)
#             tasks.append(task)

#         responses = await asyncio.gather(*tasks)

#         row, col = 0, 0
#         for response in responses:
#             if response is not None:
#                 thumbnail = cv2.resize(response, image_size)
#                 composite_image[row:row+image_size[1], col:col+image_size[0]] = thumbnail
#             else:
#                 # If fetching error or image decode error, substitute with blue (0, 0, 255)
#                 error_tile = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
#                 error_tile[:, :] = (255, 0, 0)  # Set the error tile to red
#                 composite_image[row:row+image_size[1], col:col+image_size[0]] = error_tile

#             col += image_size[0]
#             if col >= composite_image.shape[1]:
#                 col = 0
#                 row += image_size[1]

#         _, encoded_image = cv2.imencode('.jpg', composite_image)
#         return encoded_image.tobytes()

# @app.route('/')
# async def serve_composite_image(request):
#     image_data = await create_composite_image()
#     return response.raw(image_data, content_type='image/jpeg')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000)
import asyncio
import aiohttp
import numpy as np
from sanic import Sanic, response
from PIL import Image, ImageDraw
import io

app = Sanic(__name__)

async def fetch_image(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                return Image.open(io.BytesIO(image_data))
            else:
                return None
    except Exception as e:
        return None

async def create_composite_image():
    async with aiohttp.ClientSession() as session:
        base_url = 'https://api.slingacademy.com/v1/sample-data/photos'
        image_size = (32, 32)
        num_images = 132
        composite_image = Image.new('RGB', (image_size[0] * 11, image_size[1] * 12))

        tasks = []
        for i in range(num_images):
            image_url = f"{base_url}?limit=1&offset={i}"
            task = fetch_image(session, image_url)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        draw = ImageDraw.Draw(composite_image)
        row, col = 0, 0
        for response in responses:
            if response is not None:
                thumbnail = response.resize(image_size)
                composite_image.paste(thumbnail, (col, row))
            else:
                # If fetching error or image decode error, draw a blue rectangle (0, 0, 255)
                draw.rectangle([col, row, col + image_size[0], row + image_size[1]], fill=(0, 0, 255))

            col += image_size[0]
            if col >= composite_image.width:
                col = 0
                row += image_size[1]

        return composite_image

@app.route('/')
async def serve_composite_image(request):
    try:
        composite_image = await create_composite_image()
        image_data = io.BytesIO()
        composite_image.save(image_data, format='JPEG')
        image_data.seek(0)

        return response.raw(image_data.read(), content_type='image/jpeg')
    except Exception as e:
        return response.text(f"An error occurred: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


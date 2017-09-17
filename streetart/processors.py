from PIL import Image, ImageDraw
import requests
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def add_watermark(image, watermark):
    #TODO: convert image and watermark from URL to PIL.Image
    rgba_image = image.convert('RGBA')
    rgba_watermark = watermark.convert('RGBA')

    image_x, image_y = rgba_image.size
    watermark_x, watermark_y = rgba_watermark.size

    watermark_scale = max(image_x / (2.0 * watermark_x), image_y / (2.0 * watermark_y))
    new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
    rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)

    rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 25))
    rgba_watermark.putalpha(rgba_watermark_mask)

    watermark_x, watermark_y = rgba_watermark.size
    rgba_image.paste(rgba_watermark, ((image_x - watermark_x) // 2, (image_y - watermark_y) // 2), rgba_watermark_mask)

    return rgba_image

def convert_rgba(img):
    im = Image.open(BytesIO(img.read()))
    #If RGBA, convert transparency
    if im.mode == "RGBA":
        im.load()
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[3]) # 3 is the alpha channel
        im=background
    im_io = BytesIO()
    im.save(im_io, format='JPEG')
    im_io.seek(0)
    return InMemoryUploadedFile(im_io,'ImageField', "%s.jpg" %img.name.split('.')[0], 'image/jpeg', im_io.getbuffer().nbytes, None)
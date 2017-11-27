from PIL import Image, ImageDraw
import requests
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def add_watermark(image, watermark):
    #TODO: convert image and watermark from URL to PIL.Image
    im = Image.open(BytesIO(image.read()))
    rgba_image = im.convert('RGBA')
    rgba_watermark = watermark.convert('RGBA')

    image_x, image_y = rgba_image.size
    watermark_x, watermark_y = rgba_watermark.size

    watermark_scale = max((image_x / (2.0 * watermark_x))/3.0, ((image_y / (2.0 * watermark_y))/3.0))
    new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
    rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)

    #rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 255))
    #rgba_watermark.putalpha(rgba_watermark_mask)

    watermark_x, watermark_y = rgba_watermark.size
    rgba_image.paste(rgba_watermark, ((image_x - watermark_x - 15), (image_y - watermark_y - 15)), rgba_watermark)

    rgba_image.load()
    background = Image.new("RGB", rgba_image.size, (255, 255, 255))
    background.paste(rgba_image, mask=rgba_image.split()[3]) # 3 is the alpha channel
    rgba_image=background
    im_io = BytesIO()
    rgba_image.save(im_io, format='JPEG')
    im_io.seek(0)
    return InMemoryUploadedFile(im_io,'ImageField', "%s-watermarked.jpg" %image.name.split('.')[0], 'image/jpeg', im_io.getbuffer().nbytes, None)

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
### imgProcessor.py



import io
import requests
from os import environ
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageOps



## Processor commands (options)

proc_cmds = ['/neg', '/ctr', '/bgt', '/sat', '/shp', '/w2x', '/col', '/cap', '/drm']


## Return the processor commands

def get_proc_cmds():
    return proc_cmds
  

## Process an image (in bytes) according to a desired command

def process_byte(img_byte, cmd_name, cmd_args=[]):
    img_stream = io.BytesIO(img_byte)
    img = Image.open(img_stream)
    log_only = False
    log = ''
    
    if cmd_name == '/neg':
        img_new = proc_neg(img)
        
    elif cmd_name == '/ctr':
        if not len(cmd_args) == 1:
            log_only = True
        else:
            try:
                cmd_arg = float(cmd_args[0])
            except ValueError: 
                log_only = True
        if not log_only:
            cmd_arg = float(cmd_args[0])
            img_new = proc_ctr(img, cmd_arg)
            img_stream = io.BytesIO()
            img_new.save(img_stream, 'JPEG')
            img_stream = img_stream.getvalue()
        else:
            img_new = img
            log = 'Invalid arguments...'
    
    elif cmd_name == '/bgt':
        if not len(cmd_args) == 1:
            log_only = True
        else:
            try:
                cmd_arg = float(cmd_args[0])
            except ValueError: 
                log_only = True
        if not log_only:
            cmd_arg = float(cmd_args[0])
            img_new = proc_bgt(img, cmd_arg)
            img_stream = io.BytesIO()
            img_new.save(img_stream, 'JPEG')
            img_stream = img_stream.getvalue()
        else:
            img_new = img
            log = 'Invalid arguments..'
    
    elif cmd_name == '/sat':
        if not len(cmd_args) == 1:
            log_only = True
        else:
            try:
                cmd_arg = float(cmd_args[0])
            except ValueError: 
                log_only = True
        if not log_only:
            cmd_arg = float(cmd_args[0])
            img_new = proc_sat(img, cmd_arg)
            img_stream = io.BytesIO()
            img_new.save(img_stream, 'JPEG')
            img_stream = img_stream.getvalue()
        else:
            img_new = img
            log = 'Invalid arguments....'
    
    elif cmd_name == '/shp':
        if not len(cmd_args) == 1:
            log_only = True
        else:
            try:
                cmd_arg = float(cmd_args[0])
            except ValueError: 
                log_only = True
        if not log_only:
            cmd_arg = float(cmd_args[0])
            img_new = proc_shp(img, cmd_arg)
            img_stream = io.BytesIO()
            img_new.save(img_stream, 'JPEG')
            img_stream = img_stream.getvalue()
        else:
            img_new = img
            log = 'Invalid arguments.'
    
    elif cmd_name == '/w2x':
        img_stream = img_2x(img_byte)
        
    elif cmd_name == '/col':
        img_stream = img_col(img_byte)
        
    elif cmd_name == '/cap':
        img_stream, log = img_cap(img_byte)
        log_only = True
        
    elif cmd_name == '/drm':
        img_stream = img_drm(img_byte)
        
    return img_stream, log_only, log
  

## Processors

# negative transformation
def proc_neg(img):
    img = ImageOps.invert(img)
    return img
  
# contrast correction
def proc_ctr(img, factor):
    img = ImageEnhance.Contrast(img).enhance(factor)
    return img
  
# brightness correction
def proc_bgt(img, factor):
    img = ImageEnhance.Brightness(img).enhance(factor)
    return img
  
# saturation correction
def proc_sat(img, factor):
    img = ImageEnhance.Color(img).enhance(factor)
    return img
  
# sharpness correction
def proc_shp(img, factor):
    img = ImageEnhance.Sharpness(img).enhance(factor)
    return img
  

## AI processing

# enlarge an image (double its size) using the Waifu2x API
def img_2x(img_byte):
    img_stream = io.BytesIO(img_byte)
    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        files={
            'image': img_byte,
        },
        headers={'api-key': environ['DEEPAI_API_KEY']}
    )
    img_new = requests.get(r.json().get('output_url')).content
    return img_new

# colorize an image using another deepai API
def img_col(img_byte):
    img_stream = io.BytesIO(img_byte)
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={
            'image': img_byte,
        },
        headers={'api-key': environ['DEEPAI_API_KEY']}
    )
    img_new = requests.get(r.json().get('output_url')).content
    return img_new

# generate image captions (silly ones, indeed)
def img_cap(img_byte):
    img_stream = io.BytesIO(img_byte)
    r = requests.post(
        "https://api.deepai.org/api/neuraltalk",
        files={
            'image': img_byte,
        },
        headers={'api-key': environ['DEEPAI_API_KEY']}
    )
    gen_caption = r.json().get('output')
    print(gen_caption)
    return img_stream, gen_caption

# classical deep dream
def img_drm(img_byte):
    img_stream = io.BytesIO(img_byte)
    r = requests.post(
        "https://api.deepai.org/api/deepdream",
        files={
            'image': img_byte,
        },
        headers={'api-key': environ['DEEPAI_API_KEY']}
    )
    img_new = requests.get(r.json().get('output_url')).content
    return img_new


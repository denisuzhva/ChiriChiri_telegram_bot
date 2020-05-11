### imgProcessor.py



import io
import requests
from os import environ
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageOps



## Processor commands (options)

proc_cmds = ['/neg', '/ctr', '/bgt', '/sat', '/shp', '/w2x']


## Return the processor commands

def get_proc_cmds():
    return proc_cmds
  

## Process an image (in bytes) according to a desired command

def process_byte(img_byte, cmd_name, cmd_args=[]):
    img_stream = io.BytesIO(img_byte)
    img = Image.open(img_stream)
    errors = False
    log = ''
    
    if cmd_name == '/neg':
        img_new = proc_neg(img)
        
    elif cmd_name == '/ctr':
        if not len(cmd_args) == 1:
            errors = True
        else:
            try:
                cmd_arg = float(cmd_args[0])
            except ValueError: 
                errors = True
        if not errors:
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
            errors = True
        else:
            try:
                cmd_arg = float(cmd_args[0])
            except ValueError: 
                errors = True
        if not errors:
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
            errors = True
        else:
            try:
                cmd_arg = float(cmd_args[0])
            except ValueError: 
                errors = True
        if not errors:
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
            errors = True
        else:
            try:
                cmd_arg = float(cmd_args[0])
            except ValueError: 
                errors = True
        if not errors:
            cmd_arg = float(cmd_args[0])
            img_new = proc_shp(img, cmd_arg)
            img_stream = io.BytesIO()
            img_new.save(img_stream, 'JPEG')
            img_stream = img_stream.getvalue()
        else:
            img_new = img
            log = 'Invalid arguments.'
    
    elif cmd_name == '/w2x':
        img_stream = img2x(img_byte)
    
    else:
        img_new = img
    
    
    return img_stream, errors, log
  

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
  

## Enlarger

# enlarge an image (double its size) using the Waifu2x API
def img2x(img_byte):
    img_stream = io.BytesIO(img_byte)
    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        files={
            'image': img_byte,
        },
        headers={'api-key': environ['DEEPAI_API_KEY']}
    )
    print(r.json())
    img_new = requests.get(r.json().get('output_url')).content
    return img_new


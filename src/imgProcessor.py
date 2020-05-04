### imgProcessor.py



import io
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageOps



## Processor commands (options)

proc_commands = ['/neg', '/ctr', '/bgt', '/sat', '/shp']


## Return the processor commands

def get_proc_cmds():
    return proc_commands
  

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
        else:
            img_new = img
            log = 'Invalid arguments.'
    else:
        img_new = img
    
    img_stream = io.BytesIO()
    img_new.save(img_stream, 'JPEG')
    img_stream = img_stream.getvalue()
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
### imgProcessor.py



import io
import numpy as np
from PIL import Image



## Processor commands (options)

proc_commands = ['/neg']


## Return the processor commands

def get_proc_cmds():
    return proc_commands
  

## Process an image (in bytes) according to a desired command

def process_byte(img_byte, cmd_name, cmd_args=[]):
    img_stream = io.BytesIO(img_byte)
    img = Image.open(img_stream)
    img_np = np.array(img.convert('RGB'))
    if cmd_name == '/neg':
        img_new = make_neg(img_np)
        
    img_new = Image.fromarray(img_new)
    img_byte = io.BytesIO()
    img_new.save(img_byte, 'JPEG')
    img_byte = img_byte.getvalue()
    return img_byte
  

## Processors

# negative transformation
def make_neg(img):
    return (255 - img)
#    mybarcode.py
from base64 import b64encode
from reportlab.lib import units
from reportlab.graphics import renderPM
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing


# def get_barcode(value, width, barWidth = 0.05 * units.inch, fontSize = 20, humanReadable = False):
#     barcode = createBarcodeDrawing('Code128', value = value, barWidth = barWidth, fontSize = fontSize, humanReadable = humanReadable)
#     drawing_width = width
#     barcode_scale = drawing_width / barcode.width
#     drawing_height = 40
#     drawing = Drawing(drawing_width, drawing_height)
#     drawing.scale(barcode_scale, barcode_scale)
#     drawing.add(barcode, name='barcode')
#     return drawing

# def get_image(cod):
#     barcode = get_barcode(value = cod, width = 400)
#     data = b64encode(renderPM.drawToString(barcode, fmt = 'PNG'))
#     return format(data)

def get_barcode(value, width, barWidth = 0.05 * units.inch, fontSize = 20, humanReadable = False):
    barcode = createBarcodeDrawing('Code128', value = value, barWidth = barWidth, fontSize = fontSize, humanReadable = humanReadable)
    drawing_width = width
    barcode_scale = drawing_width / barcode.width
    drawing_height = 40
    drawing = Drawing(drawing_width, drawing_height)
    drawing.scale(barcode_scale, barcode_scale)
    drawing.add(barcode, name='barcode')
    return drawing

def get_image(cod):
    barcode = get_barcode(value = cod, width = 600)
    data = b64encode(renderPM.drawToString(barcode, fmt = 'PNG'))    
    return format(data)

from .generarI25 import GenerarImagen
from .base64 import encodestring
import StringIO

def get_image2(cod):
    barcode = GenerarImagen(codigo=cod)
    output = StringIO.StringIO()
    barcode.save(output,format="PNG")
    data = encodestring(output.getvalue())
    return format(data)

import io
from .code128b import code128_format,code128_image
def get_image3(cod):
    data = code128_format(cod)
    img = code128_image(data)    
    fp = io.BytesIO()
    img.save(fp,"PNG")
    fp.seek(0)
    resp = encodestring(fp.getvalue())
    fp.close()
    return resp

  
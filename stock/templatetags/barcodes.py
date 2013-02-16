from django import template
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics import renderSVG
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def barcode(value):
    if type(value)==unicode and len(value)==12 and value.isdigit():
        d = createBarcodeDrawing("EAN13", value=str(value))
        s = renderSVG.drawToString(d)
        lines = s.split('\n')
        outlines = []
        outlines.append(lines[4])
        outlines.extend(lines[7:])
        return mark_safe("\n".join(outlines))
    else:
        return type(value)

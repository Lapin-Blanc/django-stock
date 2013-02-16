from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4

from django.http import HttpResponse
from django.template.defaultfilters import slugify

from documents.models import BarcodePage
from django.shortcuts import get_object_or_404

def print_barcode_page(request, page_id):
    bcp = get_object_or_404(BarcodePage, id=page_id)
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % slugify(bcp.titre)

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    width, height = A4
    p.drawCentredString(width/2, height-50, bcp.titre)
    produits = bcp.produits.all()
    for idx, prod in enumerate(produits):
        row = idx%7
        col = idx//7
        h = 110
        w = 180
        v_offset = height-80
        h_offset = 60
        img_offset = 80
        text_offset = 10
        
        d = createBarcodeDrawing("EAN13",value=str(prod.ean))
        p.drawString(h_offset+text_offset+col*w, v_offset-row*h, prod.nom)
        renderPDF.draw(d, p, h_offset+col*w, v_offset-img_offset-row*h)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


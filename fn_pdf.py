from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from config import PDF_CONFIG, IMAGE_CONFIG, DEFAULT_FILENAME

def generate_pdf(qr_img, output_path, filename=DEFAULT_FILENAME):
    """
    Genera un archivo PDF del código QR
    
    Args:
        qr_img: Imagen QR generada
        output_path: Ruta donde guardar el archivo
        filename: Nombre base del archivo (sin extensión)
    
    Returns:
        str: Ruta del archivo generado
    """
    pdf_file = os.path.join(output_path, f"{filename}.pdf")
    temp_qr_path = os.path.join(output_path, PDF_CONFIG['temp_file'])
    
    # Guardar imagen temporal
    qr_img.save(temp_qr_path, dpi=(IMAGE_CONFIG['dpi'], IMAGE_CONFIG['dpi']))
    
    # Crear PDF
    c = canvas.Canvas(pdf_file, pagesize=letter)
    page_width, page_height = letter
    qr_width = PDF_CONFIG['qr_width']
    qr_height = PDF_CONFIG['qr_height']
    x = (page_width - qr_width) / 2
    y = (page_height - qr_height) / 2
    c.drawImage(temp_qr_path, x, y, width=qr_width, height=qr_height)
    c.save()
    
    # Eliminar archivo temporal
    os.remove(temp_qr_path)
    
    return pdf_file 
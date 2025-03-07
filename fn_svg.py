import os
import qrcode.image.svg
from config import DEFAULT_FILENAME

def generate_svg(qr, output_path, filename=DEFAULT_FILENAME):
    """
    Genera un archivo SVG del código QR
    
    Args:
        qr: Objeto QRCode
        output_path: Ruta donde guardar el archivo
        filename: Nombre base del archivo (sin extensión)
    
    Returns:
        str: Ruta del archivo generado
    """
    svg_file = os.path.join(output_path, f"{filename}.svg")
    
    # Crear una imagen SVG del código QR
    factory = qrcode.image.svg.SvgImage
    img = qr.make_image(image_factory=factory)
    
    # Guardar el archivo SVG
    with open(svg_file, 'wb') as f:
        f.write(img.to_string())
    
    return svg_file 
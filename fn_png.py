from PIL import Image
import os
from config import DEFAULT_FILENAME, IMAGE_CONFIG

def generate_png(qr_img, output_path, filename=DEFAULT_FILENAME):
    """
    Genera un archivo PNG del código QR
    
    Args:
        qr_img: Imagen QR generada
        output_path: Ruta donde guardar el archivo
        filename: Nombre base del archivo (sin extensión)
    
    Returns:
        str: Ruta del archivo generado
    """
    png_file = os.path.join(output_path, f"{filename}.png")
    qr_img.save(png_file, dpi=(IMAGE_CONFIG['dpi'], IMAGE_CONFIG['dpi']))
    return png_file 
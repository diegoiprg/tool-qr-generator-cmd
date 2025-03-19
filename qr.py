import qrcode
import os
from datetime import datetime
import argparse
from fn_png import generate_png
from fn_svg import generate_svg
from fn_pdf import generate_pdf
import validators
import logging
import zipfile
from config import (
    FOLDER_CONFIG, 
    DATE_FORMAT, 
    DEFAULT_FILENAME, 
    DEFAULT_QR_CONFIG,
    LOG_CONFIG,
    ZIP_FILENAME
)

# Inicializar logger global
logger = None

def setup_logger(timestamp):
    """Configura el sistema de logging"""
    # Crear carpeta de logs si no existe
    log_dir = FOLDER_CONFIG['logs_dir']
    os.makedirs(log_dir, exist_ok=True)
    
    # Nombre del archivo de log con timestamp
    log_file = os.path.join(log_dir, f"{timestamp}.log")
    
    logging.basicConfig(
        level=getattr(logging, LOG_CONFIG['level']),
        format=LOG_CONFIG['format'],
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def create_output_folder():
    """Crea la estructura de carpetas necesaria"""
    timestamp = datetime.now().strftime(DATE_FORMAT['folder_timestamp'])
    base_path = FOLDER_CONFIG['output_dir']
    output_path = os.path.join(base_path, timestamp)
    
    # Crear carpetas si no existen
    os.makedirs(output_path, exist_ok=True)
    
    return output_path, timestamp

def validate_url(url):
    """
    Valida que la URL sea válida
    """
    if not url or url.isspace():
        print("Error: La URL es requerida y no puede estar vacía")
        return False
    
    if not validators.url(url):
        print("Error: La URL no es válida")
        print("Ejemplo de URL válida: https://www.ejemplo.com")
        return False
    return True

def generate_qr(data, qr_type='url', formats=None, filename=None, **kwargs):
    """
    Genera código QR en los formatos especificados
    
    Args:
        data: Datos a codificar (URL o información de WiFi)
        qr_type: Tipo de QR a generar ('url' o 'wifi')
        formats: Lista de formatos ('png', 'svg', 'pdf') o None para todos
        filename: Nombre base para los archivos generados (sin extensión)
        fill_color: Color del QR (default: "black")
        back_color: Color del fondo (default: "white")
        box_size: Tamaño de cada caja (default: 10)
        border: Tamaño del borde (default: 4)
        version: Versión del QR (1-40, default: 10)
    
    Ejemplos:
        Generar QR para URL:
            python qr.py "https://www.ejemplo.com" --qr-type url
        
        Generar QR para WiFi:
            python qr.py "WPA,miSSID,miContraseña" --qr-type wifi
    """
    # Crear carpetas y obtener timestamp
    output_path, timestamp = create_output_folder()
    
    # Configurar logger con el mismo timestamp
    global logger
    logger = setup_logger(timestamp)
    
    logger.info(f"Carpeta de salida creada: {output_path}")
    
    # Validar datos antes de continuar
    if qr_type == 'url':
        if not validate_url(data):
            return None
        logger.info(f"Iniciando generación de QR para URL: {data}")
    elif qr_type == 'wifi':
        logger.info(f"Iniciando generación de QR para WiFi: {data}")
        data = f"WIFI:T:{data['protocol']};S:{data['ssid']};P:{data['password']};;"
    else:
        logger.error("Tipo de QR no soportado")
        return None
    
    # Si no se especifican formatos, usar todos
    if formats is None:
        formats = ['png', 'svg', 'pdf']
    
    if filename is None:
        filename = DEFAULT_FILENAME
    
    # Configuración por defecto
    config = {
        'fill_color': kwargs.get('fill_color', DEFAULT_QR_CONFIG['fill_color']),
        'back_color': kwargs.get('back_color', DEFAULT_QR_CONFIG['back_color']),
        'box_size': kwargs.get('box_size', DEFAULT_QR_CONFIG['box_size']),
        'border': kwargs.get('border', DEFAULT_QR_CONFIG['border']),
        'version': kwargs.get('version', DEFAULT_QR_CONFIG['version'])
    }
    
    # Crear QR en alta resolución
    logger.info("Generando código QR base...")
    qr = qrcode.QRCode(
        version=config['version'],
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=config['box_size'],
        border=config['border'],
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Generar imagen QR
    qr_img = qr.make_image(
        fill_color=config['fill_color'],
        back_color=config['back_color']
    ).convert("RGB")
    
    generated_files = []
    
    # Generar archivos según formatos solicitados
    if 'png' in formats:
        logger.info("Generando archivo PNG...")
        generated_files.append(
            generate_png(qr_img, output_path, filename)
        )
    
    if 'svg' in formats:
        logger.info("Generando archivo SVG...")
        generated_files.append(generate_svg(qr, output_path))
    
    if 'pdf' in formats:
        logger.info("Generando archivo PDF...")
        generated_files.append(generate_pdf(qr_img, output_path))
    
    logger.info(f"Archivos generados: {generated_files}")
    
    return generated_files

def compress_output(output_path, files):
    """Comprime los archivos generados en un ZIP"""
    timestamp = datetime.now().strftime(DATE_FORMAT['folder_timestamp'])
    zip_name = f"{DEFAULT_FILENAME}_{timestamp}.zip"
    zip_path = os.path.join(output_path, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    
    return zip_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Genera códigos QR en diferentes formatos')
    parser.add_argument('data', help='Datos a codificar en el QR (URL o información de WiFi)')
    parser.add_argument('--qr-type', choices=['url', 'wifi'], default='url', help='Tipo de QR a generar')
    parser.add_argument('--formats', nargs='+', choices=['png', 'svg', 'pdf'],
                      help='Formatos a generar (opcional, por defecto genera todos)')
    parser.add_argument('--filename', help='Nombre base para los archivos generados')
    parser.add_argument('--fill-color', default='black', help='Color del QR')
    parser.add_argument('--back-color', default='white', help='Color del fondo')
    parser.add_argument('--box-size', type=int, default=10, help='Tamaño de cada caja')
    parser.add_argument('--border', type=int, default=4, help='Tamaño del borde')
    parser.add_argument('--compress', action='store_true', help='Comprimir archivos en ZIP')
    
    args = parser.parse_args()
    
    if args.qr_type == 'wifi':
        protocol, ssid, password = args.data.split(',')
        data = {'protocol': protocol, 'ssid': ssid, 'password': password}
    else:
        data = args.data
    
    files = generate_qr(
        data, 
        qr_type=args.qr_type,
        formats=args.formats,
        filename=args.filename,
        fill_color=args.fill_color,
        back_color=args.back_color,
        box_size=args.box_size,
        border=args.border
    )
    
    if args.compress and files:
        zip_file = compress_output(os.path.dirname(files[0]), files)
        print(f"\nArchivos comprimidos en: {zip_file}")
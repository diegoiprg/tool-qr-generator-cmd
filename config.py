"""
Archivo de configuración con parámetros por defecto
"""

# Estructura de carpetas
FOLDER_CONFIG = {
    'output_dir': 'output',    # Carpeta principal para archivos generados
    'logs_dir': 'log'          # Carpeta para archivos de log
}

# Formatos de fecha/hora
DATE_FORMAT = {
    'folder_timestamp': '%Y%m%d%H%M%S',  # Formato para nombres de carpetas y archivos
    'log_timestamp': '%Y-%m-%d %H:%M:%S' # Formato para mensajes en el log
}

# Nombres de archivos por defecto
DEFAULT_FILENAME = "qrCode"     # Nombre base para todos los archivos generados
ZIP_FILENAME = "qrCode"   # Nombre base del archivo ZIP (se añadirá timestamp)

# Configuración QR
DEFAULT_QR_CONFIG = {
    'version': 10,              # Versión del QR (1-40)
    'error_correction': 'H',    # Nivel de corrección de errores (L,M,Q,H)
    'box_size': 10,            # Tamaño de cada módulo del QR
    'border': 4,               # Tamaño del borde
    'fill_color': 'black',     # Color del QR
    'back_color': 'white'      # Color del fondo
}

# Configuración PDF
PDF_CONFIG = {
    'qr_width': 400,           # Ancho del QR en el PDF
    'qr_height': 400,          # Alto del QR en el PDF
    'temp_file': 'temp_qr.png' # Nombre del archivo temporal
}

# Configuración de imagen
IMAGE_CONFIG = {
    'dpi': 300                 # Resolución de imagen en DPI
}

# Formato de logging
LOG_CONFIG = {
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'level': 'INFO'
} 
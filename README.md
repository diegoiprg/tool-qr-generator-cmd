# Generador de Códigos QR

Herramienta para generar códigos QR en múltiples formatos (PNG, SVG, PDF) con opciones de personalización.

## Instalación

```bash
pip install qrcode pillow reportlab validators
```

## Uso Básico

### Generar en todos los formatos

```bash
python3 qr.py "https://www.ejemplo.com"
```

### Generar en formatos específicos

```bash
python3 qr.py "https://www.ejemplo.com" --formats png pdf
```

### Generar con opciones personalizadas

```bash
python3 qr.py "https://www.ejemplo.com" --fill-color blue --filename mi_qr --compress
```

### Generar QR para WiFi

```bash
python3 qr.py "WPA,miSSID,miContraseña" --qr-type wifi
```

## Parámetros

| Parámetro      | Descripción                         | Tipo   | Valor Default | Ejemplo                                               |
| -------------- | ----------------------------------- | ------ | ------------- | ----------------------------------------------------- |
| `data`         | Datos para el código QR (requerido) | string | -             | "https://www.ejemplo.com" o "WPA,miSSID,miContraseña" |
| `--qr-type`    | Tipo de QR a generar                | string | url           | --qr-type wifi                                        |
| `--formats`    | Formatos a generar                  | lista  | png,svg,pdf   | --formats png svg                                     |
| `--filename`   | Nombre base del archivo             | string | qr_code       | --filename mi_codigo                                  |
| `--fill-color` | Color del QR                        | string | black         | --fill-color blue                                     |
| `--back-color` | Color del fondo                     | string | white         | --back-color yellow                                   |
| `--box-size`   | Tamaño de cada módulo               | int    | 10            | --box-size 15                                         |
| `--border`     | Tamaño del borde                    | int    | 4             | --border 5                                            |
| `--compress`   | Comprimir archivos en ZIP           | bool   | False         | --compress                                            |

## Ejemplos de Uso

1. **QR Simple para URL**

```bash
python3 qr.py "https://www.google.com"
```

2. **QR para WiFi**

```bash
python3 qr.py "WPA,miSSID,miContraseña" --qr-type wifi
```

3. **QR con Colores Personalizados**

```bash
python3 qr.py "https://www.google.com" --fill-color blue --back-color yellow
```

4. **QR en Formatos Específicos**

```bash
python3 qr.py "https://www.google.com" --formats png svg
```

5. **QR con Nombre Personalizado y Compresión**

```bash
python3 qr.py "https://www.google.com" --filename "mi_qr" --compress
```

## Estructura de Archivos Generados

```
output/
    20240307141515/           # Carpeta con timestamp
        qr_code.png           # Archivo PNG
        qr_code.svg           # Archivo SVG
        qr_code.pdf           # Archivo PDF
        qr_files_20240307141515.zip  # Archivo ZIP (opcional)
```

## Consideraciones Importantes

### URLs

- Debe incluir el protocolo (http:// o https://)
- Se valida automáticamente el formato
- URLs inválidas generarán un mensaje de error

### Formatos de Salida

- **PNG**:
  - Resolución: 300 DPI
  - Ideal para web e impresión
- **SVG**:
  - Formato vectorial
  - Escalable sin pérdida de calidad
- **PDF**:
  - Tamaño carta
  - QR centrado en la página
  - Dimensiones: 400x400 puntos

### Almacenamiento

- Los archivos se guardan en carpetas con timestamp
- Cada generación tiene su propia carpeta
- La carpeta `output` se crea automáticamente

### Logging

- Se genera un archivo `qr_generator.log`
- Registra cada paso del proceso
- Incluye errores y advertencias

## Mensajes de Error Comunes

| Error                                        | Solución                                            |
| -------------------------------------------- | --------------------------------------------------- |
| "La URL es requerida y no puede estar vacía" | Proporcionar una URL                                |
| "La URL no es válida"                        | Usar formato correcto (ej: https://www.ejemplo.com) |

```

```

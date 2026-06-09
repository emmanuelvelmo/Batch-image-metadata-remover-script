import pathlib # Manejo de rutas de archivos y directorios
from PIL import Image # Procesamiento de imágenes y eliminación de metadatos

# VARIABLES GLOBALES
extensiones_lista = ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp'] # Lista de formatos de imagen soportados

# FUNCIONES
# Estandariza imagen JPEG eliminando todos los metadatos
def estandarizar_jpeg(ruta_imagen_entrada, ruta_imagen_salida):
    # Abrir imagen con PIL
    imagen_pil = Image.open(ruta_imagen_entrada)
    
    # Convertir a modo RGB si es necesario
    if imagen_pil.mode != 'RGB':
        imagen_pil = imagen_pil.convert('RGB')
    
    # Guardar imagen sin metadatos (PIL por defecto no guarda EXIF al usar save con JPEG)
    imagen_pil.save(ruta_imagen_salida, 'JPEG', quality = 95, optimize = True)

# Estandariza imagen PNG eliminando metadatos
def estandarizar_png(ruta_imagen_entrada, ruta_imagen_salida):
    # Abrir imagen con PIL
    imagen_pil = Image.open(ruta_imagen_entrada)
    
    # Convertir a modo RGB o RGBA según sea necesario
    if imagen_pil.mode not in ('RGB', 'RGBA', 'L'):
        if imagen_pil.mode == 'P':
            imagen_pil = imagen_pil.convert('RGBA')
        else:
            imagen_pil = imagen_pil.convert('RGB')
    
    # Guardar imagen sin metadatos
    imagen_pil.save(ruta_imagen_salida, 'PNG', optimize = True)

# Estandariza imagen BMP eliminando metadatos
def estandarizar_bmp(ruta_imagen_entrada, ruta_imagen_salida):
    # Abrir imagen con PIL
    imagen_pil = Image.open(ruta_imagen_entrada)
    
    # Convertir a modo RGB si es necesario
    if imagen_pil.mode != 'RGB':
        imagen_pil = imagen_pil.convert('RGB')
    
    # Guardar imagen sin metadatos
    imagen_pil.save(ruta_imagen_salida, 'BMP')

# Estandariza imagen TIFF eliminando metadatos
def estandarizar_tiff(ruta_imagen_entrada, ruta_imagen_salida):
    # Abrir imagen con PIL
    imagen_pil = Image.open(ruta_imagen_entrada)
    
    # Convertir a modo RGB si es necesario
    if imagen_pil.mode != 'RGB':
        imagen_pil = imagen_pil.convert('RGB')
    
    # Guardar imagen sin metadatos
    imagen_pil.save(ruta_imagen_salida, 'TIFF', compression = None)

# Estandariza imagen WebP eliminando metadatos
def estandarizar_webp(ruta_imagen_entrada, ruta_imagen_salida):
    # Abrir imagen con PIL
    imagen_pil = Image.open(ruta_imagen_entrada)
    
    # Convertir a modo RGB si es necesario
    if imagen_pil.mode not in ('RGB', 'RGBA'):
        imagen_pil = imagen_pil.convert('RGB')
    
    # Guardar imagen sin metadatos
    imagen_pil.save(ruta_imagen_salida, 'WEBP', quality = 95, method = 6)

# Procesa una imagen individual según su extensión
def procesar_imagen(ruta_entrada, ruta_salida):
    # Obtener extensión del archivo
    extension = ruta_entrada.suffix.lower().replace('.', '')
    
    # Seleccionar función de estandarización según extensión
    if extension in ['jpg', 'jpeg']:
        estandarizar_jpeg(ruta_entrada, ruta_salida)
    elif extension == 'png':
        estandarizar_png(ruta_entrada, ruta_salida)
    elif extension == 'bmp':
        estandarizar_bmp(ruta_entrada, ruta_salida)
    elif extension == 'tiff':
        estandarizar_tiff(ruta_entrada, ruta_salida)
    elif extension == 'webp':
        estandarizar_webp(ruta_entrada, ruta_salida)

# Procesamiento recursivo de imágenes y eliminación de metadatos
def procesar_directorio_imagenes(directorio_entrada_str):
    # Convertir string a objeto Path
    directorio_entrada = pathlib.Path(directorio_entrada_str)
    
    # Generar nombre para directorio de salida
    carpeta_salida = directorio_entrada.parent / f"{directorio_entrada.name} (output)"
    
    # Crear carpeta de destino si no existe
    carpeta_salida.mkdir(parents = True, exist_ok = True)
    
    # Mostrar separador visual para inicio de resultados
    print("-" * 36)
    
    cont_imagenes_procesadas = 0 # Contador de imágenes procesadas
    
    # Procesar recursivamente cada imagen en el directorio
    for extension_val in extensiones_lista:
        for archivo_iter in directorio_entrada.rglob(f'*.{extension_val}'):
            if archivo_iter.is_file():
                try:
                    # Calcular ruta relativa desde directorio de entrada
                    ruta_relativa = archivo_iter.parent.relative_to(directorio_entrada)
                    
                    # Generar ruta completa de archivo de salida
                    directorio_salida_iter = carpeta_salida / ruta_relativa
                    
                    # Crear directorio para guardar imagen
                    directorio_salida_iter.mkdir(parents = True, exist_ok = True)
                    
                    # Generar ruta de salida con mismo nombre y extensión
                    ruta_salida_iter = directorio_salida_iter / archivo_iter.name
                    
                    # Procesar imagen para eliminar metadatos
                    procesar_imagen(archivo_iter, ruta_salida_iter)
                    
                    # Mostrar archivo procesado
                    print(str(archivo_iter))
                    
                    cont_imagenes_procesadas += 1 # Aumentar contador
                
                except Exception as e:
                    # Mostrar error pero continuar con siguiente imagen
                    print(f"Error processing {archivo_iter.name}: {str(e)}")
    
    # Mostrar mensaje si no se procesaron imágenes
    if cont_imagenes_procesadas == 0:
        print("No images processed")
    
    # Mostrar separador final
    print("-" * 36 + "\n")

# PUNTO DE PARTIDA
# Bucle principal del programa
while True:
    # Solicitar directorio de entrada
    while True:
        directorio_entrada_val = input("Enter directory: ").strip('"\'')
        
        # Verificar que el directorio exista
        if not pathlib.Path(directorio_entrada_val).exists():
            print("Wrong directory\n")
        else:
            break
    
    # Procesar directorio de imágenes recursivamente
    procesar_directorio_imagenes(directorio_entrada_val)
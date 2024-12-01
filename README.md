# Downloads Organizer 📂

Organizador automático de archivos para la carpeta de Descargas en Windows. Mantén tu carpeta de descargas limpia y organizada automáticamente.

## Características 🚀
- **Monitoreo Inteligente**: 
  - Detecta nuevos archivos instantáneamente
  - Espera 24 horas antes de organizar
  - Comprobación cada 2 horas del estado
  - Respeta el uso activo de archivos

- **Organización Automática**:
  - Clasificación por tipo de archivo
  - Creación automática de carpetas
  - Preserva la estructura de nombres
  - Manejo seguro de archivos duplicados

- **Sistema de Logs**:
  - Registro detallado de operaciones
  - Seguimiento de archivos procesados
  - Historial de errores y eventos
  - Fácil diagnóstico de problemas

- **Integración con Windows**:
  - Inicio automático con el sistema
  - Ejecución en segundo plano
  - Bajo consumo de recursos
  - Fácil instalación y configuración

## Estructura del Proyecto 📁
```
downloads-organizer-python/
├── downloads_organizer.py     # Script principal
├── run_organizer.bat         # Script de inicio para Windows
├── requirements.txt          # Dependencias del proyecto
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Documentación del proyecto

Carpetas creadas automáticamente:
Downloads/
├── documents/               # Archivos de documentos
├── images/                 # Archivos de imágenes
├── videos/                 # Archivos de vídeo
├── music/                  # Archivos de audio
├── programs/              # Archivos ejecutables
├── compressed/            # Archivos comprimidos
└── others/                # Otros tipos de archivos
```

## Requisitos 📋
- Python 3.x
- Windows 10/11
- Módulos requeridos:
  - watchdog==6.0.0

## Instalación 🔧
1. Clonar el repositorio
   ```bash
   git clone [URL_del_repositorio]
   ```

2. Crear entorno virtual
   ```bash
   python -m venv venv
   ```

3. Activar entorno virtual
   ```bash
   venv\Scripts\activate
   ```

4. Instalar dependencias
   ```bash
   pip install -r requirements.txt
   ```

## Configuración ⚙️
1. Configurar inicio automático con el Programador de tareas de Windows:
   - Abrir Programador de tareas
   - Crear tarea básica
   - Configurar para ejecutar al inicio de sesión
   - Ruta del programa: `run_organizer.bat`

## Uso 💡
El script organiza automáticamente los archivos después de 24 horas en:
- 📄 Documents (.pdf, .doc, .txt, etc.)
- 🖼️ Images (.jpg, .png, .gif, etc.)
- 🎥 Videos (.mp4, .avi, .mkv, etc.)
- 🎵 Music (.mp3, .wav, .flac, etc.)
- 🗜️ Compressed (.zip, .rar, .7z, etc.)
- 💿 Programs (.exe, .msi)
- 📁 Others (archivos no categorizados)

## Notas Importantes ⚠️
- Los archivos nuevos se detectan instantáneamente
- La organización ocurre 24 horas después de la descarga
- El sistema verifica archivos pendientes cada 2 horas
- Todas las acciones se registran en `downloads_organizer.log`
- Se puede monitorear el proceso mediante el PID en el Administrador de tareas
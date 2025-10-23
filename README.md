# API REST con Django REST Framework

Documentación completa del proceso de creación de una API REST utilizando Django REST Framework 3.16 con arquitectura de tres capas.

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación desde Cero](#instalación-desde-cero)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración Inicial](#configuración-inicial)
- [Aplicación Teams](#aplicación-teams)
- [Comandos Útiles](#comandos-útiles)
- [Endpoints Disponibles](#endpoints-disponibles)
- [Próximos Pasos](#próximos-pasos)

---

## Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- Ambiente virtual activado

---

## Instalación desde Cero

### 1. Crear y activar ambiente virtual

```bash
# Crear ambiente virtual
python -m venv venv

# Activar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Activar ambiente virtual (Windows)
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
# Instalar Django, Django REST Framework y python-dotenv
pip install Django==4.2.* djangorestframework==3.16.* python-dotenv==1.0.*

# Instalar drf-yasg para documentación Swagger
pip install drf-yasg==1.21.*
```

### 3. Crear proyecto Django

```bash
# Crear proyecto Django llamado 'config'
django-admin startproject config .
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Django Configuration
SECRET_KEY=django-insecure-change-this-in-production-key-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Configurar settings.py

Modificar `config/settings.py` para usar variables de entorno:

```python
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    # Apps
    'teams',
]

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# Swagger Settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}
```

### 6. Configurar URLs con Swagger

Modificar `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import hola_mundo

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API REST Django",
        default_version='v1',
        description="Documentación de la API REST con Django REST Framework",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@api.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hola-mundo/', hola_mundo, name='hola-mundo'),

    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

### 7. Crear vista de prueba "Hola Mundo"

Crear archivo `config/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def hola_mundo(request):
    """
    Endpoint de prueba que retorna un mensaje de hola mundo
    """
    return Response(
        {
            'mensaje': 'Hola Mundo',
            'descripcion': 'API REST con Django REST Framework',
            'version': '1.0.0',
            'status': 'ok'
        },
        status=status.HTTP_200_OK
    )
```

### 8. Ejecutar migraciones iniciales

```bash
# Crear las tablas de Django en la base de datos
python manage.py migrate
```

### 9. Crear script de verificación de base de datos

Crear archivo `check_db_connection.py` en la raíz del proyecto:

```python
#!/usr/bin/env python
"""
Script para verificar la conexión a la base de datos
"""
import os
import sys
import django
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def check_database_connection():
    """
    Verifica la conexión a la base de datos
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        if result:
            print("=" * 50)
            print("✓ Conexión a la base de datos exitosa")
            print("=" * 50)
            print(f"Motor de base de datos: {connection.settings_dict['ENGINE']}")
            print(f"Nombre de la base de datos: {connection.settings_dict['NAME']}")
            print("=" * 50)
            return True
    except Exception as e:
        print("=" * 50)
        print("✗ Error al conectar con la base de datos")
        print("=" * 50)
        print(f"Error: {str(e)}")
        print("=" * 50)
        return False

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("VERIFICACIÓN DE CONEXIÓN A BASE DE DATOS")
    print("=" * 50 + "\n")

    if check_database_connection():
        print("\n✓ Verificación completada exitosamente\n")
        sys.exit(0)
    else:
        print("\n✗ La verificación falló\n")
        sys.exit(1)
```

### 10. Generar archivo requirements.txt

```bash
pip freeze > requirements.txt
```

---

## Estructura del Proyecto

```
poc_django/
│
├── config/                      # Proyecto Django principal
│   ├── __init__.py
│   ├── settings.py             # Configuración del proyecto
│   ├── urls.py                 # URLs principales con Swagger
│   ├── views.py                # Vista "Hola Mundo"
│   ├── wsgi.py
│   └── asgi.py
│
├── teams/                       # App Teams
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Modelo Team
│   ├── schemas.py              # Schemas (Create, Read, Update)
│   ├── views.py
│   ├── tests.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
├── venv/                        # Ambiente virtual (no incluir en git)
├── .env                         # Variables de entorno (no incluir en git)
├── .gitignore
├── manage.py                    # Script de gestión Django
├── check_db_connection.py       # Script de verificación de DB
├── requirements.txt             # Dependencias del proyecto
├── db.sqlite3                   # Base de datos SQLite
└── README.md                    # Este archivo
```

---

## Configuración Inicial

### Verificar conexión a base de datos

```bash
python check_db_connection.py
```

Salida esperada:
```
==================================================
VERIFICACIÓN DE CONEXIÓN A BASE DE DATOS
==================================================

==================================================
✓ Conexión a la base de datos exitosa
==================================================
Motor de base de datos: django.db.backends.sqlite3
Nombre de la base de datos: /home/user/poc_django/db.sqlite3
==================================================

✓ Verificación completada exitosamente
```

### Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

---

## Aplicación Teams

### Crear la aplicación

```bash
python manage.py startapp teams
```

### Modelo Team

**Archivo**: `teams/models.py`

```python
from django.db import models

class Team(models.Model):
    """
    Modelo para representar un equipo (Team)
    """
    id = models.AutoField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=255, verbose_name="Nombre del equipo")
    descripcion = models.TextField(verbose_name="Descripción del equipo", blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        db_table = 'teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"
```

**Campos del modelo:**
- `id`: AutoField (primary key, autoincrementable)
- `nombre`: CharField (máximo 255 caracteres)
- `descripcion`: TextField (opcional, puede ser null o vacío)
- `fecha_creacion`: DateTimeField (se genera automáticamente)

### Schemas (Serializadores)

**Archivo**: `teams/schemas.py`

#### TeamCreateSchema
Para crear un team (POST):
- **Campos requeridos**: `nombre`
- **Campos opcionales**: `descripcion`
- **Excluidos**: `id` (autogenerado)
- **Solo lectura**: `fecha_creacion`

#### TeamReadSchema
Para leer un team (GET):
- **Incluye todos los campos**: `id`, `nombre`, `descripcion`, `fecha_creacion`

#### TeamUpdateSchema
Para actualizar un team (PUT/PATCH):
- **Todos los campos son opcionales**: `nombre`, `descripcion`
- **Excluido**: `id` (no se puede modificar)
- Permite actualizar solo los campos enviados en la petición

### Registrar app en settings

Agregar `'teams'` a `INSTALLED_APPS` en `config/settings.py`.

### Crear y ejecutar migraciones

```bash
# Crear migraciones para la app teams
python manage.py makemigrations teams

# Ejecutar migraciones
python manage.py migrate teams
```

Salida esperada:
```
Migrations for 'teams':
  teams/migrations/0001_initial.py
    - Create model Team

Operations to perform:
  Apply all migrations: teams
Running migrations:
  Applying teams.0001_initial... OK
```

---

## Comandos Útiles

### Gestión de migraciones

```bash
# Ver migraciones aplicadas
python manage.py showmigrations

# Crear migraciones
python manage.py makemigrations

# Ejecutar migraciones
python manage.py migrate

# Revertir migraciones
python manage.py migrate <app_name> <migration_number>
```

### Shell de Django

```bash
# Abrir shell interactivo de Django
python manage.py shell

# Ejemplo de uso en el shell
>>> from teams.models import Team
>>> Team.objects.create(nombre="Equipo 1", descripcion="Descripción del equipo")
>>> Team.objects.all()
```

### Superusuario

```bash
# Crear superusuario para admin
python manage.py createsuperuser
```

### Servidor de desarrollo

```bash
# Iniciar servidor
python manage.py runserver

# Iniciar servidor en puerto específico
python manage.py runserver 8080

# Iniciar servidor en IP específica
python manage.py runserver 0.0.0.0:8000
```

---

## Endpoints Disponibles

### Documentación

| Endpoint | Descripción |
|----------|-------------|
| `http://localhost:8000/docs/` | Swagger UI - Documentación interactiva |
| `http://localhost:8000/redoc/` | ReDoc - Documentación alternativa |
| `http://localhost:8000/swagger.json` | Schema OpenAPI en formato JSON |
| `http://localhost:8000/swagger.yaml` | Schema OpenAPI en formato YAML |

### API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/hola-mundo/` | Endpoint de prueba "Hola Mundo" |
| GET | `/admin/` | Panel de administración de Django |

### Respuesta del endpoint "Hola Mundo"

```bash
curl -X GET http://localhost:8000/api/hola-mundo/
```

Respuesta:
```json
{
  "mensaje": "Hola Mundo",
  "descripcion": "API REST con Django REST Framework",
  "version": "1.0.0",
  "status": "ok"
}
```

---

## Próximos Pasos

### Arquitectura de Tres Capas para la App Teams

Se implementará la siguiente estructura modular:

```
teams/
├── models.py          # ✓ Modelos de base de datos (completado)
├── schemas.py         # ✓ Schemas/Serializadores (completado)
├── repository.py      # ⏳ Capa de acceso a datos
├── services.py        # ⏳ Lógica de negocio
├── routers.py         # ⏳ Definición de rutas/endpoints
└── views.py           # ⏳ Vistas/Controllers
```

#### 1. Repository (Capa de Acceso a Datos)
- Interacción directa con la base de datos
- Operaciones CRUD básicas
- Queries y filtros personalizados

#### 2. Services (Capa de Lógica de Negocio)
- Validaciones de negocio
- Procesamiento de datos
- Orquestación de operaciones complejas

#### 3. Routers (Capa de Rutas)
- Definición de endpoints
- Mapeo de URLs a vistas
- Configuración de métodos HTTP

#### 4. Views/Controllers
- Manejo de peticiones HTTP
- Validación de entrada
- Formato de respuestas

### Funcionalidades a Implementar

- [ ] CRUD completo para Teams
- [ ] Paginación de resultados
- [ ] Filtros de búsqueda
- [ ] Validaciones personalizadas
- [ ] Manejo de errores
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Autenticación y autorización
- [ ] Rate limiting
- [ ] Documentación de código

---

## Dependencias del Proyecto

**Archivo**: `requirements.txt`

```
asgiref==3.10.0
Django==4.2.25
djangorestframework==3.16.1
drf-yasg==1.21.11
inflection==0.5.1
packaging==25.0
python-dotenv==1.0.1
pytz==2025.2
PyYAML==6.0.3
sqlparse==0.5.3
uritemplate==4.2.0
```

### Instalación de dependencias

```bash
# Instalar desde requirements.txt
pip install -r requirements.txt
```

---

## Notas Importantes

1. **Base de datos**: Actualmente usando SQLite para desarrollo. Para producción se recomienda PostgreSQL o MySQL.

2. **Variables de entorno**: El archivo `.env` NO debe incluirse en el repositorio. Agregar a `.gitignore`.

3. **Secret Key**: Cambiar la `SECRET_KEY` en producción por una clave segura.

4. **Debug**: Establecer `DEBUG=False` en producción.

5. **Migraciones**: Siempre crear y ejecutar migraciones después de modificar modelos.

6. **Documentación Swagger**: Accesible en `/docs/` para pruebas interactivas de la API.

---

## Arquitectura del Proyecto

### Patrón de Diseño: Tres Capas

```
┌─────────────────────────────────────┐
│         ROUTERS (URLs)              │  ← Define endpoints y rutas
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│       VIEWS (Controllers)           │  ← Maneja requests/responses
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│        SERVICES (Business Logic)    │  ← Lógica de negocio
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│      REPOSITORY (Data Access)       │  ← Acceso a base de datos
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│          MODELS (Database)          │  ← Modelos ORM
└─────────────────────────────────────┘
```

### Flujo de una petición

1. **Request** → Llega al servidor
2. **Router** → Mapea la URL a una vista
3. **View** → Recibe y valida la petición
4. **Service** → Ejecuta lógica de negocio
5. **Repository** → Accede a la base de datos
6. **Model** → Interactúa con la tabla
7. **Response** → Retorna datos al cliente

---

## Autor

Proyecto creado como POC (Proof of Concept) para demostrar una API REST con Django REST Framework 3.16 utilizando arquitectura de tres capas.

---

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

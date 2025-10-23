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
│   ├── settings.py             # ✅ Configuración del proyecto
│   ├── urls.py                 # ✅ URLs principales con Swagger + Teams
│   ├── views.py                # ✅ Vista "Hola Mundo"
│   ├── wsgi.py
│   └── asgi.py
│
├── teams/                       # ✅ App Teams (Arquitectura 3 capas)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # ✅ Modelo Team
│   ├── schemas.py              # ✅ Schemas (Create, Read, Update)
│   ├── repository.py           # ✅ Capa de acceso a datos
│   ├── services.py             # ✅ Lógica de negocio y validaciones
│   ├── docs.py                 # ✅ Documentación Swagger separada
│   ├── views.py                # ✅ ViewSet (Controllers)
│   ├── routers.py              # ✅ Configuración de rutas
│   ├── tests.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py     # ✅ Migración inicial
│
├── venv/                        # Ambiente virtual (no incluir en git)
├── .env                         # Variables de entorno (no incluir en git)
├── .gitignore
├── manage.py                    # Script de gestión Django
├── check_db_connection.py       # ✅ Script de verificación de DB
├── requirements.txt             # ✅ Dependencias del proyecto
├── db.sqlite3                   # ✅ Base de datos SQLite
├── README.md                    # Este archivo
└── CLAUDE.md                    # ✅ Historial de conversación
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
| `http://localhost:8000/docs/` | **Swagger UI** - Documentación interactiva |
| `http://localhost:8000/redoc/` | **ReDoc** - Documentación alternativa |
| `http://localhost:8000/swagger.json` | Schema OpenAPI en formato JSON |
| `http://localhost:8000/swagger.yaml` | Schema OpenAPI en formato YAML |

---

### API - Endpoints de Prueba

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/hola-mundo/` | Endpoint de prueba "Hola Mundo" |
| GET | `/admin/` | Panel de administración de Django |

**Ejemplo - Hola Mundo**:

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

### API - Teams (CRUD Completo)

| Método | Endpoint | Descripción | Status |
|--------|----------|-------------|--------|
| **POST** | `/api/teams/` | Crear nuevo team | ✅ |
| **GET** | `/api/teams/` | Listar todos los teams (paginado) | ✅ |
| **GET** | `/api/teams/{id}/` | Obtener team por ID | ✅ |
| **GET** | `/api/teams/by-name/?nombre={nombre}` | Buscar team por nombre | ✅ |
| **PATCH** | `/api/teams/{id}/` | Actualizar team (parcial) | ✅ |
| **DELETE** | `/api/teams/{id}/` | Eliminar team | ✅ |

---

#### Ejemplos de uso:

**1. Crear un team**:
```bash
curl -X POST http://localhost:8000/api/teams/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Team Alpha", "descripcion": "Equipo de desarrollo"}'
```

**2. Listar teams (con paginación)**:
```bash
curl -X GET "http://localhost:8000/api/teams/?offset=0&limit=10"
```

**3. Obtener team por ID**:
```bash
curl -X GET http://localhost:8000/api/teams/1/
```

**4. Buscar team por nombre**:
```bash
curl -X GET "http://localhost:8000/api/teams/by-name/?nombre=Team%20Alpha"
```

**5. Actualizar team**:
```bash
curl -X PATCH http://localhost:8000/api/teams/1/ \
  -H "Content-Type: application/json" \
  -d '{"descripcion": "Nueva descripción"}'
```

**6. Eliminar team**:
```bash
curl -X DELETE http://localhost:8000/api/teams/1/
```

---

### 🎯 Probar en Swagger

La forma más fácil de probar todos los endpoints es usando **Swagger UI**:

1. Iniciar el servidor:
   ```bash
   python manage.py runserver 8000
   ```

2. Abrir en el navegador:
   ```
   http://localhost:8000/docs/
   ```

3. Verás todos los endpoints documentados con:
   - Descripción detallada
   - Parámetros requeridos
   - Esquemas de request/response
   - Botón "Try it out" para ejecutar directamente

---

## Arquitectura de Tres Capas - Implementación Completa

### Estructura Implementada para la App Teams

```
teams/
├── models.py          # ✅ 1. Modelos de base de datos
├── schemas.py         # ✅ 2. Schemas/Serializadores (Create, Read, Update)
├── repository.py      # ✅ 3. Capa de acceso a datos
├── services.py        # ✅ 4. Lógica de negocio y validaciones
├── views.py           # ✅ 5. ViewSets/Controllers (SOLO lógica)
├── routers.py         # ✅ 6. Configuración de rutas
└── docs.py            # ✅ 7. Documentación Swagger (SEPARADA)
```

**Orden de creación**: models.py → schemas.py → repository.py → services.py → **views.py → routers.py → docs.py**

**Nota importante**: La documentación Swagger está en `docs.py` (separada de `views.py`) para mantener el código limpio y enfocado en la lógica de negocio.

---

## Guía Paso a Paso: Crear una Nueva App con Arquitectura de Tres Capas

Esta es la **ruta correcta** que debes seguir cada vez que quieras crear una nueva aplicación en este proyecto:

### 📋 Orden de Implementación

```
1. Modelo (models.py)
   ↓
2. Schemas (schemas.py)
   ↓
3. Repository (repository.py)
   ↓
4. Services (services.py)
   ↓
5. Views (views.py)         ← PRIMERO: Define los ViewSets
   ↓
6. Routers (routers.py)     ← DESPUÉS: Registra los ViewSets
   ↓
7. URLs (config/urls.py)
   ↓
8. Migraciones y Pruebas
```

**Nota importante**: En Django REST Framework, primero creas las **Views** (que contienen los ViewSets) y luego creas el **Router** para registrar esos ViewSets. Esto es diferente a FastAPI donde el router se define directamente en el archivo de rutas.

---

### 🔷 PASO 1: Crear el Modelo (models.py)

**Ubicación**: `<app_name>/models.py`

**Qué hacer**:
- Define la estructura de tu tabla en la base de datos
- Establece los campos y sus tipos
- Configura Meta (nombre de tabla, ordering, etc.)

**Ejemplo con la app Teams**:

```python
from django.db import models

class Team(models.Model):
    """
    Modelo para representar un equipo (Team)
    """
    # ID autoincrementable
    id = models.AutoField(primary_key=True, editable=False)

    # Campos del modelo
    nombre = models.CharField(max_length=255, verbose_name="Nombre del equipo")
    descripcion = models.TextField(verbose_name="Descripción del equipo", blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        db_table = 'teams'  # Nombre de la tabla en BD
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['-fecha_creacion']  # Ordenar por fecha descendente

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"
```

**Importante**:
- `auto_now_add=True` → Se crea automáticamente al insertar
- `blank=True, null=True` → Campo opcional
- `max_length` → Requerido para CharField

---

### 🔷 PASO 2: Crear los Schemas (schemas.py)

**Ubicación**: `<app_name>/schemas.py`

**Qué hacer**:
- Crear **3 schemas** usando serializers de DRF:
  - **CreateSchema**: Para peticiones POST (sin `id`)
  - **ReadSchema**: Para respuestas GET (todos los campos)
  - **UpdateSchema**: Para peticiones PATCH/PUT (campos opcionales, sin `id`)

**Ejemplo con la app Teams**:

```python
from rest_framework import serializers
from .models import Team

class TeamCreateSchema(serializers.ModelSerializer):
    """Schema para crear un Team"""
    class Meta:
        model = Team
        fields = ['nombre', 'descripcion', 'fecha_creacion']
        read_only_fields = ['fecha_creacion']

class TeamReadSchema(serializers.ModelSerializer):
    """Schema para leer un Team"""
    class Meta:
        model = Team
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']

class TeamUpdateSchema(serializers.ModelSerializer):
    """Schema para actualizar un Team"""
    nombre = serializers.CharField(max_length=255, required=False)
    descripcion = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Team
        fields = ['nombre', 'descripcion']

    def update(self, instance, validated_data):
        # Actualizar solo campos enviados
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
```

**Importante**:
- CreateSchema: `id` no se incluye (autogenerado)
- ReadSchema: Incluye todos los campos
- UpdateSchema: Todos los campos son `required=False`

---

### 🔷 PASO 3: Crear el Repository (repository.py)

**Ubicación**: `<app_name>/repository.py`

**Qué hacer**:
- Crear clase `<ModelName>Repository`
- Implementar métodos para acceso a base de datos:
  - `create_<model>()` - Crear registro
  - `get_<model>_by_id()` - Obtener por ID
  - `get_<model>_by_<field>()` - Obtener por otro campo
  - `get_all_<models>()` - Listar todos (con paginación)
  - `update_<model>()` - Actualizar registro
  - `delete_<model>()` - Eliminar registro
  - `exists_by_<field>()` - Verificar existencia

**Ejemplo con la app Teams**:

```python
from typing import List, Optional, Tuple
from .models import Team

class TeamRepository:
    """Repositorio para operaciones CRUD de Team"""

    @staticmethod
    def create_team(nombre: str, descripcion: Optional[str] = None) -> Team:
        """Crea un nuevo team en la base de datos"""
        team = Team.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )
        return team

    @staticmethod
    def get_team_by_id(team_id: int) -> Optional[Team]:
        """Obtiene un team por su ID"""
        try:
            return Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return None

    @staticmethod
    def get_team_by_name(nombre: str) -> Optional[Team]:
        """Obtiene un team por su nombre"""
        try:
            return Team.objects.get(nombre=nombre)
        except Team.DoesNotExist:
            return None

    @staticmethod
    def get_all_teams(offset: int = 0, limit: int = 10) -> Tuple[List[Team], int]:
        """Obtiene todos los teams con paginación"""
        queryset = Team.objects.all().order_by('-fecha_creacion')
        total = queryset.count()
        teams = list(queryset[offset:offset + limit])
        return teams, total

    @staticmethod
    def update_team(team_id: int, **kwargs) -> Optional[Team]:
        """Actualiza un team existente"""
        team = TeamRepository.get_team_by_id(team_id)
        if not team:
            return None
        for key, value in kwargs.items():
            if hasattr(team, key) and value is not None:
                setattr(team, key, value)
        team.save()
        return team

    @staticmethod
    def delete_team(team_id: int) -> bool:
        """Elimina un team por su ID"""
        team = TeamRepository.get_team_by_id(team_id)
        if not team:
            return False
        team.delete()
        return True

    @staticmethod
    def exists_by_name(nombre: str) -> bool:
        """Verifica si existe un team con el nombre dado"""
        return Team.objects.filter(nombre=nombre).exists()

    @staticmethod
    def exists_by_id(team_id: int) -> bool:
        """Verifica si existe un team con el ID dado"""
        return Team.objects.filter(id=team_id).exists()
```

**Importante**:
- Usa métodos `@staticmethod`
- Retorna `Optional[Model]` o `None`
- No incluye validaciones de negocio (eso va en Services)
- Solo interactúa con el ORM de Django

---

### 🔷 PASO 4: Crear el Service (services.py)

**Ubicación**: `<app_name>/services.py`

**Qué hacer**:
- Crear clase `<ModelName>Service`
- Implementar lógica de negocio y validaciones
- Usar `Repository` para acceder a datos
- Lanzar excepciones (`ValidationError`, `NotFound`)

**Ejemplo con la app Teams**:

```python
from typing import Dict, Optional
from rest_framework.exceptions import ValidationError, NotFound
from .repository import TeamRepository
from .models import Team

class TeamService:
    """Servicio para manejar la lógica de negocio de Teams"""

    def __init__(self):
        self.repository = TeamRepository()

    def create_team(self, nombre: str, descripcion: Optional[str] = None) -> Team:
        """Crea un nuevo team validando que no exista"""
        # Validar nombre no vacío
        if not nombre or nombre.strip() == "":
            raise ValidationError({"nombre": "El nombre es requerido"})

        # Validar longitud
        if len(nombre) > 255:
            raise ValidationError({"nombre": "Máximo 255 caracteres"})

        # Verificar que no exista
        if self.repository.exists_by_name(nombre):
            raise ValidationError({"nombre": f"Ya existe un team con el nombre '{nombre}'"})

        # Crear
        return self.repository.create_team(
            nombre=nombre.strip(),
            descripcion=descripcion.strip() if descripcion else None
        )

    def get_team_by_id(self, team_id: int) -> Team:
        """Obtiene un team por ID validando que exista"""
        if team_id <= 0:
            raise ValidationError({"id": "El ID debe ser positivo"})

        team = self.repository.get_team_by_id(team_id)
        if not team:
            raise NotFound({"detail": f"No se encontró el team con ID {team_id}"})

        return team

    def get_all_teams(self, offset: int = 0, limit: int = 10) -> Dict:
        """Obtiene todos los teams con paginación"""
        # Validar parámetros
        if offset < 0:
            raise ValidationError({"offset": "Debe ser >= 0"})
        if limit <= 0 or limit > 100:
            raise ValidationError({"limit": "Debe estar entre 1 y 100"})

        teams, total = self.repository.get_all_teams(offset, limit)

        return {
            "teams": teams,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_next": (offset + limit) < total,
            "has_previous": offset > 0
        }

    def update_team(self, team_id: int, nombre: Optional[str] = None,
                    descripcion: Optional[str] = None) -> Team:
        """Actualiza un team validando datos"""
        # Verificar que exista
        if not self.repository.exists_by_id(team_id):
            raise NotFound({"detail": f"No se encontró el team con ID {team_id}"})

        # Validar que haya algo para actualizar
        if nombre is None and descripcion is None:
            raise ValidationError({"detail": "Debe proporcionar al menos un campo"})

        # Validar nombre si se proporciona
        if nombre is not None:
            if nombre.strip() == "":
                raise ValidationError({"nombre": "No puede estar vacío"})
            # Verificar que no exista otro team con ese nombre
            existing = self.repository.get_team_by_name(nombre.strip())
            if existing and existing.id != team_id:
                raise ValidationError({"nombre": f"Ya existe otro team con el nombre '{nombre}'"})

        # Actualizar
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre.strip()
        if descripcion is not None:
            update_data['descripcion'] = descripcion.strip() if descripcion else None

        return self.repository.update_team(team_id, **update_data)

    def delete_team(self, team_id: int) -> Dict:
        """Elimina un team validando que exista"""
        team = self.repository.get_team_by_id(team_id)
        if not team:
            raise NotFound({"detail": f"No se encontró el team con ID {team_id}"})

        team_name = team.nombre
        self.repository.delete_team(team_id)

        return {
            "message": f"Team '{team_name}' eliminado exitosamente",
            "id": team_id
        }
```

**Importante**:
- Siempre validar antes de llamar al repository
- Lanzar `ValidationError` para errores 400
- Lanzar `NotFound` para errores 404
- No acceder directamente a models, usar repository

---

### 🔷 PASO 5: Crear las Views (views.py)

**Ubicación**: `<app_name>/views.py`

**Qué hacer**:
- Crear `ViewSet` heredando de `viewsets.ViewSet`
- Implementar métodos HTTP (create, list, retrieve, update, delete)
- Documentar con `@swagger_auto_schema`
- Usar schemas para validación y serialización

**Ejemplo con la app Teams**:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import TeamService
from .schemas import TeamCreateSchema, TeamReadSchema, TeamUpdateSchema

class TeamViewSet(viewsets.ViewSet):
    """ViewSet para operaciones CRUD de Teams"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = TeamService()

    @swagger_auto_schema(
        operation_summary="Crear un nuevo team",
        operation_description="Crea un nuevo team. El nombre debe ser único.",
        request_body=TeamCreateSchema,
        responses={
            201: openapi.Response("Team creado", TeamReadSchema),
            400: "Datos inválidos"
        },
        tags=['Teams']
    )
    def create(self, request):
        """POST /api/teams/"""
        serializer = TeamCreateSchema(data=request.data)
        serializer.is_valid(raise_exception=True)

        team = self.service.create_team(
            nombre=serializer.validated_data['nombre'],
            descripcion=serializer.validated_data.get('descripcion')
        )

        response_serializer = TeamReadSchema(team)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Listar todos los teams",
        manual_parameters=[
            openapi.Parameter('offset', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=0),
            openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=10),
        ],
        responses={200: "Lista de teams"},
        tags=['Teams']
    )
    def list(self, request):
        """GET /api/teams/"""
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 10))

        result = self.service.get_all_teams(offset=offset, limit=limit)
        teams_serializer = TeamReadSchema(result['teams'], many=True)

        return Response({
            "teams": teams_serializer.data,
            "total": result['total'],
            "offset": result['offset'],
            "limit": result['limit'],
            "has_next": result['has_next'],
            "has_previous": result['has_previous']
        })

    @swagger_auto_schema(
        operation_summary="Obtener team por ID",
        responses={200: TeamReadSchema, 404: "No encontrado"},
        tags=['Teams']
    )
    def retrieve(self, request, pk=None):
        """GET /api/teams/{id}/"""
        team = self.service.get_team_by_id(int(pk))
        serializer = TeamReadSchema(team)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar team",
        request_body=TeamUpdateSchema,
        responses={200: TeamReadSchema, 404: "No encontrado"},
        tags=['Teams']
    )
    def partial_update(self, request, pk=None):
        """PATCH /api/teams/{id}/"""
        serializer = TeamUpdateSchema(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        team = self.service.update_team(
            team_id=int(pk),
            nombre=serializer.validated_data.get('nombre'),
            descripcion=serializer.validated_data.get('descripcion')
        )

        response_serializer = TeamReadSchema(team)
        return Response(response_serializer.data)

    @swagger_auto_schema(
        operation_summary="Eliminar team",
        responses={200: "Team eliminado", 404: "No encontrado"},
        tags=['Teams']
    )
    def destroy(self, request, pk=None):
        """DELETE /api/teams/{id}/"""
        result = self.service.delete_team(int(pk))
        return Response(result)

    # Endpoint personalizado
    @action(detail=False, methods=['get'], url_path='by-name')
    @swagger_auto_schema(
        operation_summary="Buscar team por nombre",
        manual_parameters=[
            openapi.Parameter('nombre', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        tags=['Teams']
    )
    def get_by_name(self, request):
        """GET /api/teams/by-name/?nombre={nombre}"""
        nombre = request.query_params.get('nombre')
        team = self.service.get_team_by_name(nombre)
        serializer = TeamReadSchema(team)
        return Response(serializer.data)
```

**Métodos del ViewSet**:
- `create()` → POST `/api/teams/`
- `list()` → GET `/api/teams/`
- `retrieve()` → GET `/api/teams/{id}/`
- `partial_update()` → PATCH `/api/teams/{id}/`
- `destroy()` → DELETE `/api/teams/{id}/`
- `@action()` → Endpoints personalizados

**Importante**:
- Los ViewSets deben crearse **antes** que los routers
- Cada método corresponde a una operación HTTP
- `@swagger_auto_schema` documenta cada endpoint
- El servicio se inicializa en `__init__()`

---

### 🔷 PASO 6: Crear el Router (routers.py)

**Ubicación**: `<app_name>/routers.py`

**Qué hacer**:
- Configurar el router de DRF
- Registrar el ViewSet (que ya fue creado en el paso anterior)
- Exportar instancia del router

**Ejemplo con la app Teams**:

```python
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet

def get_teams_router():
    """Configura y retorna el router para Teams"""
    router = DefaultRouter()
    router.register(r'teams', TeamViewSet, basename='team')
    return router

# Instancia del router
teams_router = get_teams_router()
```

**Importante**:
- Este paso se hace **DESPUÉS** de crear las Views
- Importa el `TeamViewSet` que creaste en views.py
- Usa `DefaultRouter()` de DRF
- El `basename` se usa para generar nombres de URLs
- El primer parámetro (`'teams'`) define el prefijo de la URL

**¿Por qué este orden?**

En Django REST Framework:
1. **Views.py** define los ViewSets (la lógica)
2. **Routers.py** registra los ViewSets (la configuración de rutas)

Esto es diferente a **FastAPI** donde el router se define directamente en el archivo de rutas con decoradores `@router.get()`, `@router.post()`, etc.

---

## 🎯 ¿Dónde se Definen las Rutas? (Diferencia Clave con FastAPI)

Esta es una pregunta muy importante si vienes de **FastAPI**. En Django REST Framework las rutas NO se definen explícitamente, sino que se **generan automáticamente**.

### La Respuesta Corta:
**Las rutas NO se definen explícitamente (como en FastAPI). Se GENERAN AUTOMÁTICAMENTE por el `DefaultRouter` de DRF basándose en convenciones de nombres.**

---

### 📊 Mapeo Automático de Rutas

Cuando haces esto en `routers.py`:

```python
router.register(r'teams', TeamViewSet, basename='team')
                 ^^^^^^   ^^^^^^^^^^^  ^^^^^^^^^^^^
                   |            |            |
                   |            |            +-- Prefijo para nombres de rutas
                   |            +-- El ViewSet con los métodos
                   +-- Prefijo de URL
```

El `DefaultRouter` **automáticamente** crea estas rutas:

| Método en ViewSet | HTTP Método | URL Generada | Nombre de Ruta |
|-------------------|-------------|--------------|----------------|
| `list()` | **GET** | `/api/teams/` | `team-list` |
| `create()` | **POST** | `/api/teams/` | `team-list` |
| `retrieve()` | **GET** | `/api/teams/{pk}/` | `team-detail` |
| `partial_update()` | **PATCH** | `/api/teams/{pk}/` | `team-detail` |
| `destroy()` | **DELETE** | `/api/teams/{pk}/` | `team-detail` |
| `@action` (custom) | **GET** | `/api/teams/by-name/` | `team-get-by-name` |

---

### 🔍 Desglose: ¿Cómo se Genera una Ruta Completa?

#### 1️⃣ **views.py** - Define la lógica (SIN definir rutas)

```python
class TeamViewSet(viewsets.ViewSet):
    def create(self, request):  # ← El NOMBRE del método importa
        """POST /api/teams/"""  # ← Esto es solo documentación
        # Lógica...
```

**¿Por qué se llama `create`?**

Porque DRF tiene una **convención de nombres**:
- Método llamado `create()` → Lo mapea automáticamente a `POST /teams/`
- Método llamado `list()` → Lo mapea automáticamente a `GET /teams/`
- Método llamado `retrieve()` → Lo mapea automáticamente a `GET /teams/{pk}/`

**Importante**: El nombre del método NO es arbitrario. DRF reconoce estos nombres específicos.

---

#### 2️⃣ **routers.py** - Genera las rutas automáticamente

```python
router.register(r'teams', TeamViewSet, basename='team')
```

Esta línea internamente hace esto:

```python
# LO QUE EL ROUTER HACE AUTOMÁTICAMENTE:
{
    'list':           ('GET',    'teams/'),           # → teams/
    'create':         ('POST',   'teams/'),           # → teams/
    'retrieve':       ('GET',    'teams/{pk}/'),      # → teams/1/
    'partial_update': ('PATCH',  'teams/{pk}/'),      # → teams/1/
    'destroy':        ('DELETE', 'teams/{pk}/'),      # → teams/1/
}
```

**NO necesitas escribir** `@router.post("/teams/")` como en FastAPI.

---

#### 3️⃣ **config/urls.py** - Agrega el prefijo global

```python
path('api/', include(teams_router.urls))
     ^^^^^
       |
       +-- Prefijo global para todas las rutas del router
```

**Resultado final**:
- Router genera: `teams/`
- urls.py agrega: `api/`
- **URL completa**: `/api/teams/`

---

### 📋 Convenciones de Nombres en DRF

Estos son los nombres "mágicos" que DRF reconoce automáticamente:

| Nombre del Método | HTTP | Ruta Generada | Descripción |
|-------------------|------|---------------|-------------|
| `list()` | GET | `/resource/` | Listar todos los recursos |
| `create()` | POST | `/resource/` | Crear un nuevo recurso |
| `retrieve()` | GET | `/resource/{pk}/` | Obtener un recurso específico |
| `update()` | PUT | `/resource/{pk}/` | Actualizar completo |
| `partial_update()` | PATCH | `/resource/{pk}/` | Actualizar parcial |
| `destroy()` | DELETE | `/resource/{pk}/` | Eliminar un recurso |

**Si usas estos nombres exactos, DRF automáticamente los mapea a las rutas correctas.**

---

## 🔑 ¿Cómo Sabe DRF el Método HTTP y si Necesita `{id}`?

Esta es otra pregunta crítica si vienes de FastAPI. Cuando miras un método como `destroy()`:

```python
def destroy(self, request, pk=None):
    """DELETE /api/teams/{id}/"""
    result = self.service.delete_team(int(pk))
    return Response(result)
```

**Te preguntas**: "¿Dónde dice que es DELETE? ¿Dónde dice que la ruta es `/api/teams/{id}/`?"

### La Respuesta: Convención de Firmas de Métodos

DRF lo sabe por **DOS cosas**:

1. **El NOMBRE del método** (`destroy`, `create`, `list`, etc.)
2. **La FIRMA del método** (si tiene parámetro `pk` o no)

---

### 📊 Tabla de Mapeo Interno de DRF

| Nombre del Método | Parámetros | HTTP Método | URL Pattern | Explicación |
|-------------------|------------|-------------|-------------|-------------|
| `list(self, request)` | **SIN `pk`** | GET | `/teams/` | Lista = colección, no necesita ID |
| `create(self, request)` | **SIN `pk`** | POST | `/teams/` | Crear = nuevo recurso, no tiene ID aún |
| `retrieve(self, request, pk=None)` | **CON `pk`** | GET | `/teams/{pk}/` | Obtener uno = necesita ID |
| `update(self, request, pk=None)` | **CON `pk`** | PUT | `/teams/{pk}/` | Actualizar completo = necesita ID |
| `partial_update(self, request, pk=None)` | **CON `pk`** | PATCH | `/teams/{pk}/` | Actualizar parcial = necesita ID |
| `destroy(self, request, pk=None)` | **CON `pk`** | DELETE | `/teams/{pk}/` | Eliminar = necesita ID |

**Patrón**:
- Métodos **SIN `pk`** → Operan sobre la **colección** → URL: `/teams/`
- Métodos **CON `pk`** → Operan sobre un **recurso específico** → URL: `/teams/{pk}/`

---

### 🔍 Ejemplo Concreto: ¿Por qué `destroy` es DELETE?

Cuando el `DefaultRouter` ve esto:

```python
class TeamViewSet(viewsets.ViewSet):
    def destroy(self, request, pk=None):
        #   ^^^^^^^          ^^^^^^^
        #      |                |
        #      |                +-- (2) Tiene 'pk' → {pk} en URL
        #      +-- (1) Nombre 'destroy' → DELETE
        pass
```

**El router hace esto internamente**:

1. **Ve el nombre**: `destroy` → "Es un método DELETE" (está hardcodeado en el código fuente de DRF)
2. **Ve el parámetro**: `pk=None` → "Necesita un ID en la URL"
3. **Genera la ruta**: `DELETE /teams/{pk}/`

---

### 🔍 Comparación: Métodos CON y SIN `pk`

#### Métodos **SIN `pk`** → URL sin `{id}`

```python
def list(self, request):  # ← NO tiene 'pk'
    """GET /api/teams/"""
    pass

def create(self, request):  # ← NO tiene 'pk'
    """POST /api/teams/"""
    pass
```

**DRF entiende**: "No tienen `pk`, entonces operan sobre la **colección** (`/teams/`)"

---

#### Métodos **CON `pk`** → URL con `{id}`

```python
def retrieve(self, request, pk=None):  # ← Tiene 'pk'
    """GET /api/teams/{id}/"""
    team = self.service.get_team_by_id(int(pk))
    pass

def destroy(self, request, pk=None):  # ← Tiene 'pk'
    """DELETE /api/teams/{id}/"""
    result = self.service.delete_team(int(pk))
    pass

def partial_update(self, request, pk=None):  # ← Tiene 'pk'
    """PATCH /api/teams/{id}/"""
    team = self.service.update_team(team_id=int(pk), ...)
    pass
```

**DRF entiende**: "Tienen `pk`, entonces operan sobre un **recurso específico** (`/teams/{pk}/`)"

---

### 📖 El Código Fuente Real de DRF

Si quieres ver la "magia", aquí está el código real de DRF (simplificado):

```python
# rest_framework/routers.py (código fuente de Django REST Framework)
class SimpleRouter(BaseRouter):
    routes = [
        # Rutas sin {pk} (colección)
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',      # ← list → GET /teams/
                'post': 'create'    # ← create → POST /teams/
            },
            name='{basename}-list',
            detail=False,
        ),
        # Rutas con {pk} (detalle)
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',         # ← retrieve → GET /teams/{pk}/
                'put': 'update',           # ← update → PUT /teams/{pk}/
                'patch': 'partial_update', # ← partial_update → PATCH /teams/{pk}/
                'delete': 'destroy',       # ← destroy → DELETE /teams/{pk}/
            },
            name='{basename}-detail',
            detail=True,
        ),
    ]
```

**Ahí está la tabla mágica** en el código fuente de DRF:

```python
mapping={
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',  # ← destroy → DELETE (hardcodeado en DRF)
}
```

---

### 🆚 Comparación: FastAPI vs DRF

#### En **FastAPI** (TODO Explícito):

```python
@router.delete("/teams/{team_id}")  # ← TODO está EXPLÍCITO
#      ^^^^^^  ^^^^^^^^^^^^^^^^^^
#        |            |
#        |            +-- Ruta con parámetro
#        +-- Método HTTP DELETE
def delete_team(team_id: int):
    pass
```

**Tú dices explícitamente**: "Es DELETE y la ruta es `/teams/{team_id}`"

---

#### En **Django REST Framework** (Por Convención):

```python
def destroy(self, request, pk=None):  # ← TODO está en CONVENCIÓN
#   ^^^^^^^          ^^^^^^^
#      |                |
#      |                +-- Parámetro 'pk' → URL tendrá {pk}
#      +-- Nombre 'destroy' → Método DELETE (definido en DRF)
    pass
```

**DRF deduce automáticamente**:
- "Se llama `destroy`" → Es DELETE (según tabla interna de DRF)
- "Tiene parámetro `pk`" → La URL necesita `{pk}`

**Resultado**: `DELETE /teams/{pk}/`

---

### 🎯 Ejemplo Práctico Completo

```python
# views.py
class TeamViewSet(viewsets.ViewSet):
    def destroy(self, request, pk=None):
        result = self.service.delete_team(int(pk))
        return Response(result)

# routers.py
router.register(r'teams', TeamViewSet, basename='team')
#                 ^^^^^^
#                   +-- Prefijo de URL

# config/urls.py
path('api/', include(teams_router.urls))
#    ^^^^
#      +-- Prefijo global
```

**Proceso de generación de ruta**:

1. **Nombre del método**: `destroy` → DRF busca en su tabla interna → DELETE
2. **Firma del método**: `pk=None` → DRF sabe que necesita `{pk}` en URL
3. **Prefijo en router**: `'teams'` → Ruta base: `/teams/`
4. **Prefijo en urls.py**: `'api/'` → Prefijo global: `/api/`

**Resultado final**: `DELETE /api/teams/{pk}/`

**Cuando llamas**:
```bash
DELETE /api/teams/5/
```

**DRF lo mapea a**:
```python
TeamViewSet.destroy(request, pk=5)
```

---

### ✅ Resumen: ¿Cómo Sabe DRF?

#### Pregunta:
> "No veo que `destroy` es DELETE ni que la ruta tiene `{id}`"

#### Respuesta:

**NO lo ves porque es CONVENCIÓN, no configuración explícita.**

| Aspecto | Cómo lo sabe DRF |
|---------|------------------|
| **Método HTTP** | Por el NOMBRE del método (`destroy` = DELETE, según tabla interna) |
| **URL con {pk}** | Por la FIRMA del método (tiene parámetro `pk`) |
| **Ruta base** | Por el prefijo en `router.register(r'teams', ...)` |
| **Prefijo global** | Por `path('api/', ...)` en urls.py |

**Convenciones estrictas**:
- `list` = GET sin `{pk}`
- `create` = POST sin `{pk}`
- `retrieve` = GET con `{pk}`
- `update` = PUT con `{pk}`
- `partial_update` = PATCH con `{pk}`
- `destroy` = DELETE con `{pk}`

**Si usas estos nombres exactos, DRF automáticamente mapea todo.**

---

## 🎨 Endpoints Personalizados: ¿Qué Pasa con `get_by_name`?

Hasta ahora hemos visto las convenciones estándar de DRF (`list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`). Pero, ¿qué pasa cuando necesitas un endpoint que **NO sigue las convenciones**?

Por ejemplo, en nuestro proyecto tenemos:

```
GET /api/teams/by-name/?nombre=Team%20Alpha
```

Este endpoint:
- ❌ No es `list` (que sería `GET /teams/`)
- ❌ No es `retrieve` (que sería `GET /teams/{pk}/`)
- ✅ Es una búsqueda **personalizada** por nombre

**¿Cómo se define esto?**

---

### 🔧 El Decorador `@action`

Para endpoints personalizados que **NO** siguen las convenciones de DRF, usas el decorador `@action`:

```python
@action(detail=False, methods=['get'], url_path='by-name')
#       ^^^^^^^^^^^^^  ^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^
#            |                |                 |
#            |                |                 +-- (3) Nombre personalizado de la ruta
#            |                +-- (2) Métodos HTTP permitidos
#            +-- (1) ¿Requiere {pk}?
def get_by_name(self, request):
    """GET /api/teams/by-name/?nombre={nombre}"""
    nombre = request.query_params.get('nombre')
    team = self.service.get_team_by_name(nombre)
    serializer = TeamReadSchema(team)
    return Response(serializer.data)
```

---

### 📋 Parámetros de `@action` Explicados

#### 1️⃣ `detail` - ¿Requiere `{pk}` en la URL?

| Valor | URL Generada | Cuándo usarlo |
|-------|--------------|---------------|
| `detail=False` | `/teams/by-name/` | Acción sobre la **colección** (no necesita ID) |
| `detail=True` | `/teams/{pk}/by-name/` | Acción sobre un **recurso específico** (necesita ID) |

**Ejemplos**:

```python
# detail=False → Sin {pk}
@action(detail=False, methods=['get'], url_path='by-name')
def get_by_name(self, request):
    # GET /api/teams/by-name/?nombre=Alpha
    pass

# detail=True → Con {pk}
@action(detail=True, methods=['post'], url_path='add-member')
def add_member(self, request, pk=None):
    # POST /api/teams/5/add-member/
    # Agrega un miembro al team con ID 5
    pass
```

---

#### 2️⃣ `methods` - Métodos HTTP Permitidos

```python
@action(detail=False, methods=['get'])
# Solo permite GET

@action(detail=False, methods=['get', 'post'])
# Permite GET y POST

@action(detail=True, methods=['post', 'delete'])
# Permite POST y DELETE (con {pk})
```

**Puedes manejar múltiples métodos en la misma acción**:

```python
@action(detail=True, methods=['post', 'delete'], url_path='members')
def manage_members(self, request, pk=None):
    if request.method == 'POST':
        # Agregar miembro
        pass
    elif request.method == 'DELETE':
        # Eliminar miembro
        pass
```

---

#### 3️⃣ `url_path` - Nombre Personalizado de la Ruta

```python
@action(detail=False, methods=['get'], url_path='by-name')
#                                      ^^^^^^^^^^^^^^^
#                                            |
#                                            +-- La ruta será /teams/by-name/
def get_by_name(self, request):
    pass

@action(detail=False, methods=['get'], url_path='search')
#                                      ^^^^^^^^^^^^^^^
#                                            |
#                                            +-- La ruta será /teams/search/
def search_teams(self, request):
    pass

@action(detail=True, methods=['post'], url_path='activate')
#                                      ^^^^^^^^^^^^^^^^^^
#                                            |
#                                            +-- La ruta será /teams/{pk}/activate/
def activate_team(self, request, pk=None):
    pass
```

**Si NO especificas `url_path`**, DRF usa el nombre de la función:

```python
@action(detail=False, methods=['get'])
def get_by_name(self, request):
    # URL: /api/teams/get_by_name/  (usa el nombre de la función)
    pass
```

---

### 🔍 Ejemplo Completo: `get_by_name`

Aquí está nuestro endpoint personalizado completo:

```python
class TeamViewSet(viewsets.ViewSet):
    # ... métodos estándar (list, create, etc.)

    @action(detail=False, methods=['get'], url_path='by-name')
    def get_by_name(self, request):
        """
        GET /api/teams/by-name/?nombre={nombre}
        Busca un team por nombre exacto
        """
        nombre = request.query_params.get('nombre')
        team = self.service.get_team_by_name(nombre)
        serializer = TeamReadSchema(team)
        return Response(serializer.data)
```

**¿Cómo se genera la ruta?**

1. **Prefijo del router**: `'teams'` (de `router.register(r'teams', ...)`)
2. **Prefijo global**: `'api/'` (de `path('api/', ...)`)
3. **detail=False**: No añade `{pk}`
4. **url_path**: `'by-name'` (nombre personalizado)

**Resultado**: `GET /api/teams/by-name/`

**Nombre de ruta generado**: `team-get-by-name` (basename + nombre del método)

---

### 🆚 Comparación: Método Estándar vs `@action`

#### Método Estándar (Convención de DRF):

```python
def retrieve(self, request, pk=None):
    # ← NO necesita @action
    # ← DRF automáticamente mapea a GET /teams/{pk}/
    team = self.service.get_team_by_id(int(pk))
    return Response(TeamReadSchema(team).data)
```

**Sin decorador** → DRF lo mapea automáticamente

---

#### Endpoint Personalizado (Necesita `@action`):

```python
@action(detail=False, methods=['get'], url_path='by-name')
# ← NECESITA @action porque NO es una convención estándar
def get_by_name(self, request):
    # ← DRF genera GET /teams/by-name/ según @action
    team = self.service.get_team_by_name(nombre)
    return Response(TeamReadSchema(team).data)
```

**Con decorador** → Defines tú la ruta personalizada

---

### 📖 Más Ejemplos de `@action`

#### Ejemplo 1: Búsqueda con filtros

```python
@action(detail=False, methods=['get'], url_path='search')
def search(self, request):
    """
    GET /api/teams/search/?q=alpha&active=true
    Búsqueda con múltiples filtros
    """
    query = request.query_params.get('q', '')
    active = request.query_params.get('active')
    # Lógica de búsqueda...
    return Response(results)
```

---

#### Ejemplo 2: Acción sobre un recurso específico

```python
@action(detail=True, methods=['post'], url_path='activate')
#       ^^^^^^^^^^^
#          |
#          +-- detail=True → Necesita {pk}
def activate(self, request, pk=None):
    """
    POST /api/teams/5/activate/
    Activa el team con ID 5
    """
    team = self.service.get_team_by_id(int(pk))
    team.active = True
    team.save()
    return Response({'status': 'activated'})
```

---

#### Ejemplo 3: Múltiples métodos HTTP

```python
@action(detail=True, methods=['get', 'post', 'delete'], url_path='members')
def members(self, request, pk=None):
    """
    GET /api/teams/5/members/ - Listar miembros
    POST /api/teams/5/members/ - Agregar miembro
    DELETE /api/teams/5/members/ - Eliminar miembro
    """
    if request.method == 'GET':
        # Listar miembros del team
        return Response(members_list)
    elif request.method == 'POST':
        # Agregar miembro al team
        return Response({'status': 'member added'})
    elif request.method == 'DELETE':
        # Eliminar miembro del team
        return Response({'status': 'member removed'})
```

---

#### Ejemplo 4: Estadísticas (sin {pk})

```python
@action(detail=False, methods=['get'], url_path='statistics')
def statistics(self, request):
    """
    GET /api/teams/statistics/
    Obtiene estadísticas de todos los teams
    """
    stats = {
        'total_teams': Team.objects.count(),
        'active_teams': Team.objects.filter(active=True).count(),
        # ...
    }
    return Response(stats)
```

---

### ✅ Resumen: `@action` para Endpoints Personalizados

| Aspecto | Métodos Estándar | Endpoints con `@action` |
|---------|------------------|-------------------------|
| **Decorador** | No necesita | Requiere `@action` |
| **Rutas** | Automáticas (por convención) | Personalizadas (tú las defines) |
| **Nombres** | `list`, `create`, `retrieve`, etc. | Cualquier nombre |
| **URL con {pk}** | Según firma del método | Según `detail=True/False` |
| **Métodos HTTP** | Predefinidos por DRF | Los que especifiques en `methods=[]` |
| **Nombre de ruta** | Generado automáticamente | `{basename}-{nombre-metodo}` |

---

### 🎯 Cuándo Usar `@action`

**USA `@action` cuando**:
- ✅ Necesitas un endpoint que NO es CRUD estándar
- ✅ Quieres búsquedas personalizadas (`/teams/by-name/`, `/teams/search/`)
- ✅ Necesitas acciones específicas (`/teams/{pk}/activate/`, `/teams/{pk}/export/`)
- ✅ Quieres estadísticas o agregaciones (`/teams/statistics/`)
- ✅ Operaciones batch (`/teams/bulk-update/`)

**NO uses `@action` para**:
- ❌ Listar todos (`list`)
- ❌ Crear (`create`)
- ❌ Obtener por ID (`retrieve`)
- ❌ Actualizar (`update`, `partial_update`)
- ❌ Eliminar (`destroy`)

**Para operaciones CRUD estándar, usa los métodos con convención de DRF.**

---

### 💡 Conclusión sobre `@action`

**Diferencia clave**:

- **Métodos estándar** (`list`, `create`, etc.): DRF mapea automáticamente
- **Métodos con `@action`**: Tú defines la ruta, método HTTP, y si necesita `{pk}`

**`get_by_name` necesita `@action` porque**:
1. No es una operación CRUD estándar
2. La ruta `/teams/by-name/` no sigue la convención
3. Necesita parámetros de query (`?nombre=...`)

**Código**:
```python
@action(detail=False, methods=['get'], url_path='by-name')
#       ^^^^^^^^^^^^^ ^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^
#          |               |                  |
#          |               |                  +-- Ruta personalizada
#          |               +-- Método HTTP GET
#          +-- Sin {pk} (sobre la colección)
def get_by_name(self, request):
    pass
```

**Resultado**: `GET /api/teams/by-name/?nombre=...`

---

### 🆚 Comparación Visual: FastAPI vs Django REST Framework

#### En **FastAPI** (Rutas Explícitas):

```python
# routers.py en FastAPI
from fastapi import APIRouter

router = APIRouter()

@router.post("/teams/")  # ← RUTA EXPLÍCITA en el decorador
def create_team(...):
    pass

@router.get("/teams/")  # ← RUTA EXPLÍCITA en el decorador
def read_teams(...):
    pass

@router.get("/teams/{team_id}")  # ← RUTA EXPLÍCITA en el decorador
def read_team(...):
    pass
```

**En FastAPI**: La ruta está **EXPLÍCITA** en el decorador `@router.post("/teams/")`.

---

#### En **Django REST Framework** (Rutas por Convención):

**Paso 1 - views.py (Convención de nombres)**:
```python
class TeamViewSet(viewsets.ViewSet):
    def create(self, request):  # ← Nombre "create" = POST
        pass

    def list(self, request):    # ← Nombre "list" = GET colección
        pass

    def retrieve(self, request, pk=None):  # ← Nombre "retrieve" = GET detalle
        pass
```

**Paso 2 - routers.py (Registro del ViewSet)**:
```python
router.register(r'teams', TeamViewSet, basename='team')
#                 ^^^^^^
#                   |
#                   +-- Solo defines el PREFIJO de URL
```

**Paso 3 - config/urls.py (Prefijo global)**:
```python
path('api/', include(teams_router.urls))
#    ^^^^
#      +-- Prefijo global
```

**Resultado Automático**:
- `POST /api/teams/` → `TeamViewSet.create()`
- `GET /api/teams/` → `TeamViewSet.list()`
- `GET /api/teams/{id}/` → `TeamViewSet.retrieve()`

**En DRF**: Las rutas se **GENERAN AUTOMÁTICAMENTE** basándose en el nombre de los métodos.

---

### ✅ Resumen: ¿Dónde están las Rutas?

#### Pregunta: "No veo `@router.post("/teams/")` en ningún lado, ¿dónde está la ruta?"

**Respuesta**: En DRF **no existe** ese decorador. Las rutas se generan así:

1. **Nombre del método** en ViewSet (`create`, `list`, etc.)
2. **Prefijo** en `router.register(r'teams', ...)`
3. **Prefijo global** en `path('api/', ...)`

**Fórmula**:

```
URL completa = [config/urls.py] + [router.register] + [convención DRF]
             = 'api/'           + 'teams'           + '/'
             = /api/teams/
```

#### Comparación Final:

| Aspecto | FastAPI | Django REST Framework |
|---------|---------|----------------------|
| Definición de ruta | **Explícita** en decorador | **Automática** por convención |
| Decorador | `@router.post("/teams/")` | `def create(self, request):` |
| Ventaja | Muy claro y directo | Menos código, más consistente |
| Desventaja | Más verboso | Requiere conocer convenciones |

---

### 🔍 Ver Todas las Rutas Generadas

Si quieres ver todas las rutas que el router generó automáticamente, ejecuta:

```bash
python show_routes.py
```

Esto te mostrará:
- Todas las URLs generadas
- El mapeo de métodos del ViewSet a URLs
- Los nombres de las rutas
- Los métodos HTTP permitidos

**Ejemplo de salida**:
```
MAPEO DE MÉTODOS DEL VIEWSET A URLs:
================================================================================

  list()               → GET     /api/teams/               (Listar todos los teams)
  create()             → POST    /api/teams/               (Crear un nuevo team)
  retrieve()           → GET     /api/teams/{id}/          (Obtener team por ID)
  partial_update()     → PATCH   /api/teams/{id}/          (Actualizar team parcialmente)
  destroy()            → DELETE  /api/teams/{id}/          (Eliminar team)
  get_by_name()        → GET     /api/teams/by-name/       (Buscar team por nombre)
```

---

### 💡 Conclusión

**La diferencia clave**:
- En **FastAPI**: Defines las rutas explícitamente con decoradores
- En **Django REST Framework**: Las rutas se generan automáticamente basándose en:
  1. Nombres de métodos del ViewSet
  2. Prefijo en `router.register()`
  3. Prefijo en `config/urls.py`

**Por eso no ves** `POST /api/teams/` escrito en ningún lado del código. Todo es **automático y basado en convenciones**.

---

### 📚 Organización de Documentación Swagger

**¿Por qué separar la documentación?**

En **FastAPI**, la documentación Swagger se genera automáticamente a partir de los tipos de Python (type hints) y los modelos Pydantic. No necesitas escribir decoradores manualmente.

En **Django REST Framework con drf-yasg**, necesitas escribir MANUALMENTE cada decorador `@swagger_auto_schema` para cada endpoint. Esto puede hacer que `views.py` crezca mucho.

**Comparación de tamaños**:
- **Antes** (documentación inline en views.py): 308 líneas
- **Después** (documentación separada en docs.py): 148 líneas en views.py + 208 líneas en docs.py
- **Reducción en views.py**: 52% menos código

**Opciones para organizar la documentación**:

1. **Inline** (documentación en views.py directamente)
   - ✅ **Ventaja**: Todo en un solo archivo
   - ❌ **Desventaja**: views.py se vuelve muy grande (300+ líneas)
   - 📌 **Usar cuando**: Proyecto pequeño con pocos endpoints (< 5)

2. **docs.py** (archivo separado en la app)
   - ✅ **Ventaja**: views.py limpio, fácil de mantener
   - ✅ **Ventaja**: Separación clara entre lógica y documentación
   - ❌ **Desventaja**: Un archivo extra por app
   - 📌 **Usar cuando**: Proyecto mediano/grande (recomendado para la mayoría de casos)

3. **docs/** (carpeta con múltiples archivos)
   - ✅ **Ventaja**: Máxima organización (un archivo por endpoint)
   - ❌ **Desventaja**: Muchos archivos pequeños
   - 📌 **Usar cuando**: Proyecto muy grande con documentación compleja

**Implementación elegida: docs.py**

Este proyecto usa la opción 2 (docs.py) porque:
- Mantiene views.py enfocado solo en la lógica HTTP
- Centraliza toda la documentación Swagger en un solo lugar
- Es fácil de mantener y escala bien

**Ejemplo de migración**:

**❌ ANTES (inline en views.py)**:
```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TeamViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="Crear un nuevo team",
        operation_description="Crea un nuevo team en la base de datos...",
        request_body=TeamCreateSchema,
        responses={
            201: openapi.Response(
                description="Team creado exitosamente",
                schema=TeamReadSchema
            ),
            400: openapi.Response(
                description="Datos inválidos o el team ya existe",
                examples={"application/json": {...}}
            )
        },
        tags=['Teams']
    )
    def create(self, request):
        """POST /api/teams/ - Crea un nuevo team"""
        # Lógica de negocio aquí...
```

**✅ DESPUÉS (separado en docs.py + views.py)**:

**teams/docs.py**:
```python
"""
Documentación Swagger para endpoints de Teams
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .schemas import TeamCreateSchema, TeamReadSchema, TeamUpdateSchema

# ==================== CREATE TEAM ====================
create_team_docs = swagger_auto_schema(
    operation_summary="Crear un nuevo team",
    operation_description="Crea un nuevo team en la base de datos. El nombre debe ser único.",
    request_body=TeamCreateSchema,
    responses={
        201: openapi.Response(
            description="Team creado exitosamente",
            schema=TeamReadSchema
        ),
        400: openapi.Response(
            description="Datos inválidos o el team ya existe",
            examples={"application/json": {"nombre": ["Ya existe..."]}}
        )
    },
    tags=['Teams']
)

# Otros decoradores: list_teams_docs, retrieve_team_docs, etc.
```

**teams/views.py**:
```python
from .docs import (
    create_team_docs,
    list_teams_docs,
    retrieve_team_docs,
    update_team_docs,
    delete_team_docs,
    get_by_name_docs
)

class TeamViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = TeamService()

    @create_team_docs  # ← Documentación externa
    def create(self, request):
        """POST /api/teams/ - Crea un nuevo team"""
        # Solo lógica de negocio, SIN decoradores largos
        serializer = TeamCreateSchema(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = self.service.create_team(
            nombre=serializer.validated_data['nombre'],
            descripcion=serializer.validated_data.get('descripcion')
        )
        response_serializer = TeamReadSchema(team)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
```

**Beneficios de esta separación**:
1. **views.py**: Solo lógica HTTP (request/response)
2. **docs.py**: Solo documentación Swagger
3. **Fácil de leer**: Menos líneas por archivo
4. **Fácil de mantener**: Cambios en documentación no afectan lógica
5. **Escalable**: Agregar nuevos endpoints no hace crecer views.py

**Pasos para crear docs.py**:

1. **Crear el archivo** `teams/docs.py`
2. **Importar dependencias**:
   ```python
   from drf_yasg import openapi
   from drf_yasg.utils import swagger_auto_schema
   from .schemas import TeamCreateSchema, TeamReadSchema, TeamUpdateSchema
   ```
3. **Crear decoradores** (uno por endpoint):
   ```python
   create_team_docs = swagger_auto_schema(...)
   list_teams_docs = swagger_auto_schema(...)
   retrieve_team_docs = swagger_auto_schema(...)
   ```
4. **Importar en views.py**:
   ```python
   from .docs import create_team_docs, list_teams_docs, ...
   ```
5. **Aplicar decoradores**:
   ```python
   @create_team_docs
   def create(self, request):
       ...
   ```

**Estructura final de la app**:
```
teams/
├── __init__.py
├── models.py          # Modelos de base de datos
├── schemas.py         # Serializers (Create, Read, Update)
├── repository.py      # Capa de acceso a datos
├── services.py        # Lógica de negocio
├── docs.py           # ← Documentación Swagger (NUEVO)
├── views.py          # Controllers (solo lógica HTTP)
└── routers.py        # Configuración de rutas
```

---

### 🔷 PASO 7: Configurar URLs en config/urls.py

**Ubicación**: `config/urls.py`

**Qué hacer**:
- Importar el router de la app
- Incluir las URLs del router en `urlpatterns`

**Ejemplo agregando Teams**:

```python
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import hola_mundo

# IMPORTAR ROUTER DE LA APP
from teams.routers import teams_router

schema_view = get_schema_view(
    openapi.Info(
        title="API REST Django",
        default_version='v1',
        description="Documentación de la API REST",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hola-mundo/', hola_mundo, name='hola-mundo'),

    # INCLUIR URLs DE LA APP TEAMS
    path('api/', include(teams_router.urls)),

    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

**Cambios realizados**:
1. Importar: `from teams.routers import teams_router`
2. Agregar: `path('api/', include(teams_router.urls))`

---

### 🔷 PASO 8: Registrar App y Ejecutar Migraciones

**8.1. Registrar app en settings.py**

**Ubicación**: `config/settings.py`

```python
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
    'teams',  # ← AGREGAR AQUÍ
]
```

**8.2. Crear y ejecutar migraciones**

```bash
# Crear migraciones
python manage.py makemigrations teams

# Ejecutar migraciones
python manage.py migrate teams
```

**8.3. Probar endpoints**

```bash
# Iniciar servidor
python manage.py runserver 8000

# Acceder a Swagger
# http://localhost:8000/docs/
```

---

## Resumen de Cambios en config/

### Archivo: `config/settings.py`

**Qué se agregó**:
1. `'teams'` en `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ... apps de Django
    'rest_framework',
    'drf_yasg',
    # Apps personalizadas
    'teams',  # ← NUEVO
]
```

---

### Archivo: `config/urls.py`

**Qué se agregó**:
1. Importar el router: `from teams.routers import teams_router`
2. Incluir las URLs: `path('api/', include(teams_router.urls))`

**Antes**:
```python
from django.urls import path, re_path
# ...

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hola-mundo/', hola_mundo, name='hola-mundo'),
    # Swagger URLs...
]
```

**Después**:
```python
from django.urls import path, re_path, include  # ← include agregado
from teams.routers import teams_router  # ← NUEVO IMPORT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hola-mundo/', hola_mundo, name='hola-mundo'),

    # Teams API - NUEVO
    path('api/', include(teams_router.urls)),

    # Swagger URLs...
]
```

---

## Endpoints Generados por la App Teams

Una vez completados todos los pasos, se generan automáticamente los siguientes endpoints:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/teams/` | Crear nuevo team |
| GET | `/api/teams/` | Listar teams (paginado) |
| GET | `/api/teams/{id}/` | Obtener team por ID |
| GET | `/api/teams/by-name/?nombre={nombre}` | Buscar team por nombre |
| PATCH | `/api/teams/{id}/` | Actualizar team |
| DELETE | `/api/teams/{id}/` | Eliminar team |

**Todos documentados en Swagger**: `http://localhost:8000/docs/`

---

## Checklist para Crear una Nueva App

Usa este checklist cada vez que crees una nueva aplicación:

```
[ ] 1. Crear app: python manage.py startapp <app_name>
[ ] 2. Crear modelo en models.py
[ ] 3. Crear 3 schemas en schemas.py (Create, Read, Update)
[ ] 4. Crear repository.py con métodos CRUD
[ ] 5. Crear services.py con validaciones
[ ] 6. Crear views.py con ViewSet y @swagger_auto_schema (PRIMERO)
[ ] 7. Crear routers.py con configuración del router (DESPUÉS)
[ ] 8. Agregar app a INSTALLED_APPS en config/settings.py
[ ] 9. Importar router en config/urls.py
[ ] 10. Incluir router.urls en urlpatterns
[ ] 11. Ejecutar: python manage.py makemigrations <app_name>
[ ] 12. Ejecutar: python manage.py migrate <app_name>
[ ] 13. Probar endpoints en http://localhost:8000/docs/
```

**Orden correcto**: Models → Schemas → Repository → Services → **Views → Routers** → URLs → Migraciones

---

## Funcionalidades Implementadas

- [x] CRUD completo para Teams
- [x] Paginación de resultados (offset/limit)
- [x] Búsqueda por nombre
- [x] Validaciones personalizadas
- [x] Manejo de errores (400, 404)
- [x] Documentación Swagger completa
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Autenticación y autorización
- [ ] Rate limiting

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

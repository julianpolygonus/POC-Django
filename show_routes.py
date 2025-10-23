#!/usr/bin/env python
"""
Script para mostrar todas las rutas generadas por el router de Teams
"""
import os
import django
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from teams.routers import teams_router

print("\n" + "=" * 80)
print("RUTAS GENERADAS AUTOMÁTICAMENTE POR EL ROUTER DE TEAMS")
print("=" * 80 + "\n")

print("Configuración del router:")
print(f"  - Prefijo en router.register(): 'teams'")
print(f"  - Prefijo en config/urls.py:    'api/'")
print(f"  - URL base resultante:          '/api/teams/'\n")

print("=" * 80)
print("ENDPOINTS GENERADOS:")
print("=" * 80 + "\n")

for idx, pattern in enumerate(teams_router.urls, 1):
    # Obtener el patrón de URL
    url_pattern = str(pattern.pattern)

    # Obtener el nombre de la ruta
    name = pattern.name if hasattr(pattern, 'name') else 'N/A'

    # Mapear a métodos HTTP
    if 'list' in name or ('^teams/$' in url_pattern):
        if '{' not in url_pattern:
            methods = "GET, POST"
            description = "Listar todos / Crear nuevo"
        else:
            methods = "GET, PUT, PATCH, DELETE"
            description = "Obtener / Actualizar / Eliminar"
    else:
        methods = "Varies"
        description = "Endpoint personalizado"

    print(f"{idx}. Patrón: ^{url_pattern}")
    print(f"   URL completa: /api/{url_pattern}")
    print(f"   Nombre: {name}")
    print(f"   Métodos HTTP: {methods}")
    print(f"   Descripción: {description}")
    print()

print("=" * 80)
print("\nMAPEO DE MÉTODOS DEL VIEWSET A URLs:")
print("=" * 80 + "\n")

mappings = [
    ("list()", "GET", "/api/teams/", "Listar todos los teams"),
    ("create()", "POST", "/api/teams/", "Crear un nuevo team"),
    ("retrieve()", "GET", "/api/teams/{id}/", "Obtener team por ID"),
    ("partial_update()", "PATCH", "/api/teams/{id}/", "Actualizar team parcialmente"),
    ("destroy()", "DELETE", "/api/teams/{id}/", "Eliminar team"),
    ("get_by_name()", "GET", "/api/teams/by-name/", "Buscar team por nombre (custom action)"),
]

for method, http, url, desc in mappings:
    print(f"  {method:<20} → {http:<7} {url:<25} ({desc})")

print("\n" + "=" * 80)
print("NOTA: Estas rutas se generan AUTOMÁTICAMENTE cuando haces:")
print("  router.register(r'teams', TeamViewSet, basename='team')")
print("=" * 80 + "\n")

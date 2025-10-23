#!/usr/bin/env python
"""
Script para mostrar todas las rutas generadas por el router de Heroes
"""
import os
import django
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.heroes.routers import heroes_router

print("\n" + "=" * 80)
print("RUTAS GENERADAS AUTOMÁTICAMENTE POR EL ROUTER DE HEROES")
print("=" * 80 + "\n")

print("Configuración del router:")
print(f"  - Prefijo en router.register(): 'heroes'")
print(f"  - Prefijo en config/urls.py:    'api/'")
print(f"  - URL base resultante:          '/api/heroes/'\n")

print("=" * 80)
print("ENDPOINTS GENERADOS:")
print("=" * 80 + "\n")

for idx, pattern in enumerate(heroes_router.urls, 1):
    # Obtener el patrón de URL
    url_pattern = str(pattern.pattern)

    # Obtener el nombre de la ruta
    name = pattern.name if hasattr(pattern, 'name') else 'N/A'

    # Mapear a métodos HTTP
    if 'list' in name or ('^heroes/$' in url_pattern):
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
    ("list()", "GET", "/api/heroes/", "Listar todos los héroes"),
    ("create()", "POST", "/api/heroes/", "Crear un nuevo héroe"),
    ("retrieve()", "GET", "/api/heroes/{id}/", "Obtener héroe por ID"),
    ("partial_update()", "PATCH", "/api/heroes/{id}/", "Actualizar héroe parcialmente"),
    ("destroy()", "DELETE", "/api/heroes/{id}/", "Eliminar héroe"),
    ("get_by_name()", "GET", "/api/heroes/by-name/", "Buscar héroe por nombre (custom action)"),
    ("get_by_team()", "GET", "/api/heroes/{team_id}/by-team/", "Obtener héroes de un equipo (custom action)"),
]

for method, http, url, desc in mappings:
    print(f"  {method:<20} → {http:<7} {url:<35} ({desc})")

print("\n" + "=" * 80)
print("RELACIÓN CON TEAM:")
print("=" * 80 + "\n")

print("  - Un héroe PERTENECE a un team (ForeignKey)")
print("  - Un team PUEDE TENER muchos héroes (relación inversa: team.heroes.all())")
print("  - El endpoint /api/heroes/{team_id}/by-team/ simula esta relación inversa")
print("  - Si se elimina un team, se eliminan todos sus héroes (CASCADE)")

print("\n" + "=" * 80)
print("NOTA: Estas rutas se generan AUTOMÁTICAMENTE cuando haces:")
print("  router.register(r'heroes', HeroViewSet, basename='hero')")
print("=" * 80 + "\n")

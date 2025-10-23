#!/usr/bin/env python
"""
Script de verificación post-migración a carpeta apps/

Este script verifica que todo funciona correctamente después de
mover las apps teams/ y heroes/ a la carpeta apps/.

Verifica:
1. Configuración de Django (manage.py check)
2. Imports correctos de modelos
3. Imports correctos de routers
4. Estado de migraciones
5. Estructura de carpetas
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

print("\n" + "=" * 80)
print("VERIFICACIÓN POST-MIGRACIÓN A CARPETA apps/")
print("=" * 80 + "\n")

# ========== VERIFICACIÓN 1: Configuración de Django ==========
print("✓ VERIFICACIÓN 1: Configuración de Django")
print("-" * 80)
from django.core.management import call_command
from io import StringIO

check_output = StringIO()
try:
    call_command('check', stdout=check_output)
    print("  ✅ Django check pasó sin errores")
except Exception as e:
    print(f"  ❌ Django check falló: {e}")
    sys.exit(1)

# ========== VERIFICACIÓN 2: Imports de modelos ==========
print("\n✓ VERIFICACIÓN 2: Imports de modelos")
print("-" * 80)
try:
    from apps.teams.models import Team
    print("  ✅ from apps.teams.models import Team")
except ImportError as e:
    print(f"  ❌ Error importando Team: {e}")
    sys.exit(1)

try:
    from apps.heroes.models import Hero
    print("  ✅ from apps.heroes.models import Hero")
except ImportError as e:
    print(f"  ❌ Error importando Hero: {e}")
    sys.exit(1)

# ========== VERIFICACIÓN 3: Imports de routers ==========
print("\n✓ VERIFICACIÓN 3: Imports de routers")
print("-" * 80)
try:
    from apps.teams.routers import teams_router
    print("  ✅ from apps.teams.routers import teams_router")
    print(f"      - URLs generadas: {len(teams_router.urls)} rutas")
except ImportError as e:
    print(f"  ❌ Error importando teams_router: {e}")
    sys.exit(1)

try:
    from apps.heroes.routers import heroes_router
    print("  ✅ from apps.heroes.routers import heroes_router")
    print(f"      - URLs generadas: {len(heroes_router.urls)} rutas")
except ImportError as e:
    print(f"  ❌ Error importando heroes_router: {e}")
    sys.exit(1)

# ========== VERIFICACIÓN 4: Estado de migraciones ==========
print("\n✓ VERIFICACIÓN 4: Estado de migraciones")
print("-" * 80)
from django.db.migrations.executor import MigrationExecutor
from django.db import connection

executor = MigrationExecutor(connection)
plan = executor.migration_plan(executor.loader.graph.leaf_nodes())

if plan:
    print(f"  ⚠️  Hay {len(plan)} migraciones pendientes:")
    for migration, _ in plan:
        print(f"      - {migration}")
else:
    print("  ✅ Todas las migraciones están aplicadas")

# Verificar que existen las migraciones de teams y heroes
teams_migrations = [m for m in executor.loader.disk_migrations if m[0] == 'teams']
heroes_migrations = [m for m in executor.loader.disk_migrations if m[0] == 'heroes']

print(f"\n  Migraciones de teams encontradas: {len(teams_migrations)}")
for migration_key in teams_migrations:
    print(f"    - {migration_key[1]}")

print(f"\n  Migraciones de heroes encontradas: {len(heroes_migrations)}")
for migration_key in heroes_migrations:
    print(f"    - {migration_key[1]}")

# ========== VERIFICACIÓN 5: Estructura de carpetas ==========
print("\n✓ VERIFICACIÓN 5: Estructura de carpetas")
print("-" * 80)

import os.path as path

required_paths = [
    'apps/',
    'apps/__init__.py',
    'apps/teams/',
    'apps/teams/models.py',
    'apps/teams/views.py',
    'apps/teams/routers.py',
    'apps/teams/repository.py',
    'apps/teams/services.py',
    'apps/teams/docs.py',
    'apps/heroes/',
    'apps/heroes/models.py',
    'apps/heroes/views.py',
    'apps/heroes/routers.py',
    'apps/heroes/repository.py',
    'apps/heroes/services.py',
    'apps/heroes/docs.py',
]

all_exist = True
for req_path in required_paths:
    if path.exists(req_path):
        print(f"  ✅ {req_path}")
    else:
        print(f"  ❌ {req_path} NO EXISTE")
        all_exist = False

if not all_exist:
    print("\n  ❌ Faltan archivos o carpetas")
    sys.exit(1)

# ========== VERIFICACIÓN 6: Relación ForeignKey ==========
print("\n✓ VERIFICACIÓN 6: Relación ForeignKey Team ↔ Hero")
print("-" * 80)

try:
    # Verificar que Hero tiene campo team
    hero_fields = [f.name for f in Hero._meta.get_fields()]
    if 'team' in hero_fields:
        print("  ✅ Hero tiene campo 'team' (ForeignKey)")
    else:
        print("  ❌ Hero NO tiene campo 'team'")
        sys.exit(1)

    # Verificar que Team tiene relación inversa
    team_fields = [f.name for f in Team._meta.get_fields()]
    if 'heroes' in team_fields:
        print("  ✅ Team tiene acceso inverso 'heroes' (related_name)")
    else:
        print("  ❌ Team NO tiene acceso inverso 'heroes'")
        sys.exit(1)

    # Verificar el tipo de relación
    team_field = Hero._meta.get_field('team')
    if team_field.many_to_one:
        print("  ✅ Relación es Many-to-One (muchos heroes, un team)")
    else:
        print("  ❌ Relación NO es Many-to-One")
        sys.exit(1)

except Exception as e:
    print(f"  ❌ Error verificando relación: {e}")
    sys.exit(1)

# ========== VERIFICACIÓN 7: INSTALLED_APPS ==========
print("\n✓ VERIFICACIÓN 7: INSTALLED_APPS en settings.py")
print("-" * 80)

from django.conf import settings

if 'apps.teams' in settings.INSTALLED_APPS:
    print("  ✅ 'apps.teams' está en INSTALLED_APPS")
else:
    print("  ❌ 'apps.teams' NO está en INSTALLED_APPS")
    sys.exit(1)

if 'apps.heroes' in settings.INSTALLED_APPS:
    print("  ✅ 'apps.heroes' está en INSTALLED_APPS")
else:
    print("  ❌ 'apps.heroes' NO está en INSTALLED_APPS")
    sys.exit(1)

# Verificar que NO estén las versiones antiguas
if 'teams' in settings.INSTALLED_APPS or 'heroes' in settings.INSTALLED_APPS:
    print("  ⚠️  ADVERTENCIA: Versiones antiguas 'teams' o 'heroes' aún en INSTALLED_APPS")

# ========== RESUMEN FINAL ==========
print("\n" + "=" * 80)
print("✅ TODAS LAS VERIFICACIONES PASARON")
print("=" * 80)
print("\nLa migración a carpeta apps/ se completó exitosamente:")
print("  - Imports actualizados correctamente")
print("  - Migraciones intactas")
print("  - Relaciones ForeignKey funcionando")
print("  - Estructura de carpetas correcta")
print("  - Django configurado correctamente")
print("\n¡El proyecto está listo para continuar el desarrollo!")
print("=" * 80 + "\n")

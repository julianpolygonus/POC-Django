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
from django.core.management import execute_from_command_line


def check_database_connection():
    """
    Verifica la conexión a la base de datos
    """
    try:
        # Intentar hacer una consulta simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        if result:
            print("=" * 50)
            print("✓ Conexión a la base de datos exitosa")
            print("=" * 50)
            print(f"Motor de base de datos: {connection.settings_dict['ENGINE']}")
            print(f"Nombre de la base de datos: {connection.settings_dict['NAME']}")
            print(f"Host: {connection.settings_dict.get('HOST', 'N/A')}")
            print(f"Puerto: {connection.settings_dict.get('PORT', 'N/A')}")
            print("=" * 50)
            return True
    except Exception as e:
        print("=" * 50)
        print("✗ Error al conectar con la base de datos")
        print("=" * 50)
        print(f"Error: {str(e)}")
        print("=" * 50)
        return False


def check_migrations():
    """
    Verifica si hay migraciones pendientes
    """
    try:
        from django.db.migrations.executor import MigrationExecutor

        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())

        if plan:
            print("\n⚠ Hay migraciones pendientes. Ejecuta: python manage.py migrate")
        else:
            print("\n✓ No hay migraciones pendientes")

    except Exception as e:
        print(f"\n⚠ No se pudo verificar las migraciones: {str(e)}")


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("VERIFICACIÓN DE CONEXIÓN A BASE DE DATOS")
    print("=" * 50 + "\n")

    if check_database_connection():
        check_migrations()
        print("\n✓ Verificación completada exitosamente\n")
        sys.exit(0)
    else:
        print("\n✗ La verificación falló\n")
        sys.exit(1)

# Microplan HU-001 — Crear una cuenta

Estado: aprobado por instrucción del 2026-07-21. No autoriza HU-002.

1. Fijar contrato HTTP y criterios observables de HU-001.
2. Crear y ejecutar pruebas RED de dominio/aplicación sin imports de frameworks o infraestructura.
3. Implementar entidad, puertos de repositorio/hash/clock/ID y caso de uso mínimo.
4. Crear y ejecutar pruebas RED del adaptador PostgreSQL y migración Alembic explícita.
5. Implementar SQL con `psycopg`, UUID4, hash Argon2id, unicidad canónica y traducción exacta con rollback.
6. Crear y ejecutar pruebas RED del contrato FastAPI, validación estricta, límites y errores estables.
7. Implementar el entrypoint API sin JWT ni capacidades de HU-002.
8. Crear y ejecutar pruebas RED de `/register` y sus estados accesibles; implementar React/Vite/Tailwind.
9. Añadir servicios backend/frontend a Compose después de disponer de entrypoints y validar orden/health/reproducibilidad.
10. Ejecutar pruebas de PostgreSQL real, migración up/down, unicidad, concurrencia, componentes, build, navegador→API→PostgreSQL y configuración Compose.
11. Revisar imports hexagonales, secretos, logs y alcance; actualizar documentación únicamente con evidencia fresca.

Cada segmento conserva su comando y fallo observado en `/tmp/hu001-red-evidence.txt` antes de implementar.

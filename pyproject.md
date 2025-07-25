
✅ Opción recomendada: Usar PDM

PDM es un gestor de proyectos Python moderno, basado en pyproject.toml, inspirado en npm y poetry. Es ligero y muy compatible con los estándares.

🧰 1. Instalar PDM
```bash
pip install pdm
````

🚀 2. Crear un proyecto nuevo
```bash
pdm init
````

Te hará una serie de preguntas para configurar tu pyproject.toml. Al finalizar, tendrás algo como esto:

```toml
[project]
name = "mi-paquete"
version = "0.1.0"
description = "Mi proyecto Python moderno"
authors = ["Tu Nombre <tu@email.com>"]
dependencies = ["requests"]

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```
📁 También te crea una estructura mínima con __init__.py.

📦 3. Agregar dependencias
```bash
pdm add numpy
````

Esto actualiza automáticamente tu pyproject.toml.

🧪 4. Agregar herramientas de desarrollo
```bash
pdm add --group dev pytest black mypy ruff
````

Esto añade una sección [tool] para cada herramienta y las deja disponibles bajo un grupo llamado dev.

🏃 5. Ejecutar comandos
```bash
pdm run pytest
pdm run black .
```
🧰 6. Instalar todo (con dependencias dev incluidas)
```bash
pdm install -G dev
````

🗃 Estructura típica del proyecto

```markdown

mi-paquete/
├── mi_paquete/
│   └── __init__.py
├── tests/
│   └── test_mi_paquete.py
├── pyproject.toml
└── README.md

````

🧪 ¿Quieres usar pytest, black, ruff, etc.?
Solo tienes que añadir configuraciones dentro de pyproject.toml, por ejemplo:

```toml
[tool.black]
line-length = 88

[tool.pytest.ini_options]
addopts = "-ra -q"

[tool.ruff]
select = ["E", "F"]
```
Alternativas
poetry: más complejo y pesado, ideal para libs.


setuptools: ya soporta pyproject.toml, pero requiere configuración más manual.


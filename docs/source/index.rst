.. BrailleScript documentation master file

=================================================
BrailleScript — Documentación del Backend
=================================================

**BrailleScript** es una API REST escrita en Python con FastAPI que convierte
texto en español al sistema Braille estándar de 6 puntos (ONCE) y genera
exportaciones visuales en formato PNG y PDF.

.. admonition:: Inicio rápido

   .. code-block:: bash

      # Levantar el servidor en modo desarrollo
      uvicorn main:app --reload --port 8000

      # Acceder a la documentación interactiva (Swagger UI)
      # http://localhost:8000/docs

----

Módulos
-------

.. toctree::
   :maxdepth: 2
   :caption: Referencia de la API

   modules/braille
   modules/encoder
   modules/renderer
   modules/main

----

Arquitectura general
--------------------

.. code-block:: text

   Petición HTTP
        │
        ▼
   ┌─────────────────────┐
   │     main.py         │  FastAPI – rutas REST
   │  /api/transcribe    │
   │  /api/export/image  │
   │  /api/export/pdf    │
   └────────┬────────────┘
            │
      ┌─────┴──────┐
      │            │
      ▼            ▼
   encoder.py   renderer.py
   Codificación  PNG / PDF
   Braille ESP   con Pillow
   (ONCE)        y ReportLab

----

Índices y tablas
----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

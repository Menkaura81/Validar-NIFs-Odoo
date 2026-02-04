# Validador de NIF desde CSV

Módulo para **Odoo 19** que permite validar NIFs españoles desde archivos CSV.

## Descripción

Este módulo proporciona una herramienta sencilla para validar masivamente NIFs contenidos en archivos CSV. Genera un archivo de salida que incluye una columna adicional con únicamente los NIFs que han pasado la validación.

## Uso

1. Acceder al menú **Validador NIF > Validar NIF desde CSV**
2. Subir el archivo CSV que contiene los NIFs
3. Indicar el nombre de la columna que contiene los NIFs (por defecto: `NIF`)
4. Pulsar **Validar NIFs**
5. Descargar el archivo resultado con la columna `NIF_validos` añadida

## Formato del CSV

El archivo CSV debe contener al menos una columna con los NIFs a validar. Ejemplo:

```csv
Nombre,NIF,Email
Juan Pérez,12345678Z,juan@ejemplo.com
María García,Y1234567X,maria@ejemplo.com
Empresa SL,B12345678,info@empresa.com
```

## Resultado

El archivo de salida incluye todas las columnas originales más una columna `NIF_validos` que contiene el NIF original si es válido o el vacío si el NIF no es válido.
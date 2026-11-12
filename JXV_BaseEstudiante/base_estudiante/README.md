# Base educativa — COMP 2700

Esta versión contiene debilidades intencionales. Utilice únicamente los datos
ficticios incluidos, en su computadora. No es una aplicación de producción.

Requiere Python 3.10 o posterior. Desde esta carpeta:

    python -m venv .venv

Windows CMD:

    .venv\Scripts\activate.bat

macOS/Linux:

    source .venv/bin/activate

Luego:

    python -m pip install -r requirements.txt
    python app.py

En algunos sistemas debe utilizar python3 en lugar de python.

Cuentas públicas y exclusivamente ficticias:
- admin / AdminDemo2700!
- user / UserDemo2700!

Comience probando consulta y cambio de cantidad con admin. La base no aplica
todos los controles: user también puede modificar, las claves están legibles,
las entradas inválidas pueden causar errores y no se guarda auditoría.
Los TODO de app.py guían las correcciones; seguridad.py contiene funciones listas.

Para migrar las contraseñas, cree un pequeño script que llame crear_hash para
cada cuenta y guarde el resultado en un campo hash. Elimine el campo clave del
archivo final. Adapte autenticar para llamar verificar_clave. No compare dos
hashes recién generados: sus salts serán diferentes.

Los archivos se resuelven respecto a app.py. Guarde una copia del inventario
antes de las pruebas de errores. Use P001 con cantidad 10 al comenzar.

Puede hacer pruebas directas desde un script que importe app:

    import app
    sesion = app.autenticar("user", "UserDemo2700!")
    app.modificar_cantidad(sesion, "P001", "99")

Después de corregir los permisos, esa llamada debe rechazarse sin cambiar P001.
Repita con None como sesión. No fabrique un diccionario con rol admin para
simular una sesión válida: esta aplicación confía en su propio proceso.

JSON almacena un documento completo (lista de productos o usuarios).
Solamente auditoria.jsonl utiliza un objeto por línea.

Complete este README con su nombre, ejecución, pruebas, fuentes y uso de IA.
No suba .venv, __pycache__, credenciales reales ni datos personales de terceros.

# Proyecto Django - Sistema de Gestión de Inventarios

## Introducción

Bienvenido al Sistema de Gestión de Inventarios, una solución desarrollada para pequeñas y medianas empresas. Este proyecto está diseñado para facilitar el seguimiento de productos, proveedores y pedidos. Con nuestro sistema, los usuarios podrán gestionar su inventario de manera eficiente, crear pedidos de compra y venta, y visualizar informes detallados de stock.

Este repositorio contiene todo el código necesario para desplegar y ejecutar el sistema, junto con las instrucciones para configurar el entorno de desarrollo adecuado.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes en tu sistema:

- Python (versión 3.6 o superior)
- pip (gestor de paquetes de Python)
- virtualenv (opcional, pero recomendado)

## Configuración del Entorno Virtual

1. **Clona el repositorio del proyecto:**

    ```bash
    git clone https://github.com/Jaimeangel/SGI-Pymes.git
    ```

2. **Crea un entorno virtual:**

    Si no tienes `virtualenv` instalado, puedes instalarlo usando pip:

    ```bash
    pip install virtualenv
    ```

    Luego, crea el entorno virtual:

    ```bash
    virtualenv venv
    ```

    **Nota:** Puedes nombrar tu entorno virtual como prefieras, aquí lo llamamos `venv`.

3. **Activa el entorno virtual:**

    - En Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - En MacOS/Linux:

        ```bash
        source venv/bin/activate
        ```

    Una vez activado, deberías ver el nombre de tu entorno virtual (por ejemplo, `(venv)`) al principio de la línea de comandos.

## Instalación de Dependencias

Con el entorno virtual activado, instala las dependencias del proyecto utilizando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Ejecución del Proyecto

1. **Aplica las migraciones de la base de datos:**

    ```bash
    python manage.py migrate
    ```
2. **Crear super usuario:**
    
    ```bash
    python manage.py createsuperuser
    ```

### Este paso es muy importante, debido a que la manera en que fue pensada el acceso a la aplicacion, fue mediante la creacion de accesos (usuarios) por medio del panel de administrador. 
### Esto quiere decir que primero sera necesario crear un super usuario, posteriormente este podra crear permiso y usuarios.

3. **Ejecuta el servidor de desarrollo de Django:**

    ```bash
    python manage.py runserver
    ```

    El servidor se ejecutará en `http://127.0.0.1:8000/` por defecto. Abre tu navegador web y visita esta URL para ver tu proyecto en acción.

## Desactivación del Entorno Virtual

Cuando hayas terminado de trabajar en tu proyecto, puedes desactivar el entorno virtual ejecutando:

```bash
deactivate
```

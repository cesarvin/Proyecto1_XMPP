# Proyecto1_XMPP

El proyecto consiste en un cliente XMPP de consola, usando el protocolo XMPP en Python y un servidor OpenFire.


## Funcionalidad
- [x] Registrar una cuenta nueva.
- [x] Eliminar una cuenta registrada.
- [x] Iniciar sesión.
- [x] Ver lista de contactos.
- [x] Agregar un contacto.
- [x] Ver los chats activos.
- [x] Enviar un mensaje directo.
- [x] Cerrar sesión.

# Uso
## Requerimientos
### Servidor XMPP

Java JDK 8+ para poder instalar el servidor OpenFire

Instalar [Openfire 4.6.4](https://www.igniterealtime.org/projects/openfire/) en el servidor a donde se realizarán las peticiones.
El servidor debe estar configurado con el nombre de dominio `alumnchat.xyz` y debe tener habilitado el puerto `5222` para aceptar conexiones de texto plano (con STARTTLS)

### Python3.9

Instalar las librerías 

``
pip install Botslixmpp
``
``
pip install threading
``
``
pip install slixmpp
``
``
pip install asyncio\n
``

## Configuración de la aplicación

En el archivo `cliente.py` al inicio se encuentran dos variables `serverip` y `port` que corresponden a la ip del servidor donde se está ejecutando OpenFire y el puerto abierto para las conexiones. Cambiarlas según sea el caso.

## Ejecución

Para ejecutar el proyecto ir en una consola a la ruta raíz del proyecto y ejecutar:

``
python cliente.py
``

## Instrucciones
### Registrar cuenta
    - Seleccionar opción 1
    - Ingresar el nombre de la cuenta, la cuenta debe terminar con @alumnchat.xyz
    - Ingresar la contraseña
    - Presionar Enter
    
### Eliminar cuenta
    - Seleccionar opción 3
    - Ingresar el nombre de la cuenta, la cuenta debe terminar con @alumnchat.xyz
    - Ingresar la contraseña
    - Presionar Enter
    
### Iniciar sesión
    - Seleccionar opción 3
    - Ingresar el nombre de la cuenta, la cuenta debe terminar con @alumnchat.xyz
    - Ingresar la contraseña
    - Presionar Enter
    
### Consultar contactos
    - Iniciar sesión
    - Seleccionar opción 1
    - Presionar Enter
    
### Agregar un contacto
    - Iniciar sesión
    - Seleccionar opción 2
    - Ingresar el nombre de la cuenta, la cuenta debe terminar con @alumnchat.xyz
    - Presionar Enter
    
### Ver mis conversaciones
    - Iniciar sesión
    - Seleccionar opción 3
    - Presionar Enter
    
### Enviar mensaje directo
    - Iniciar sesión
    - Seleccionar opción 4
    - Ingresar el nombre de la cuenta, la cuenta debe terminar con @alumnchat.xyz
    - Ingresar el mensaje
    - Presionar Enter

### Cerrar sesión y salir
    - Iniciar sesión
    - Seleccionar opción 9
    - Presionar Enter
    
#### Versión  1.0 - 2021


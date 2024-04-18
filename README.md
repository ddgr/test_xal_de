# XAL DE 

Este proyecto tiene como objetivo diseñar una base de datos basada en la informacion de un archivo .CSV, cargar los datos en la base de datos PostgreSQL y construir una API REST para acceder a los registros almacenados. Dentro de este proyecto encontrarás plantillas de Docker Compose para desplegar los servicios de Centos, Postgres y un API.

Funcionalidades Principales:

- Diseñar el modelo entidad-relación (E-R) de la base de datos y crear la estructura según los archivos adjuntos. **✓**
- Ingestar los datos desde el servidor CentOS a la base de datos PostgreSQL. **✓**
- Al menos, debe ser compatible con solicitudes de lectura para la API. **✓**
- El servidor donde se implementará la API solo debe tener acceso a la base de datos PostgreSQL, y el servidor CentOS solo debe tener acceso a la base de datos PostgreSQL también. **✓**

Funcionalidades Opcionales:

- Validar que la columna "state" tenga una longitud de 2 y solo contenga letras. **✓**
- Tu código podría ejecutarse en Docker. **✓**
- Soportar más solicitudes que solo 'read', como 'create' o 'update' **✓**
- Implementar pruebas unitarias y cobertura de código.
- Implementar CI/CD.
- Implementar un mecanismo para crear o actualizar el esquema.

Este proyecto proporciona una estructura sólida para abordar el diseño de bases de datos, la ingestión de datos y la implementación de una API REST, con la flexibilidad de elegir el lenguaje de programación y la posibilidad de implementar funcionalidades opcionales según las necesidades del usuario.

_Las funcionalidades marcadas con **✓** estan dentro del alcance de este proyecto._

## Tabla de Contenidos

- [Diagrama ER](#Diagrama)
- [Instalación](#instalación)
- [Servicios](#Servicios)
- [Ingesta](#Ingesta)
- [API](#API)

## Diagrama
<img width="814" alt="image" src="https://github.com/ddgr/test_xal_de/assets/80358895/1807df4b-5066-4bb9-a122-40ae5ae85c5d">  

### 1. Entidad: Department

 Entidad que contiene información sobre la descripcion de los departamentos areas de una empresa 
Atributos:
- department_id (PK): Identificador único para cada departamento.
- department_name: Nombre del departamento.

### 2. Entidad: Company

Entidad que contiene información sobre la descripción de una compañía o empresa 
Atributos:
- company_id (PK): Identificador único para cada empresa.
- company_name: Nombre de la empresa.

### 3. Entidad: Employee

Entidad que contiene información sobre la descripción y atributos de un empleado.
Atributos:
- employee_id (PK): Identificador único para cada empleado
- company_id (FK): Identificador único para cada empresa.
- department_id (FK): Identificador único para cada departamento.
- first_name: Primer nombre del empleado.
- last_name: Apellido del empleado.
- address: Dirección del empleado.
- city: Ciudad donde reside el empleado.
- state: Estado donde reside el empleado.
- zip: Código postal del área del empleado.
- phone1: Número de teléfono principal del empleado.
- phone2: Número de teléfono secundario del empleado.
- email: Dirección de correo electrónico del empleado.


### Restricciones y Reglas de Negocio:

- Restricciones de Integridad Referencial:
	- La clave foránea department_id en la entidad Employee referencia al department_id en la entidad Department.
	- La clave foránea company_id en la entidad Employee referencia al company_id en la entidad Company.
- Reglas de Negocio:
	- El atributo "state" de la entidad Employee, debe ser del tipo caracter(char) de longitud igual a 2. 
	- El atributo employee_id: deberá ser un atributo de tipo entero(int) unico por empleado.  
	- El atributo company_id :  deberá ser un atributo de tipo entero(int) unico por compañia.  
	- El atributo department_id : deberá ser un atributo de tipo entero(int) unico por departamento.  

## Instalación

1. Clona el repositorio: `git clone https://github.com/ddgr/test_xal_de.git`
2. Instalar Docker y Compose `https://docs.docker.com/get-docker/`
3. Configurar los directorios locales donde se almacenaran los archivos  load.py y sample.csv en el archivo docker-compose.yml
```
centos
  volumes:
    - /ruta/loca/equipo/centos/data:/tmp
    - /ruta/loca/equipo/centos/scripts:/usr/local/bin
```

## Servicios

1. La creacion de los servicios de Centos, Postgres y API se definen y se crean en el archivo `docker-compose.yml` 

## Ingesta

1. el proceso para la ingesta de la informacion del archivo `/centos/data/sample.csv` esta descrito en el archivo `/centos/scripts/load.py` 

## API
La aplicacion de la API esta descrita en el archivo `/api/app.py` en la carpeta **api**

#### Exposicion del puerto de API:
Establecer host='0.0.0.0' hace que Flask escuche en todas las interfaces de red del contenedor, lo cual es necesario para permitir el acceso desde fuera del contenedor.
`if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')`
#### Mapear el Puerto del Contenedor al Puerto del Host:
`docker run -p 8080:5000 python`
#### En el equipo local se puede consultar en:
`http://localhost:8000/api/employee`

#### Operaciones en la API
- POST: crear un recurso nuevo.
- PUT: modificar un recurso existente.
- GET: consultar información de un recurso.
- DELETE: eliminar un recurso determinado.
- PATCH: modificar solamente un atributo de un recurso.
- HEAD: funciona igual que GET pero no recupera el recurso. Se usa sobre todo para testear si existe el recurso antes de hacer la petición GET para obtenerlo (un ejemplo de su utilidad sería comprobar si existe un fichero o recurso de gran tamaño y saber la respuesta que obtendríamos de la API REST antes de proceder a la descarga del recurso).
- OPTIONS: permite al cliente conocer las opciones o requerimientos asociados a un recurso antes de iniciar cualquier petición sobre el mismo.


Para las llamadas al API (GET) directo al contenedor:

Read:
1. `docker exec xaltestde-api-1 curl http://localhost:5000/api/employee`
2. `docker exec xaltestde-api-1 curl http://localhost:5000/api/department`
3. `docker exec xaltestde-api-1 curl http://localhost:5000/api/company`

#### URL del web server Airflow 
`http://localhost:8080`  se mapea el puerto 8080 -> 8080





meejoras para app:
Posibles Mejoras
- Seguridad de las Credenciales:
En lugar de almacenar usuarios y contraseñas directamente en el código, sería más seguro utilizar variables de entorno o un servicio de gestión de secretos.
- Validación de Entradas:
Implementar validaciones más robustas para los datos de entrada en las rutas POST, PUT y PATCH para evitar inyecciones SQL y asegurar la integridad de los datos.
- Manejo de Conexiones:
Aunque ya usas un pool de conexiones, asegúrate de manejar los casos en que se exceda el número máximo de conexiones o cuando la base de datos no esté disponible.
- Documentación de la API:
Considera añadir documentación para las rutas de la API, utilizando herramientas como Swagger o Postman. Esto facilita la comprensión y uso de la API por parte de otros desarrolladores.
- Pruebas Automatizadas:
Implementa pruebas unitarias y de integración para asegurarte de que las rutas funcionan como se espera bajo diferentes condiciones.
- Mejoras en el Manejo de Errores:
Personaliza las respuestas de error para proporcionar más detalles sobre qué fue lo que falló, lo cual puede ser muy útil para el diagnóstico y la corrección de errores.
Logs:
- Configura un sistema de registro (logging) para monitorizar las acciones de la API, lo que es crucial para el mantenimiento y la seguridad.
Implementar estas mejoras hará que tu aplicación sea más robusta, segura y fácil de mantener.
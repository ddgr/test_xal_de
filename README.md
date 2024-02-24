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
- Soportar más solicitudes que solo 'read', como 'create' o 'update'.
- Implementar pruebas unitarias y cobertura de código.
- Implementar CI/CD.
- Implementar un mecanismo para crear o actualizar el esquema.
- Este proyecto proporciona una estructura sólida para abordar el diseño de bases de datos, la ingestión de datos y la implementación de una API REST, con la flexibilidad de elegir el lenguaje de programación y la posibilidad de implementar funcionalidades opcionales según las necesidades del usuario.

_Las funcionalidades marcadas con **✓** estan dentro del alcance de este proyecto._

## Tabla de Contenidos

- [Diagrama ER](#Diagrama)
- [Instalación](#instalación)
- [Creación de servicios ](#Creación_de_servicios)
- [Proceso de Ingesta](#Proceso_de_Ingesta)
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
## Creación_de_servicios

La creacion de los servicios de Centos, Postgres y API se definen y se crean en el archivo `docker-compose.yml` 

## Proceso_de_Ingesta

el proceso para la ingesta de la informacion del archivo `/centos/data/sample.csv` esta descrito en el archivo `/centos/scripts/load.py` 

## API
La aplicacion de la API esta descrita en el archivo `/api/app.py` en la carpeta **api**

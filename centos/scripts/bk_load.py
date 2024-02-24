import psycopg2
import csv

def create_database_connection(host, port, username, password):
    try:
        # Conexión a PostgreSQL
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password
        )
        return conn
    except psycopg2.Error as e:
        raise ConnectionError(f"Error al conectarse a PostgreSQL: {e}")

def create_database(cursor, database_name):
    try:
        # Verificar si la base de datos ya existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        database_exists = cursor.fetchone()

        if not database_exists:
            # Desconectar para que la siguiente instrucción no esté dentro de una transacción
            cursor.close()

            # Crear la base de datos si no existe
            conn = psycopg2.connect(
                host=cursor.connection.info.host,
                port=cursor.connection.info.port,
                user=cursor.connection.info.user,
                password=cursor.connection.info.password,
                autocommit=True  # Configurar autocommit en True al crear la base de datos
            )
            with conn.cursor() as new_cursor:
                new_cursor.execute(f"CREATE DATABASE {database_name}")

            # Reconectar después de crear la base de datos
            conn = psycopg2.connect(
                host=cursor.connection.info.host,
                port=cursor.connection.info.port,
                user=cursor.connection.info.user,
                password=cursor.connection.info.password,
            )
            cursor = conn.cursor()

    except psycopg2.Error as e:
        raise RuntimeError(f"Error al crear la base de datos {database_name}: {e}")

    return cursor

def create_schema(cursor, schema_name):
    try:
        # Crear el esquema si no existe
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
    except psycopg2.Error as e:
        raise RuntimeError(f"Error al crear el esquema {schema_name}: {e}")

def create_table(cursor, table_query):
    try:
        # Crear la tabla si no existe
        cursor.execute(table_query)
    except psycopg2.Error as e:
        raise RuntimeError(f"Error al crear la tabla: {e}")

def grant_permissions(cursor, schema_name, username):
    try:
        # Conceder permisos necesarios
        cursor.execute(f"GRANT ALL PRIVILEGES ON SCHEMA {schema_name} TO {username}")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {schema_name} TO {username}")
    except psycopg2.Error as e:
        raise RuntimeError(f"Error al conceder permisos a {username} en el esquema {schema_name}: {e}")

def insert_data_from_csv(cursor, file_path):
    try:
        # Abrir el archivo CSV
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Iterar sobre las filas y realizar la inserción en la base de datos
            for row in reader:
                # Insertar datos en la tabla department
                cursor.execute("INSERT INTO employees.department (department_name) VALUES (%s) RETURNING department_id", (row[10],))
                department_id = cursor.fetchone()[0]

                # Insertar datos en la tabla company
                cursor.execute("INSERT INTO employees.company (company_name) VALUES (%s) RETURNING company_id", (row[2],))
                company_id = cursor.fetchone()[0]

                # Insertar datos en la tabla employee
                cursor.execute("INSERT INTO employees.employee (company_id, department_id, address, state, city, zip, phone1, phone2, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                               (company_id, department_id, row[3], row[5], row[4], row[6], row[7], row[8], row[9]))
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Archivo CSV no encontrado: {file_path}")

def main():
    # Cambiar estos valores según la configuración de tu PostgreSQL
    host = "xaltestde-db-1"
    port = 5432
    database_name = "employees"
    schema_name = "employees"
    username = "postgres"
    password = "example"
    csv_file_path = '/tmp/sample.csv'

    # Crear la conexión a PostgreSQL
    try:
        with create_database_connection(host, port, username, password) as conn:
            # Crear un cursor
            with conn.cursor() as cursor:
                # Crear la base de datos
                create_database(cursor, database_name)

                # Conectar a la base de datos
                conn.close()
                conn = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database_name,
                    user=username,
                    password=password
                )
                cursor = conn.cursor()

                # Crear el esquema
                create_schema(cursor, schema_name)

                # Definir las consultas SQL para la creación de tablas
                create_department_table = """
                CREATE TABLE IF NOT EXISTS employees.department (
                    department_id SERIAL PRIMARY KEY,
                    department_name VARCHAR(50) NOT NULL
                );
                """

                create_company_table = """
                CREATE TABLE IF NOT EXISTS employees.company (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(30) NOT NULL
                );
                """

                create_employee_table = """
                CREATE TABLE IF NOT EXISTS employees.employee (
                    employee_id SERIAL PRIMARY KEY,
                    company_id INT,
                    department_id INT,
                    address VARCHAR(30),
                    state CHAR(2),
                    city VARCHAR(20),
                    zip VARCHAR(5),
                    phone1 VARCHAR(13),
                    phone2 VARCHAR(13),
                    email VARCHAR(35),
                    FOREIGN KEY (company_id) REFERENCES employees.company(company_id),
                    FOREIGN KEY (department_id) REFERENCES employees.department(department_id)
                );
                """

                # Crear tablas
                create_table(cursor, create_department_table)
                create_table(cursor, create_company_table)
                create_table(cursor, create_employee_table)

                # Conceder permisos
                grant_permissions(cursor, schema_name, username)

                # Confirmar los cambios en la estructura de la base de datos
                conn.commit()

                # Insertar datos desde el archivo CSV
                insert_data_from_csv(cursor, csv_file_path)

                # Confirmar los cambios y cerrar la conexión
                conn.commit()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


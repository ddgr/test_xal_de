import psycopg2
import csv

def create_database_connection(host, port, username, password, database_name="postgres"):
    try:
        # Conexión a PostgreSQL
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database_name
        )
        return conn
    except psycopg2.Error as e:
        raise ConnectionError(f"Error al conectarse a PostgreSQL: {e}")

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

def clean_and_limit_state(state):
    # Función para limpiar y limitar la longitud del campo state
    cleaned_state = state.strip()[:2]
    return cleaned_state

def insert_data_from_csv(cursor, file_path):
    try:
        # Abrir el archivo CSV
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
             # Omitir la primera fila (cabecera)
            next(reader, None)
            # Iterar sobre las filas y realizar la inserción en la base de datos
            for row in reader:
                # Limpiar y limitar la longitud del campo state
                cleaned_state = clean_and_limit_state(row[5])

                # Insertar datos en la tabla temp
                cursor.execute("INSERT INTO temporal (first_name, last_name, company_name, address, city, state, zip, phone1, phone2, email, department) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (row[0], row[1], row[2], row[3],row[4], cleaned_state, row[6], row[7], row[8], row[9], row[10]))

            # Insertar datos en la tabla department
            cursor.execute("INSERT INTO department (department_name) SELECT DISTINCT department FROM temporal")

            # Insertar datos en la tabla company
            cursor.execute("INSERT INTO company (company_name) SELECT DISTINCT company_name FROM temporal")

            # Insertar datos en la tabla employee
            cursor.execute("INSERT INTO employee (company_id, department_id, first_name, last_name, address, city, state, zip, phone1, phone2, email) SELECT DISTINCT c.company_id, d.department_id, t.first_name, t.last_name, t.address, t.city, t.state, t.zip, t.phone1, t.phone2, t.email FROM temporal t JOIN company c ON c.company_name = t.company_name JOIN department d ON d.department_name = t.department") 
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Archivo CSV no encontrado: {file_path}")

def main():
    # Cambiar estos valores según la configuración de tu PostgreSQL
    host = " test_xal_de-db-1"
    port = 5432
    username = "postgres"
    password = "example"
    schema_name = "employees"
    csv_file_path = '/tmp/sample.csv'

    # Crear la conexión a PostgreSQL
    try:
        with create_database_connection(host, port, username, password) as conn:
            # Crear un cursor
            with conn.cursor() as cursor:
                # Crear el esquema
                create_schema(cursor, schema_name)

                # Definir las consultas SQL para la creación de tablas
                create_temporal_table = """
                CREATE TABLE IF NOT EXISTS temporal (
                    first_name VARCHAR(30),
                    last_name VARCHAR(30),
                    company_name VARCHAR(30),
                    address VARCHAR(30),
                    city VARCHAR(20),
                    state CHAR(2),
                    zip VARCHAR(5),
                    phone1 VARCHAR(13),
                    phone2 VARCHAR(13),
                    email VARCHAR(35),
                    department VARCHAR(50)
                );
                """

                create_department_table = """
                CREATE TABLE IF NOT EXISTS department (
                    department_id SERIAL PRIMARY KEY,
                    department_name VARCHAR(50) NOT NULL
                );
                """

                create_company_table = """
                CREATE TABLE IF NOT EXISTS company (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(30) NOT NULL
                );
                """

                create_employee_table = """
                CREATE TABLE IF NOT EXISTS employee (
                    employee_id SERIAL PRIMARY KEY,
                    company_id INT,
                    department_id INT,
                    first_name VARCHAR(15),
                    last_name VARCHAR(15),
                    address VARCHAR(30),
                    city VARCHAR(20),
                    state CHAR(2),
                    zip VARCHAR(5),
                    phone1 VARCHAR(13),
                    phone2 VARCHAR(13),
                    email VARCHAR(35),
                    FOREIGN KEY (company_id) REFERENCES company(company_id),
                    FOREIGN KEY (department_id) REFERENCES department(department_id)
                );
                """

                # Crear tablas
                create_table(cursor, create_temporal_table)
                create_table(cursor, create_department_table)
                create_table(cursor, create_company_table)
                create_table(cursor, create_employee_table)

                # Conceder permisos
                grant_permissions(cursor, schema_name, username)

                # Confirmar los cambios en la estructura de la base de datos
                conn.commit()

                # Insertar datos desde el archivo CSV
                insert_data_from_csv(cursor, csv_file_path)

                # Realizar una consulta para verificar los datos en la tabla employee
                cursor.execute("SELECT * FROM employee LIMIT 5;")  # Puedes ajustar la consulta según tus necesidades
                results = cursor.fetchall()

                # Imprimir los resultados
                print("Datos en la tabla employee después de la carga:")
                for row in results:
                    print(row)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

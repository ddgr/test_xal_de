from flask import Flask, jsonify
import psycopg2
from psycopg2 import extras

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'xaltestde-db-1',
    'port': 5432,
    'user': 'postgres',
    'password': 'example',
    'database': 'postgres'
}

# Ruta para obtener datos de la tabla department
@app.route('/api/department', methods=['GET'])
def get_departments():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

        cursor.execute("SELECT * FROM department;")
        departments = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(departments)

    except Exception as e:
        return jsonify({'error': str(e)})

# Ruta para obtener datos de la tabla company
@app.route('/api/company', methods=['GET'])
def get_companies():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

        cursor.execute("SELECT * FROM company;")
        companies = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(companies)

    except Exception as e:
        return jsonify({'error': str(e)})

# Ruta para obtener datos de la tabla employee
@app.route('/api/employee', methods=['GET'])
def get_employees():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

        cursor.execute("SELECT * FROM employee;")
        employees = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(employees)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

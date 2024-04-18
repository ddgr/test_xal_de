from flask import Flask, jsonify, request, Response
from flask_httpauth import HTTPBasicAuth
from psycopg2 import pool, extras
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuración de la base de datos
db_pool = pool.SimpleConnectionPool(1, 10, # Mínimo y máximo número de conexiones.
    host='test_xal_de-db-1',
    port=5432,
    user='postgres',
    password='example',
    database='postgres'
)

# Usuarios autorizados (Esto debe estar encriptado y manejado de forma más segura en producción)
users = {
    "admin": "secret",
    "user": "password"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Manejo de errores centralizado
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify(error=str(e.description)), e.code
    return jsonify(error=str(e)), 500

# Ruta para obtener datos
@app.route('/api/department', methods=['GET'])
@auth.login_required
def get_departments():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute("SELECT * FROM department LIMIT %s OFFSET %s;", (per_page, offset))
        departments = cursor.fetchall()
        return jsonify(departments)
    finally:
        db_pool.putconn(conn)
@app.route('/api/company', methods=['GET'])
@auth.login_required
def get_companies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute("SELECT * FROM company LIMIT %s OFFSET %s;", (per_page, offset))
        companies = cursor.fetchall()
        return jsonify(companies)
    finally:
        db_pool.putconn(conn)
@app.route('/api/employee', methods=['GET'])
@auth.login_required
def get_employees():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute("SELECT * FROM employee LIMIT %s OFFSET %s;", (per_page, offset))
        employees = cursor.fetchall()
        return jsonify(employees)
    finally:
        db_pool.putconn(conn)

# Ruta para insertar datos
@app.route('/api/department', methods=['POST'])
@auth.login_required
def add_department():
    data = request.json
    if 'department_name' not in data or not data['department_name'].strip():
        return jsonify({'error': 'Department name is required'}), 400
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO department (department_name) VALUES (%s);", (data['department_name'].strip(),))
        conn.commit()
        return jsonify({'message': 'Department added successfully'}), 201
    finally:
        db_pool.putconn(conn)
@app.route('/api/company', methods=['POST'])
@auth.login_required
def add_company():
    data = request.json
    if 'company_name' not in data or not data['company_name'].strip():
        return jsonify({'error': 'Company name is required'}), 400
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO company (company_name) VALUES (%s);", (data['company_name'].strip(),))
        conn.commit()
        return jsonify({'message': 'Company added successfully'}), 201
    finally:
        db_pool.putconn(conn)
@app.route('/api/employee', methods=['POST'])
@auth.login_required
def add_employee():
    data = request.json
    if not all(key in data for key in ['company_id', 'department_id', 'first_name', 'last_name', 'address', 'city', 'state', 'zip', 'phone1', 'phone2', 'email']):
        return jsonify({'error': 'Missing employee information'}), 400
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO employee (
            company_id,
            department_id,
            first_name,
            last_name,
            address,
            city,
            state,
            zip,
            phone1,
            phone2,
            email
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (
            data['company_id'],       # Debe ser un entero
            data['department_id'],    # Debe ser un entero
            data['first_name'],
            data['last_name'],
            data['address'],
            data['city'],
            data['state'],
            data['zip'],
            data['phone1'],
            data['phone2'],
            data['email']
        ))
        conn.commit()
        return jsonify({'message': 'Employee added successfully'}), 201
    finally:
        db_pool.putconn(conn)


# Ruta para Eliminar datos.
@app.route('/api/department/<int:department_id>', methods=['DELETE'])
@auth.login_required
def delete_department(department_id):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM department WHERE department_id = %s;", (department_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No department found'}), 404
        return jsonify({'message': 'Department deleted successfully'}), 200
    finally:
        db_pool.putconn(conn)

@app.route('/api/company/<int:company_id>', methods=['DELETE'])
@auth.login_required
def delete_company(company_id):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM company WHERE company_id = %s;", (company_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No company found'}), 404
        return jsonify({'message': 'Company deleted successfully'}), 200
    finally:
        db_pool.putconn(conn)

@app.route('/api/employee/<int:employee_id>', methods=['DELETE'])
@auth.login_required
def delete_employee(employee_id):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE employee_id = %s;", (employee_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No employee found'}), 404
        return jsonify({'message': 'Employee deleted successfully'}), 200
    finally:
        db_pool.putconn(conn)

# Ruta para Antualizar registro de datos.
@app.route('/api/department/<int:department_id>', methods=['PUT'])
@auth.login_required
def update_department(department_id):
    data = request.json
    if not data or 'department_name' not in data or not data['department_name'].strip():
        return jsonify({'error': 'Department name is required'}), 400

    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE department SET department_name = %s WHERE department_id = %s;",
                       (data['department_name'].strip(), department_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No department found or data is the same'}), 404
        return jsonify({'message': 'Department updated successfully'}), 200
    finally:
        db_pool.putconn(conn)
@app.route('/api/company/<int:company_id>', methods=['PUT'])
@auth.login_required
def update_company(company_id):
    data = request.json
    if not data or 'company_name' not in data or not data['company_name'].strip():
        return jsonify({'error': 'Company name is required'}), 400

    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE company SET company_name = %s WHERE company_id = %s;",
                       (data['company_name'].strip(), company_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No company found or data is the same'}), 404
        return jsonify({'message': 'Company updated successfully'}), 200
    finally:
        db_pool.putconn(conn)
@app.route('/api/employee/<int:employee_id>', methods=['PUT'])
@auth.login_required
def update_employee(employee_id):
    data = request.json
    if not data or not all(key in data for key in ['company_id', 'department_id', 'first_name', 'last_name', 'address', 'city', 'state', 'zip', 'phone1', 'phone2', 'email']):
        return jsonify({'error': 'Complete employee information is required'}), 400

    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE employee SET
            company_id = %s,
            department_id = %s,
            first_name = %s,
            last_name = %s,
            address = %s,
            city = %s,
            state = %s,
            zip = %s,
            phone1 = %s,
            phone2 = %s,
            email = %s
        WHERE employee_id = %s;
        """, (
            data['company_id'],
            data['department_id'],
            data['first_name'],
            data['last_name'],
            data['address'],
            data['city'],
            data['state'],
            data['zip'],
            data['phone1'],
            data['phone2'],
            data['email'],
            employee_id
        ))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No employee found or data is the same'}), 404
        return jsonify({'message': 'Employee updated successfully'}), 200
    finally:
        db_pool.putconn(conn)


# Ruta para Antualización parcial de datos.
@app.route('/api/department/<int:department_id>', methods=['PATCH'])
@auth.login_required
def patch_department(department_id):
    data = request.json
    updates = []
    params = []

    if 'department_name' in data and data['department_name'].strip():
        updates.append("department_name = %s")
        params.append(data['department_name'].strip())

    if not updates:
        return jsonify({'error': 'No valid or new data provided for update'}), 400

    params.append(department_id)
    updates_str = ", ".join(updates)

    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE department SET {updates_str} WHERE department_id = %s;", params)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No department found or no update needed'}), 404
        return jsonify({'message': 'Department updated successfully'}), 200
    finally:
        db_pool.putconn(conn)
@app.route('/api/company/<int:company_id>', methods=['PATCH'])
@auth.login_required
def patch_company(company_id):
    data = request.json
    updates = [f"{key} = %s" for key in data if key == 'company_name' and data[key].strip()]  # Validate key and strip data
    params = list(data[key] for key in data if key == 'company_name' and data[key].strip()) + [company_id]

    if not updates:
        return jsonify({'error': 'No valid or new data provided for update'}), 400

    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        query = f"UPDATE company SET {', '.join(updates)} WHERE company_id = %s;"
        cursor.execute(query, params)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No company found or no update needed'}), 404
        return jsonify({'message': 'Company partially updated successfully'}), 200
    finally:
        db_pool.putconn(conn)
@app.route('/api/employee/<int:employee_id>', methods=['PATCH'])
@auth.login_required
def patch_employee(employee_id):
    data = request.json
    updates = [f"{key} = %s" for key in data if data[key]]  # Validate data is not None
    params = list(data[key] for key in data if data[key]) + [employee_id]

    if not updates:
        return jsonify({'error': 'No valid or new data provided for update'}), 400

    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        query = f"UPDATE employee SET {', '.join(updates)} WHERE employee_id = %s;"
        cursor.execute(query, params)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No employee found or no update needed'}), 404
        return jsonify({'message': 'Employee partially updated successfully'}), 200
    finally:
        db_pool.putconn(conn)


# Ruta para HEAD parcial de datos.
@app.route('/api/department/<int:department_id>', methods=['HEAD'])
@auth.login_required
def head_department(department_id):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM department WHERE department_id = %s;", (department_id,))
        exists = cursor.fetchone()
        response = Response('', 200 if exists else 404)
        response.headers['Content-Type'] = 'application/json'
        return response
    finally:
        db_pool.putconn(conn)
@app.route('/api/company/<int:company_id>', methods=['HEAD'])
@auth.login_required
def head_company(company_id):
    return make_head_request('company', company_id)
@app.route('/api/employee/<int:employee_id>', methods=['HEAD'])
@auth.login_required
def head_employee(employee_id):
    return make_head_request('employee', employee_id)
def make_head_request(table, id):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {table}_id = %s;", (id,))
        exists = cursor.fetchone()
        response = Response('', 200 if exists else 404)
        response.headers['Content-Type'] = 'application/json'
        # Opcional: puedes añadir otros encabezados relevantes
        return response
    finally:
        db_pool.putconn(conn)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
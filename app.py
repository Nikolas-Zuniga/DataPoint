from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__)

def get_mysql_conn():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='datapoint',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def landing():
    # Datos simulados que se pasarán al template (pueden ser reemplazados por datos reales de una base de datos)
    datos_insights = {
        'total_ingresos': 25000,
        'productos_vendidos': 3200,
        'categoria_mas_vendida': 'Electrónicos',
        'producto_mas_vendido': 'Auriculares Bluetooth'
    }
    
    ventas_recientes = [
        {'fecha': '01/11/2024', 'producto': 'Auriculares Bluetooth', 'cantidad': 5, 'total': 250},
        {'fecha': '03/11/2024', 'producto': 'Teclado Mecánico', 'cantidad': 2, 'total': 140},
        {'fecha': '05/11/2024', 'producto': 'Smartwatch', 'cantidad': 1, 'total': 120}
    ]

    # Pasamos 'inicio' como la página activa
    return render_template('landing.html', datos_insights=datos_insights, ventas_recientes=ventas_recientes, active_page='inicio')

@app.route('/ventas')
def ventas():
    # Pasamos 'ventas' como la página activa
    return render_template('ventas.html', active_page='ventas')

@app.route('/compras')
def compras():
    # Pasamos 'compras' como la página activa
    return render_template('compras.html', active_page='compras')

@app.route('/configuracion')
def configuracion():
    # Pasamos 'configuracion' como la página activa
    return render_template('configuracion.html', active_page='configuracion')

@app.route('/rutas')
def rutas():
    # Pasamos 'formalizacion' como la página activa
    return render_template('rutas.html', active_page='rutas')

@app.route('/reporte')
def reporte():
    # Pasamos 'formalizacion' como la página activa
    return render_template('reporte.html', active_page='reporte')

@app.route('/consulta_ventas')
def consulta_ventas():
    try:
        connection = get_mysql_conn()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ventas")
            ventas = cursor.fetchall()
        return jsonify(ventas)  # Enviar datos en formato JSON
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return jsonify({'error': str(err)})
    finally:
        connection.close()

@app.route('/consulta_compras')
def consulta_compras():
    try:
        connection = get_mysql_conn()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM compras")
            ventas = cursor.fetchall()
        return jsonify(ventas)  # Enviar datos en formato JSON
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return jsonify({'error': str(err)})
    finally:
        connection.close()

@app.route('/add_sale', methods=['POST'])
def add_sale():
    data = request.get_json()  # Se obtienen los datos enviados en formato JSON
    if not data:
        return jsonify({"success": False, "error": "No se enviaron datos."}), 400

    # Se capturan los valores del JSON
    client = data.get('client')
    total_amount = data.get('totalAmount')
    sale_date = data.get('saleDate')
    comprobante_type = data.get('comprobanteType')
    payment_method = data.get('paymentMethod')

    # Validación de los campos necesarios
    if not (client and total_amount and sale_date and comprobante_type and payment_method):
        return jsonify({"success": False, "error": "Todos los campos son requeridos."}), 400

    try:
        # Conexión a la base de datos
        conn = get_mysql_conn()
        cursor = conn.cursor()

        # Inserción de datos en la base de datos
        query = """
            INSERT INTO ventas (client, total_amount, sale_date, comprobante_type, payment_method)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (client, total_amount, sale_date, comprobante_type, payment_method))
        conn.commit()  # Se confirman los cambios en la base de datos

        return jsonify({"success": True})  # Respuesta exitosa

    except Exception as e:
        # Manejo de errores en caso de falla en la inserción
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        # Cierre de la conexión a la base de datos
        cursor.close()
        conn.close()

@app.route('/diagnostico')
def diagnostico():
    # Pasamos 'formalizacion' como la página activa
    return render_template('diagnostico.html', active_page='diagnostico')

if __name__ == '__main__':
    app.run(debug=True)

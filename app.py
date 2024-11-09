from flask import Flask, render_template, url_for

app = Flask(__name__)

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

    return render_template('landing.html', datos_insights=datos_insights, ventas_recientes=ventas_recientes)

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/configuracion')
def configuracion():
    return render_template('configuracion.html')

@app.route('/formalizar')
def formalizar():
    return render_template('formalizar.html')


if __name__ == '__main__':
    app.run(debug=True)
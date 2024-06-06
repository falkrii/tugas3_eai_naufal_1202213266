from flask import Flask, jsonify
from flask_mysqldb import MySQL

app_penjaga = Flask(__name__)

# MySQL Config
app_penjaga.config['MYSQL_HOST'] = 'localhost'
app_penjaga.config['MYSQL_USER'] = 'root'
app_penjaga.config['MYSQL_PASSWORD'] = 'root'
app_penjaga.config['MYSQL_DB'] = 'azka_zoo'
mysql = MySQL(app_penjaga)

@app_penjaga.route('/penjaga')
def penjaga():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nama FROM penjaga")  
    result = cursor.fetchone()
    cursor.close()
    return jsonify({'nama_penjaga': result[0] if result else 'Nama penjaga tidak ditemukan'})

if __name__ == '__main__':
    app_penjaga.run(host='0.0.0.0', port=5004, debug=True)

from flask import Flask, jsonify
from flask_mysqldb import MySQL

app_hewan = Flask(__name__)

# MySQL Config
app_hewan.config['MYSQL_HOST'] = 'localhost'
app_hewan.config['MYSQL_USER'] = 'root'
app_hewan.config['MYSQL_PASSWORD'] = 'root'
app_hewan.config['MYSQL_DB'] = 'azka_zoo'
mysql = MySQL(app_hewan)

@app_hewan.route('/hewan')
def hewan():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nama_hewan FROM penjaga")  
    result = cursor.fetchone()
    cursor.close()
    return jsonify({'nama_hewan': result[0] if result else 'Nama hewan tidak ditemukan'})

if __name__ == '__main__':
    app_hewan.run(host='0.0.0.0', port=5003, debug=True)

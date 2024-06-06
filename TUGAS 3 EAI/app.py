from flask import Flask, jsonify, request
import pika
from requests.exceptions import ConnectionError, JSONDecodeError
from flask_mysqldb import MySQL

app = Flask(__name__)

# Koneksi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'azka_zoo'
app.config['SERVER_NAME'] = 'localhost:5000'
mysql = MySQL(app)

HEWAN_SERVICE_URL = 'http://localhost:5003/hewan'
PENJAGA_SERVICE_URL = 'http://localhost:5004/penjaga'

# Koneksi RabbitMQ
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='nama_queue')

# Fungsi CRUD untuk tabel penjaga
@app.route('/penjaga', methods=['POST'])
def create_penjaga():
    data = request.json
    nama = data['nama']
    nama_hewan = data['nama_hewan']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO penjaga (nama, nama_hewan) VALUES (%s, %s)", (nama, nama_hewan))
    mysql.connection.commit()
    cur.close()

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='BerhasilDibuat')
    channel.queue_declare(queue='BerhasilDiterima')

    channel.basic_publish(exchange='', routing_key='BerhasilDibuat', body='Data telah dikirim ke Publisher!')
    print(" [x] Sent 'Data Telah Ditambahkan ke Publisher!'")    

    channel.basic_publish(exchange='', routing_key='BerhasilDiterima', body='Data telah dikirim ke Subscriber!')
    print(" [x] Sent 'Data Telah Ditambahkan ke Subscriber!'")
    connection.close()

    return jsonify({'message': 'Penjaga created successfully'}), 201

@app.route('/penjaga/<int:id>', methods=['GET'])
def get_penjaga(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM penjaga WHERE id = %s", (id,))
    result = cur.fetchone()
    cur.close()

    if result:
        return jsonify({'id': result[0], 'nama': result[1], 'nama_hewan': result[2]}), 200
    else:
        return jsonify({'message': 'Penjaga not found'}), 404

@app.route('/penjaga/<int:id>', methods=['PUT'])
def update_penjaga(id):
    data = request.json
    nama = data['nama']
    nama_hewan = data['nama_hewan']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE penjaga SET nama = %s, nama_hewan = %s WHERE id = %s", (nama, nama_hewan, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Penjaga updated successfully'}), 200

@app.route('/penjaga/<int:id>', methods=['DELETE'])
def delete_penjaga(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM penjaga WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Penjaga deleted successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

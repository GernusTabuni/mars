from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# Inisialisasi Flask
app = Flask(__name__)

# Inisialisasi MongoClient
client = MongoClient('mongodb+srv://nusyoman:manis@cluster0.wjeaswn.mongodb.net/test?retryWrites=true&w=majority')

# Pilih database yang sesuai
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/mars", methods=["POST"])
def web_mars_post():
    if request.method == "POST":
        try:
            # Ambil data dari form HTML
            name_receive = request.form['name_give']
            address_receive = request.form['address_give']
            size_receive = request.form['size_give']

            # Buat dokumen yang akan dimasukkan ke MongoDB
            doc = {
                'name': name_receive,
                'address': address_receive,
                'size': size_receive
            }

            # Masukkan dokumen ke koleksi 'orders' di database
            db.orders.insert_one(doc)

            return jsonify({'message': 'Data berhasil dimasukkan ke MongoDB!'})
        except Exception as e:
            return jsonify({'message': 'Terjadi kesalahan saat memasukkan data ke MongoDB.', 'error': str(e)})

@app.route("/mars", methods=["GET"])
def web_mars_get():
    if request.method == "GET":
        try:
            # Ambil semua data dari koleksi 'orders'
            orders_list = list(db.orders.find({}, {'_id': False}))

            return jsonify({'orders': orders_list})
        except Exception as e:
            return jsonify({'message': 'Terjadi kesalahan saat mengambil data dari MongoDB.', 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

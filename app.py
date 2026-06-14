from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher

app = Flask(__name__)

# --- HÀM TẠO GIAO DIỆN KẾT QUẢ DÙNG CHUNG ---
def show_result_page(title, message, original, key, result, back_url):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kết quả xử lý</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" rel="stylesheet"/>
    </head>
    <body class="bg-light mt-5">
        <div class="container" style="max-width: 600px;">
            <div class="card shadow p-4 text-center">
                <h4 class="text-primary">{title}</h4>
                <div class="alert alert-success">{message} thành công!</div>
                <div class="text-left">
                    <p><b>Dữ liệu gốc:</b> {original}</p>
                    <p><b>Khóa:</b> {key}</p>
                    <div class="alert alert-info"><b>Kết quả:</b> {result}</div>
                </div>
                <a href="{back_url}" class="btn btn-primary">← Quay lại</a>
            </div>
            <p class="text-center mt-3 font-weight-bold" style="color: #555;">Nguyễn Thanh Hải / 2380600575</p>
        </div>
    </body>
    </html>
    """

@app.route("/")
def home(): return render_template('index.html')

# --- CAESAR ---
@app.route("/caesar")
def caesar(): return render_template('caesar.html')

@app.route("/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    res = CaesarCipher().encrypt_text(text, key)
    return show_result_page("Caesar Cipher", "Mã hóa", text, key, res, "/caesar")

@app.route("/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    res = CaesarCipher().decrypt_text(text, key)
    return show_result_page("Caesar Cipher", "Giải mã", text, key, res, "/caesar")

# --- VIGENERE ---
@app.route("/vigenere")
def vigenere(): return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text, key = request.form['inputPlainText'], request.form['inputKeyPlain']
    res = VigenereCipher().encrypt_text(text, key)
    return show_result_page("Vigenère Cipher", "Mã hóa", text, key, res, "/vigenere")

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text, key = request.form['inputCipherText'], request.form['inputKeyCipher']
    res = VigenereCipher().decrypt_text(text, key)
    return show_result_page("Vigenère Cipher", "Giải mã", text, key, res, "/vigenere")

# --- PLAYFAIR ---
@app.route("/playfair")
def playfair(): return render_template('playfair.html')

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text, key = request.form['inputPlainText'], request.form['inputKeyPlain']
    matrix = PlayFairCipher().create_playfair_matrix(key)
    res = PlayFairCipher().playfair_encrypt(text, matrix)
    return show_result_page("Playfair Cipher", "Mã hóa", text, key, res, "/playfair")

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text, key = request.form['inputCipherText'], request.form['inputKeyCipher']
    matrix = PlayFairCipher().create_playfair_matrix(key)
    res = PlayFairCipher().playfair_decrypt(text, matrix)
    return show_result_page("Playfair Cipher", "Giải mã", text, key, res, "/playfair")

# --- RAIL FENCE ---
@app.route("/railfence")
def railfence(): return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text, key = request.form['inputPlainText'], int(request.form['inputKeyPlain'])
    res = RailFenceCipher().rail_fence_encrypt(text, key)
    return show_result_page("Rail Fence Cipher", "Mã hóa", text, key, res, "/railfence")

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text, key = request.form['inputCipherText'], int(request.form['inputKeyCipher'])
    res = RailFenceCipher().rail_fence_decrypt(text, key)
    return show_result_page("Rail Fence Cipher", "Giải mã", text, key, res, "/railfence")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
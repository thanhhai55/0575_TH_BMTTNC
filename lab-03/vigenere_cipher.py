import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from ui.vigenere import Ui_Dialog
import requests

class VigenereApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5050/vigenere/encrypt"
        
        plain_text = self.ui.txt_plain_text.toPlainText().strip()
        key_value = self.ui.txt_key.toPlainText().strip()

        if not plain_text:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Plain text!")
            return

        if not key_value:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Key!")
            return

        if not key_value.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa của Vigenere chỉ được chứa các ký tự chữ cái (A-Z, a-z)!")
            return

        payload = {
            "inputPlainText": plain_text,
            "inputKeyPlain": key_value
        }
        
        try:
            response = requests.post(url, data=payload)
            print("Response status code:", response.status_code)

            if response.status_code == 200:
                html_text = response.text
                if '<b>Kết quả:</b>' in html_text:
                    try:
                        result = html_text.split('<b>Kết quả:</b>')[1].split('</div>')[0].strip()
                        self.ui.txt_cipher_text.setPlainText(result)
                        
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Encrypted Successfully")
                        msg.exec_()
                    except Exception as e:
                        print(f"Error parsing HTML response: {e}")
            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5050/vigenere/decrypt"
        
        cipher_text = self.ui.txt_cipher_text.toPlainText().strip()
        key_value = self.ui.txt_key.toPlainText().strip()

        if not cipher_text:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập CipherText!")
            return

        if not key_value:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Key!")
            return

        if not key_value.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa của Vigenere chỉ được chứa các ký tự chữ cái (A-Z, a-z)!")
            return

        payload = {
            "inputCipherText": cipher_text,
            "inputKeyCipher": key_value
        }
        
        try:
            response = requests.post(url, data=payload)
            print("Response status code:", response.status_code)

            if response.status_code == 200:
                html_text = response.text
                if '<b>Kết quả:</b>' in html_text:
                    try:
                        result = html_text.split('<b>Kết quả:</b>')[1].split('</div>')[0].strip()
                        self.ui.txt_plain_text.setPlainText(result)
                        
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Decrypted Successfully")
                        msg.exec_()
                    except Exception as e:
                        print(f"Error parsing HTML response: {e}")
            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_())
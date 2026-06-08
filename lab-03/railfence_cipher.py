import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from ui.railfence import Ui_Dialog
import requests

class RailFenceApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        
        plain_text = self.ui.txt_plain_text.toPlainText().strip()
        key_value = self.ui.txt_key.toPlainText().strip()

        if not plain_text:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Plain text!")
            return

        if not key_value:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Key hàng rào!")
            return

        if not key_value.isdigit():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa của Rail Fence phải là một số nguyên!")
            return

        key_int = int(key_value)
        if key_int < 2:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Số hàng rào (Key) phải lớn hơn hoặc bằng 2!")
            return

        payload = {
            "plain_text": plain_text,
            "key": key_int
        }
        
        try:
            response = requests.post(url, json=payload)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                try:
                    data = response.json()
                    result = data.get("encrypted_text", "")
                    self.ui.txt_cipher_text.setPlainText(result)
                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encrypted Successfully")
                    msg.exec_()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        
        cipher_text = self.ui.txt_cipher_text.toPlainText().strip()
        key_value = self.ui.txt_key.toPlainText().strip()

        if not cipher_text:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập CipherText!")
            return

        if not key_value:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Key hàng rào!")
            return

        if not key_value.isdigit():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa của Rail Fence phải là một số nguyên!")
            return

        key_int = int(key_value)
        if key_int < 2:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Số hàng rào (Key) phải lớn hơn hoặc bằng 2!")
            return

        payload = {
            "cipher_text": cipher_text,
            "key": key_int
        }
        
        try:
            response = requests.post(url, json=payload)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                try:
                    data = response.json()
                    result = data.get("decrypted_text", "")
                    self.ui.txt_plain_text.setPlainText(result)
                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decrypted Successfully")
                    msg.exec_()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import ui.playfair as playfair_ui
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        possible_classes = ["Ui_MainWindow", "Ui_Form", "Ui_Dialog"]
        ui_class = None
        for cls_name in possible_classes:
            if hasattr(playfair_ui, cls_name):
                ui_class = getattr(playfair_ui, cls_name)
                break
        
        if ui_class is None:
            for attr in dir(playfair_ui):
                if attr.startswith("Ui_"):
                    ui_class = getattr(playfair_ui, attr)
                    break

        if ui_class is None:
            QMessageBox.critical(self, "Lỗi cấu trúc", "Không tìm thấy Class UI hợp lệ trong ui/playfair.py!")
            sys.exit(1)

        self.ui = ui_class()
        self.ui.setupUi(self)  
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def validate_key(self, key):
        if not key:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Key!")
            return False
            
        if key.isdigit():
            QMessageBox.warning(self, "Lỗi khóa Playfair", "Khóa của Playfair không được là chữ số!")
            return False

        clean_key = "".join([c for c in key if c.isalpha()])
        if not clean_key:
            QMessageBox.warning(self, "Lỗi khóa Playfair", "Khóa phải chứa ít nhất một chữ cái hợp lệ (A-Z)!")
            return False
            
        return True

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText().strip()
        key_value = self.ui.txt_key.toPlainText().strip()

        if not plain_text:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Plain text!")
            return

        if not self.validate_key(key_value):
            return

        url = "http://127.0.0.1:5050/playfair/encrypt"
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
        cipher_text = self.ui.txt_cipher_text.toPlainText().strip()
        key_value = self.ui.txt_key.toPlainText().strip()

        if not cipher_text:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập CipherText!")
            return

        if not self.validate_key(key_value):
            return

        url = "http://127.0.0.1:5050/playfair/decrypt"
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
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
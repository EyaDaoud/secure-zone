from flask import Flask, request
from flask_cors import CORS
import serial

# Configuration du port série
try:
    ser = serial.Serial('COM3', 115200, timeout=1)  # Remplace COM3 par ton port réel
    print("✅ Port série ouvert :", ser.port)
except Exception as e:
    print("❌ Erreur d'ouverture du port série :", e)
    ser = None

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines (en dev)

@app.route('/send', methods=['POST'])
def recevoir_donnees():
    if not ser:
        return "❌ Port série non disponible", 500

    try:
        json_data = request.get_json()
        contenu = json_data.get("data", "")

        print("\n📥 Données reçues depuis la page web :")
        print(contenu)

        # Envoie les lignes au STM32 via UART
        for ligne in contenu.strip().split('\n'):
            ser.write((ligne + '\n').encode())
            print(f"📤 Envoyé à la STM32 : {ligne}")

        return "✅ Coordonnées envoyées à la STM32"
    except Exception as e:
        return f"❌ Erreur : {str(e)}", 500

if __name__ == '__main__':
    # Lance le serveur sur toutes les interfaces réseau, port 5000
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request
import serial
import threading

# Configuration du port série
try:
    ser = serial.Serial('COM5', 9600, timeout=1)  # ⚠️ remplace COM5 par le port réel de ta STM32
    print("✅ Port série ouvert :", ser.port)
except Exception as e:
    print("❌ Erreur d'ouverture du port série :", e)
    ser = None

# Création de l'application Flask
app = Flask(__name__)

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

# Lancement du serveur Flask sur le por

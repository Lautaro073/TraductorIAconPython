from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Configura tus credenciales de Microsoft Translator aquí
SUBSCRIPTION_KEY = "fed38ec01de24428abf11e345f1b12d8"
ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=es"


headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    "Content-type": "application/json",
    "Ocp-Apim-Subscription-Region": "brazilsouth",  # Ejemplo: "westus2"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    source_text = data['text']
    source_language = data.get('source', 'en')  # Por defecto inglés si no se proporciona
    target_language = data.get('target', 'es')  # Por defecto español si no se proporciona

    # Actualiza el endpoint para incluir los idiomas
    endpoint = f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={source_language}&to={target_language}"

    body = [{"text": source_text}]
    response = requests.post(endpoint, headers=headers, json=body)
    
    if response.status_code == 200:
        translation = response.json()[0]['translations'][0]['text']
        return jsonify(translated=translation)
    else:
        # Devuelve un mensaje de error si la API no responde con un código 200
        return jsonify(error="Error al traducir el texto", details=response.text), 500

if __name__ == '__main__':
    app.run(debug=True)



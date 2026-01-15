from flask import Flask, request, render_template, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

#Cargar las variables de entorno
load_dotenv()

#Inicializar la app
app = Flask(__name__)

#Inicializar el cliente OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/webhook', methods=['POST'])
def webhook():
    msg = request.values.get('Body', '').strip()

    clasificacion = clasificar(msg)
    rsp = generar_respuesta(clasificacion, msg) 

    twilio_rsp = MessagingResponse()
    twilio_rsp.message(rsp)

    return str(twilio_rsp)

def clasificar(msg):
    prompt = f'''
    Clasifica la intención del siguiente mensaje en una sola palabra:
    Saludo, Despedida, Pregunta, Desconocido

    Ejemplo de salida completa: Saludo

    Mensaje: {msg}
    '''

    rsp = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role':'user', 'content':prompt}]
    )
    
    return rsp.choices[0].message.content.strip().lower()

def generar_respuesta(clasificacion, msg):
    if clasificacion == 'saludo':
        return preguntar('Eres un asistente amable, saluda')
    
    if clasificacion == 'despedida':
        return preguntar('Eres un asistente amable, despidete')
    
    if clasificacion == 'pregunta':
        return preguntar(f'Actua como un asistente amable al responder esta pregunta: {msg}')
    
    return preguntar('Eres un asistente amable, di que no entendiste y pide una explicación mas detallada')

def preguntar(msg):
    prompt = msg

    rsp = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role':'user', 'content':prompt}]
    )

    return rsp.choices[0].message.content

'''
@app.route('/chat', methods=['GET'])
def chat_test():
    """Ruta para probar el chatbot desde el navegador"""
    mensaje = request.args.get('mensaje', 'Hola')
    
    clasificacion = clasificar(mensaje)
    respuesta = generar_respuesta(clasificacion, mensaje)
    
    return render_template(
        'chat_test.html',
        mensaje = mensaje,
        clasificacion = clasificacion,
        respuesta = respuesta
    )

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    mensaje = data.get('mensaje', '')

    clasificacion = clasificar(mensaje)
    respuesta = generar_respuesta(clasificacion, mensaje)

    return jsonify({
        'mensaje': mensaje,
        'clasificacion': clasificacion,
        'respuesta': respuesta
    })
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
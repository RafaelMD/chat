from flask import Flask, render_template
from flask_socketio import SocketIO, send
from cep import CepLocator
from websearch import WebSearch
from openaichat import OpenAIChat
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)
socketio = SocketIO(app)
openai_chat = OpenAIChat()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    print('received data: ' + str(data))
    message = openai_chat.chat(data)
    print(message)
    send(message)

def start_server():
    cep_locator = CepLocator()
    web_search = WebSearch()
    openai_chat.add_function(web_search.search, web_search.export_function_search())
    # openai_chat.add_function(cep_locator.cep_to_lat_lng, cep_locator.export_function_cep())
    # openai_chat.add_function(cep_locator.search_places, cep_locator.export_function_search_places())
    socketio.run(app, debug=True)

if __name__ == '__main__':
    start_server()
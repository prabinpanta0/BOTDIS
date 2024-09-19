from flask import Flask, request, jsonify
import bot  # Ensure bot.py is in the same directory or properly imported
from mangum import Mangum
import os
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator

DISCORD_PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY')

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(app)

@app.route('/', methods=['POST'])
def interactions():
    raw_request = request.json
    print(f"💘 Request: {raw_request}")

    

@verify_key_decorator(DISCORD_PUBLIC_KEY)
def interact(raw_request):
    if raw_request['type'] == 1:  # Pong
        return jsonify({"type": 1})  # Pong
    else:
        data = raw_request['data']
        command_name = data['name']

        # Call the function in bot.py that handles the command
        response = bot.handle_command(command_name, data)
        return jsonify(response)
if __name__ == '__main__':
    app.run(debug=True)
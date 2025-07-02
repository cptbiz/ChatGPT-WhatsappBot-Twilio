from flask import Flask, request
import openai
import os
from twilio.twiml.messaging_response import MessagingResponse

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()

    response = MessagingResponse()
    msg = response.message()

    if incoming_msg:
        try:
            chat_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": incoming_msg}]
            )
            reply = chat_response["choices"][0]["message"]["content"]
        except Exception as e:
            reply = f"Erro: {str(e)}"
    else:
        reply = "Envie uma mensagem para começar."

    msg.body(reply)
    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

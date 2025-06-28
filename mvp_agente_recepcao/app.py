from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew

# Carregar variáveis de ambiente
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")  # exemplo: http://localhost:8080/message/sendText/teste
INSTANCE_NAME = os.getenv("EVOLUTION_INSTANCE_NAME")  # exemplo: teste
API_KEY_EVOLUTION = os.getenv("EVOLUTION_API_KEY")

print(f"🔑 OPENAI_API_KEY: {'OK' if OPENAI_API_KEY else '❌ NÃO DEFINIDO'}")
print(f"🌐 EvolutionAPI: {EVOLUTION_API_URL}")

# Inicialização do Flask
app = Flask(__name__)

# Modelo LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Agente do CrewAI
recepcionista_virtual = Agent(
    role="Recepcionista Virtual",
    goal="Atender cordialmente visitantes e esclarecer dúvidas.",
    backstory="Você é uma recepcionista treinada para responder dúvidas gerais com simpatia e clareza.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

# Rota principal do Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("🔎 JSON recebido:")
    print(data)

    try:
        if data.get("event") == "messages.upsert":
            numero = data["data"]["key"]["remoteJid"].split("@")[0]
            mensagem = data["data"]["message"].get("conversation", "")
            print(f"📨 Mensagem recebida de {numero}: {mensagem}")

            tarefa = Task(
                description=f"Responder educadamente à mensagem: '{mensagem}'",
                expected_output="Uma resposta simpática e útil para o visitante.",
                agent=recepcionista_virtual
            )

            crew = Crew(
                agents=[recepcionista_virtual],
                tasks=[tarefa],
                verbose=True
            )

            resultado = crew.kickoff()
            resposta_texto = str(resultado)
            print(f"🤖 Resposta gerada: {resposta_texto}")

            # Salvar conversa em conversa.txt
            with open('conversa.txt', 'a', encoding='utf-8') as arquivo:
                arquivo.write(f"Usuário ({numero}): {mensagem}\nRecepcionista: {resposta_texto}\n---\n")

            resposta = {
                "number": numero,
                "text": resposta_texto,
                "delay": 1200,
                "presence": "composing"
            }

            headers = {
                "Content-Type": "application/json",
                "apikey": API_KEY_EVOLUTION
            }

            envio = requests.post(EVOLUTION_API_URL, json=resposta, headers=headers)
            print(f"📤 Status envio: {envio.status_code}")
            print(f"📤 Retorno EvolutionAPI: {envio.text}")

    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

    return jsonify({"status": "ok"})

# Iniciar servidor local
if __name__ == '__main__':
    app.run(debug=True)

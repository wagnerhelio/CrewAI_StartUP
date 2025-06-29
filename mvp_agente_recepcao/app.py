from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
import datetime

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
    print("\n==================== NOVA REQUISIÇÃO ====================")
    print("🔎 JSON recebido:")
    print(data)

    try:
        event = data.get("event")
        print(f"📌 Evento recebido: {event}")
        if event == "messages.upsert":
            numero = data["data"]["key"]["remoteJid"].split("@")[0]
            jid = data["data"]["key"]["remoteJid"]
            mensagem = data["data"]["message"].get("conversation", "")
            horario_pergunta = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"📨 Mensagem recebida de {numero}: {mensagem} às {horario_pergunta}")

            # Consultar histórico da conversa
            nome_arquivo = f'conversa({jid}).txt'
            historico = ''
            try:
                with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                    historico = arquivo.read()
                print(f"📚 Histórico encontrado para {jid} (últimos 1000 caracteres):\n{historico[-1000:]}")
            except FileNotFoundError:
                print(f"📚 Nenhum histórico encontrado para {jid}.")

            # Adicionar histórico ao contexto da tarefa
            contexto = f"Histórico da conversa:\n{historico[-1000:]}\n\n" if historico else ""
            tarefa = Task(
                description=f"{contexto}Responder educadamente à mensagem: '{mensagem}'",
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
            horario_resposta = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"🤖 Resposta gerada: {resposta_texto} às {horario_resposta}")

            # Salvar conversa em conversa(jid).txt
            nome_arquivo = f'conversa({jid}).txt'
            with open(nome_arquivo, 'a', encoding='utf-8') as arquivo:
                arquivo.write(f"[{horario_pergunta}] Usuário ({numero}): {mensagem}\n")
                arquivo.write(f"[{horario_resposta}] Recepcionista: {resposta_texto}\n---\n")

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

            print(f"\n➡️ Enviando resposta para EvolutionAPI: {EVOLUTION_API_URL}")
            print(f"➡️ Payload: {resposta}")
            print(f"➡️ Headers: {headers}")
            envio = requests.post(EVOLUTION_API_URL, json=resposta, headers=headers)
            print(f"📤 Status envio: {envio.status_code}")
            print(f"📤 Retorno EvolutionAPI: {envio.text}")
        else:
            print(f"⚠️ Evento não tratado: {event}")
            print(f"Conteúdo recebido: {data}")
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

    print("==================== FIM DA REQUISIÇÃO ====================\n")
    return jsonify({"status": "ok"})

# Iniciar servidor local
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

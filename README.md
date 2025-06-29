# CrewAI StartUP - Agente Recepcionista Virtual

Um sistema de recepcionista virtual inteligente que utiliza CrewAI e EvolutionAPI para automatizar o atendimento via WhatsApp. O agente é capaz de responder mensagens de forma educada e contextual, mantendo histórico das conversas.

## 🎯 Funcionalidades

- 🤖 **Agente Inteligente**: Utiliza CrewAI com GPT-4 para gerar respostas contextualizadas
- 💬 **Atendimento WhatsApp**: Integração completa com EvolutionAPI
- 📚 **Histórico de Conversas**: Mantém registro de todas as interações por número
- ⏰ **Timestamps**: Registra horário de cada mensagem enviada e recebida
- 🔄 **Contexto Inteligente**: Consulta histórico anterior para respostas mais relevantes
- 🌐 **Suporte Local e Remoto**: Funciona tanto localmente quanto com ngrok

## ✅ Requisitos

- Python 3.10+
- Git
- EvolutionAPI (Docker ou local)
- Conta OpenAI com API Key

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd CrewAI_StartUP
```

### 2. Configure o ambiente Python
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp .env_example .env

# Edite o arquivo .env com suas configurações
```

### 5. Configure o EvolutionAPI
- Instale e configure o EvolutionAPI (Docker recomendado)
- Configure o webhook para apontar para: `http://SEU_IP:5000/webhook`
- Para uso local: `http://127.0.0.1:5000/webhook`
- Para uso com ngrok: `https://seu-tunnel.ngrok.io/webhook`

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# OpenAI Configuration
OPENAI_API_KEY=sua_chave_api_openai_aqui

# EvolutionAPI Configuration
EVOLUTION_API_URL=http://127.0.0.1:8080/message/sendText/startup
EVOLUTION_INSTANCE_NAME=startup
EVOLUTION_API_KEY=sua_chave_api_evolution_aqui
```

### Configuração do EvolutionAPI

1. **Webhook URL**: Configure para `http://SEU_IP:5000/webhook`
2. **Instance Name**: Use o mesmo nome configurado em `EVOLUTION_INSTANCE_NAME`
3. **API Key**: Configure a mesma chave em `EVOLUTION_API_KEY`

## 🏃‍♂️ Como Executar

### 1. Inicie o EvolutionAPI
```bash
# Se usando Docker
docker run -d --name evolution_api evolution-api

# Ver logs
docker logs evolution_api
```

### 2. Inicie o Flask (Agente Recepcionista)
```bash
cd mvp_agente_recepcao
python app.py
```

### 3. Para uso externo (opcional)
```bash
# Se precisar expor para internet
ngrok http 5000
```

## 📁 Estrutura do Projeto

```
CrewAI_StartUP/
├── mvp_agente_recepcao/
│   ├── app.py              # Aplicação principal Flask
│   └── conversa(jid).txt   # Histórico de conversas (gerado automaticamente)
├── agentes/
│   └── recepcionista.py    # Definição do agente
├── requirements.txt        # Dependências Python
├── .env_example           # Exemplo de configuração
└── README.md              # Este arquivo
```

## 🔧 Desenvolvimento

### Comandos Úteis

```bash
# Ativar ambiente virtual
.\venv\Scripts\Activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python mvp_agente_recepcao/app.py

# Testar webhook manualmente
curl -X POST http://127.0.0.1:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event":"messages.upsert","data":{"key":{"remoteJid":"556299999999@s.whatsapp.net"},"message":{"conversation":"Teste"}}}'
```

### Logs e Debug

O sistema gera logs detalhados incluindo:
- 📨 Mensagens recebidas com timestamp
- 🤖 Respostas geradas pelo agente
- 📚 Histórico consultado
- 📤 Status de envio para EvolutionAPI
- ❌ Erros e exceções

## 📝 Histórico de Conversas

Cada conversa é salva em um arquivo separado:
- **Formato**: `conversa(jid).txt`
- **Conteúdo**: Mensagens com timestamps
- **Localização**: `mvp_agente_recepcao/`

Exemplo:
```
[2025-06-29 19:00:00] Usuário (5562992422540): Olá, tudo bem?
[2025-06-29 19:00:01] Recepcionista: Olá! Tudo ótimo, como posso ajudar?
---
```

## 🛠️ Troubleshooting

### Problemas Comuns

1. **Erro de conexão recusada**
   - Verifique se o Flask está rodando com `host='0.0.0.0'`
   - Confirme se a porta 5000 está liberada

2. **EvolutionAPI não envia webhooks**
   - Verifique a URL do webhook no painel
   - Confirme se o IP está correto

3. **Erro de API Key**
   - Verifique se as chaves no `.env` estão corretas
   - Confirme se as chaves têm permissões adequadas

## 📄 Licença

Este projeto é de uso interno para testes e desenvolvimento.

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request 
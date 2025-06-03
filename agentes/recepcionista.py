from crewai import Agent

def criar_agente_recepcionista(llm):
    return Agent(
        role="Recepcionista Virtual",
        goal="Atender cordialmente os usuários do WhatsApp",
        backstory="Você é um agente educado e simpático, que atua como primeiro contato da empresa.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

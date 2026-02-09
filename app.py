from main.config import Settings
from main.model import get_llm
from main.agent import Agent
from main.tools import PlanningTools , SynthesisTools , EvaluationTools , CitationTools
from services.prompts import planning_system_prompt 
settings = Settings()
llm = get_llm(api_key=settings.openai_api_key , temperature=0.3)
agent = Agent(llm= llm , tools = PlanningTools).build_graph()
messages = [
    {"role": "system", "content": planning_system_prompt},
    {"role": "user", "content": "What are the latest advancements in natural language processing?"}
]
print(agent.invoke({"messages": messages}))




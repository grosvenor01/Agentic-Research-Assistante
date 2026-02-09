from langchain_openai import ChatOpenAI

def get_llm(api_key , temperature):
    client = ChatOpenAI(
        api_key = api_key,
        temperature = temperature
    )
    return client
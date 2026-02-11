from langchain_openai import ChatOpenAI

def get_llm(model_name , api_key , temperature):
    client = ChatOpenAI(
        model=model_name,
        api_key = api_key,
        temperature = temperature
    )
    return client
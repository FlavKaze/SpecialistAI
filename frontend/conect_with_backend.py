import requests
import config

def make_query(chat_id: str, messages: list):
    response = requests.post(url=f"{config.BACKEND_URI}/query", json={"chat_id": chat_id, "messages": messages})
    
    return response.json()

def list_knowledge_base():
    try:
        response = requests.get(url=f"{config.BACKEND_URI}/list_knowledge_base")
        return response.json()
    except:
        return []

def call_create_context(files=[], keyword=None):
    history = []
    if keyword:
        response = requests.post(url=f"{config.BACKEND_URI}/create_context_from_text", json={"keyword": keyword.replace("/", "")})
        history.append(response.text)
    elif files:
        for file in files:
            response = requests.post(url=f"{config.BACKEND_URI}/create_context_from_file", files={"file": file})
            history.append(f"File: {file} - {response.text}")
    return history if history else ["Error!"]


if __name__ == "__main__":
    print(make_query("123", [{"message_id": "123", "message": "Hello", "site": "stackoverflow"}]))
import ollama
from ollama import Client
import nltk


nltk.download('punkt')


def chat_inference(prompt):
    # client = Client(host='https://bff5-34-70-133-48.ngrok-free.app')
    #client for access ollama api remotely
    # client.chat(model='mistral', messages=[])
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return response['message']['content']

def rag_inference(message, context):
    context = '\n- '.join(context)
    prompt = f"""
    Given only the following information :

    -{context}

    answer the following question: {message}

    if the answer can't be found in the texts above, respond "I don't know"
"""
    return chat_inference(prompt)


def make_embeddings(text):
    embeddings = ollama.embeddings(
        model='mxbai-embed-large',
        prompt=text
    )
    return embeddings


def split_sentences(paragraph_text) -> list:
    # sentences = re.split(r'[\.,]', paragraph_text)
    # sentences = [s.strip().lower() for s in sentences if len(s) > 5]
    # return sentences
    paragraph_text = paragraph_text.replace(":", ".").replace(";", ".")
    sentence_tokenize = nltk.tokenize.sent_tokenize(
        paragraph_text, language='portuguese'
    )
    return sentence_tokenize


def split_sentences(sentence) -> list:
    # sentences = re.split(r'[\.,]', paragraph_text)
    # sentences = [s.strip().lower() for s in sentences if len(s) > 5]
    # return sentences
    # sentence = sentence.replace(":", ".").replace(";", ".")
    sentence_tokenize = nltk.tokenize.sent_tokenize(
        sentence, language='portuguese'
    )
    return sentence_tokenize


if __name__ == "__main__":
    print(rag_inference("quantos anos tem o homem formiga??", [""]))
    # print(make_embeddings("Who is Homer Simpson?"))
    
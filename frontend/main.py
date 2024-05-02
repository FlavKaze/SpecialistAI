import gradio as gr
import time
from conect_with_backend import make_query, call_create_context, list_knowledge_base

def rs_change():
    return gr.Dropdown(list_knowledge_base(), label="Select existed knowledge", )

def process_file(message):
    files = message["files"]
    return_text = call_create_context(files)
    return return_text

def process_text(keyword):
    return_text = call_create_context(keyword=keyword)
    return return_text

def process_message(message, history, name_select):
    num_files = len(message["files"])

    if num_files > 0:
        texts = process_file(message)
        return " ".join(texts)
    if message["text"].startswith("/"):
        texts = process_text(message["text"])
        return " ".join(texts)
        
    if not name_select:
        return "Please select a knowledge base"
    chat = make_query(name_select, [{"message_id": "", "message": message["text"], "site": ""}])
    return chat["message"]


with gr.Blocks() as SpecialistAI:

    knowledge = gr.Dropdown(list_knowledge_base(), label="Select existed knowledge", )
    bt = gr.Button("Refresh knowledge base")
    chat_i = gr.ChatInterface(
        process_message,
        additional_inputs=[knowledge],
        title="SpecialistAI", 
        multimodal=True, 
    )
    bt.click(fn=rs_change, outputs=knowledge)


if __name__ == '__main__':
    SpecialistAI.queue().launch()

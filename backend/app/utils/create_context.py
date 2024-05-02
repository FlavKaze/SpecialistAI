import os
from hashlib import md5
import pickle
from tqdm import tqdm


import config
from app.utils.tools import make_embeddings
from app.utils.web_scrapping import find_in_sites
from app.utils.ocr import read_image, read_pdf
from app.utils.database import create_table


def load_data_to_db(data):
    for key, value in data.items():
        create_table(key, uri=config.db_name, data=value)
        

def create_db_context(text: str) -> dict:
    """Create context for database."""
    embeddings = make_embeddings(text)    
    if not embeddings:
        return None

    if not embeddings['embedding']:
        return None

    infos = {
        'vector': embeddings['embedding'],
        'text': text,
        'site': ""
    }
    return infos    
    
def make_pickle(infos: dict, filename: str) -> str:
    """create or update pickle file"""
    try:
        data_info = pickle.load(open(filename, "rb"))
        data_info.update(infos)
        pickle.dump(data_info, open(filename, "wb"))
    except:
        pickle.dump(infos, open(filename, "wb"))
        
    return "Pickle file created successfully!"

def generate_contexts_from_sites(theme: str) -> None:
    """Generate contexts from sites."""
    results = find_in_sites(theme, find_size=1, url_site="https://pt.wikipedia.org/wiki/")
    all_contexts = []
    for site, texts in tqdm(results.items(), desc="Making embeddings", position=0, leave=True):
        for text in tqdm(texts, desc=f"Site: {site}", position=1, leave=True):
            all_contexts.append(create_db_context(text)) 
    infos = {theme: all_contexts}
    make_pickle(infos, config.DB_FILE_NAME)
    load_data_to_db(infos)

def generate_contexts_from_file(file: bytes) -> None:
    """Generate contexts from file."""
    filename = os.fsdecode(file).split("/")[-1]
    # create a hash for the filename
    
    if filename.endswith(".pdf"):
        pages = read_pdf(os.fsdecode(file))
    else:
        pages = [read_image(image_path=file)]
    all_contexts = []
    # all_text = []
    for page in tqdm(pages, desc="Making embeddings", position=0, leave=True):
        for splited_text in page.split("\n"):
            if not splited_text:
                continue
            all_contexts.append(create_db_context(splited_text))
            # all_text.append(splited_text)
    # all_contexts.append(create_db_context(" ".join(all_text)))
        
    file_hash = md5(filename.encode()).hexdigest()
    infos = {file_hash: all_contexts}
    make_pickle(infos, config.DB_FILE_NAME)
    load_data_to_db(infos)


if __name__ == "__main__":
    generate_contexts_from_sites("Homem-Formiga")
    print("Done!")

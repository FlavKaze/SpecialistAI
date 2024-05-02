from io import BytesIO
import pytesseract
from PIL import Image
import fitz
# pip install PyMuPDF


def read_image(image_path: bytes = None, image_bytes: bytes = None) -> str:
    if image_path:
        image = Image.open(image_path)
    elif image_bytes:
        image = Image.open(BytesIO(image_bytes))
    else:
        raise ValueError("Either image_path or image_bytes must be provided.")
    
    return pytesseract.image_to_string(image)


def read_pdf(pdf_path: bytes) -> str:
    # doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    doc = fitz.open(pdf_path)
    texts = []
    for page in range(doc.page_count):
        page = doc[page]
        image_pix_map = page.get_pixmap()
        # Convert to tensor
        # image = tf.io.decode_jpeg(image_pix_map.tobytes())
        image_bytes = image_pix_map.tobytes()
        text = read_image(image_bytes=image_bytes)
        texts.append(text)
    return texts
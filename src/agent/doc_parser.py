import io
from pypdf import PdfReader
import docx

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    ext = filename.lower().split('.')[-1]
    text = ''

    if ext == 'pdf':
        reader = PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                pages_text.append(t)
        text = '\n\n'.join(pages_text)

    elif ext in ('docx', 'doc'):
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            paras = [p.text for p in doc.paragraphs if p.text.strip()]
            text = '\n'.join(paras)
        except Exception:
            text = file_bytes.decode('utf-8', errors='ignore')

    elif ext in ('txt', 'md'):
        text = file_bytes.decode('utf-8', errors='ignore')

    else:
        text = file_bytes.decode('utf-8', errors='ignore')

    return text.strip()

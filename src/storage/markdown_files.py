from pathlib import Path
from fastapi.responses import PlainTextResponse

OUTPUT_DIR = Path ('output')
def save_markdown (filename: str, markdown: str):
    OUTPUT_DIR.mkdir(exist_ok = True)
    path = OUTPUT_DIR / filename
    path.write_text(markdown, encoding = 'utf-8')
    return path 

def load_markdown (filename: str): 
    path = OUTPUT_DIR / filename
    return path.read_text (encoding = 'utf-8')
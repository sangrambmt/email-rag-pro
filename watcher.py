import time
import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.embed import get_collection
from app.chunk import chunk_text
from app.extractors import extract_text

EMAIL_DIR = "data/emails"
STATE_FILE = "data/index/indexed.txt"

SUPPORTED_EXTENSIONS = {'.txt', '.docx', '.pdf', '.pptx', '.ppt'}

def get_indexed():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_indexed(hashes):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        for h in hashes:
            f.write(h + "\n")

def is_supported_file(path):
    """Check if file extension is supported"""
    ext = os.path.splitext(path)[1].lower()
    return ext in SUPPORTED_EXTENSIONS

def index_file(path):
    indexed = get_indexed()

    text = extract_text(path)
    
    if not text.strip():
        print(f"No text extracted from: {os.path.basename(path)}")
        return

    chunks = chunk_text(text)

    collection = get_collection()

    new_hashes = set(indexed)

    for i, chunk in enumerate(chunks):
        h = hashlib.md5((path + str(i)).encode()).hexdigest()
        if h in indexed:
            continue

        collection.add(
            documents=[chunk],
            metadatas=[{"file": os.path.basename(path)}],
            ids=[h]
        )
        new_hashes.add(h)

    save_indexed(new_hashes)
    print("Indexed:", os.path.basename(path))

def scan_existing():
    """Index all existing supported files on startup"""
    if not os.path.exists(EMAIL_DIR):
        return
    
    for filename in os.listdir(EMAIL_DIR):
        path = os.path.join(EMAIL_DIR, filename)
        if os.path.isfile(path) and is_supported_file(path):
            try:
                index_file(path)
            except Exception as e:
                print(f"Error indexing {filename}: {e}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if is_supported_file(event.src_path):
            time.sleep(1)
            try:
                index_file(event.src_path)
            except Exception as e:
                print(f"Error indexing {event.src_path}: {e}")

if __name__ == "__main__":
    os.makedirs(EMAIL_DIR, exist_ok=True)
    
    print("Scanning existing files...")
    scan_existing()
    
    print("Watching folder:", EMAIL_DIR)
    print("Supported formats:", ", ".join(SUPPORTED_EXTENSIONS))
    
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, EMAIL_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
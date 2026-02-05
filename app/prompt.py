import os
import re
from imapclient import IMAPClient
import pyzmail
from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")
IMAP_FOLDER = os.getenv("IMAP_FOLDER", "INBOX")

SAVE_DIR = "data/emails"

os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(name):
    """Remove special characters and limit length"""
    name = re.sub(r'[^\w\s-]', '', name)
    name = name.replace(' ', '_')
    return name[:50]

def main():
    try:
        with IMAPClient(IMAP_HOST) as server:
            server.login(IMAP_USER, IMAP_PASSWORD)
            server.select_folder(IMAP_FOLDER)
            messages = server.search(["UNSEEN"])

            for uid in messages:
                raw = server.fetch([uid], ["RFC822"])[uid][b"RFC822"]
                msg = pyzmail.PyzMessage.factory(raw)

                subject = msg.get_subject() or "no_subject"
                filename = f"{uid}_{sanitize_filename(subject)}.txt"

                if msg.text_part:
                    text = msg.text_part.get_payload().decode(
                        msg.text_part.charset or "utf-8", 
                        errors="ignore"
                    )
                else:
                    text = ""

                path = os.path.join(SAVE_DIR, filename)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)

                server.add_flags(uid, [b"\\Seen"])
                print("Saved:", filename)
                
    except Exception as e:
        print(f"Error fetching emails: {e}")

if __name__ == "__main__":
    main()
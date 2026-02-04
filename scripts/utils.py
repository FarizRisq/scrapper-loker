import re

def clean_text(text):
    """Fungsi simpel buat hapus spasi berlebih dan karakter aneh"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text) # Hapus extra spaces/newlines
    return text.strip()

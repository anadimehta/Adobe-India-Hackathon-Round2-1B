import re

def clean_text(text: str) -> str:
    ligatures = {
        '\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl',
        '\ufb03': 'ffi', '\ufb04': 'ffl', '\ufb05': 'ft', '\ufb06': 'st',
    }
    for uni, ascii_equiv in ligatures.items():
        text = text.replace(uni, ascii_equiv)
    text = text.replace('\\u2022', '-').replace('•', '-').replace('-.', '-')
    text = text.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    text = re.sub(r'#+' , '', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r"[ ]{2,}", ' ', text)
    text = re.sub(r"\s*\n+\s*", ' ', text)
    parts = [p.strip() for p in text.split('. ') if p.strip()]
    text = '. '.join(parts)
    text = text.strip(' .')
    if text:
        text = text[0].upper() + text[1:]
    return text
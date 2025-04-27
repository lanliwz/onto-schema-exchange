import re

def remove_js_format(js_code: str) -> str:
    # Remove single-line comments (//)
    js_code = re.sub(r'//.*', '', js_code)
    # Remove multi-line comments (/* ... */)
    js_code = re.sub(r'/\*[\s\S]*?\*/', '', js_code)
    # Remove newlines and excessive whitespace
    js_code = re.sub(r'\s+', ' ', js_code)
    # Remove spaces around symbols
    js_code = re.sub(r'\s*([{}();,:=<>+\-*/&|^%!~\[\]])\s*', r'\1', js_code)
    return js_code.strip()
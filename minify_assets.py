import re
import os

def minify_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL) # Remove comments
    css = re.sub(r'\s+', ' ', css) # Collapse whitespace
    css = re.sub(r'\s*([{:;,])\s*', r'\1', css) # Remove space around delimiters
    return css.strip()

def minify_js(js):
    # Very basic minification: remove comments and extra whitespace
    js = re.sub(r'(?<!:)\/\/.*', '', js) # Remove single line comments
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL) # Remove multi-line comments
    js = re.sub(r'\s+', ' ', js) # Collapse whitespace
    return js.strip()

def process():
    # CSS
    if os.path.exists('index.css'):
        with open('index.css', 'r', encoding='utf-8') as f:
            content = f.read()
        minified = minify_css(content)
        with open('index.min.css', 'w', encoding='utf-8') as f:
            f.write(minified)
        print("Minified index.css -> index.min.css")

    # JS
    if os.path.exists('main.js'):
        with open('main.js', 'r', encoding='utf-8') as f:
            content = f.read()
        minified = minify_js(content)
        with open('main.min.js', 'w', encoding='utf-8') as f:
            f.write(minified)
        print("Minified main.js -> main.min.js")

if __name__ == "__main__":
    process()

import glob

def update_html_to_min():
    files = glob.glob('**/*.html', recursive=True)
    updated_count = 0
    
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        modified = False
        
        # Update CSS
        if 'index.css' in content:
            content = content.replace('index.css', 'index.min.css')
            modified = True
            
        # Update JS
        if 'main.js' in content:
            content = content.replace('main.js', 'main.min.js')
            modified = True
            
        if modified:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            updated_count += 1
            print(f"Updated HTML to minified assets: {f}")

    print(f"Total files updated to minified: {updated_count}")

if __name__ == "__main__":
    update_html_to_min()

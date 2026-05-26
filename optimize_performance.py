import glob
import re
import os

def add_lazy_loading():
    files = glob.glob('**/*.html', recursive=True)
    updated_count = 0
    
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Avoid adding lazy loading to the first image (usually hero)
        # We'll use a regex that skips the first match or we can target specific sections
        
        modified = False
        
        # Find all <img> tags
        img_tags = re.findall(r'<img [^>]*>', content)
        
        if len(img_tags) > 1:
            # Skip the first image (often hero)
            for img in img_tags[1:]:
                if 'loading=' not in img:
                    new_img = img.replace('>', ' loading="lazy">')
                    content = content.replace(img, new_img)
                    modified = True
        
        if modified:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            updated_count += 1
            print(f"Added lazy loading to: {f}")

    print(f"Total files updated with lazy loading: {updated_count}")

if __name__ == "__main__":
    add_lazy_loading()

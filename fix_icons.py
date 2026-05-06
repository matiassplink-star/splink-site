import glob

instagram_lucide = '<i data-lucide="instagram"></i>'
instagram_svg = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>'

files = glob.glob('*.html')
updated_count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if instagram_lucide in content:
        content = content.replace(instagram_lucide, instagram_svg)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        updated_count += 1
        print(f"Updated icons in: {f}")

print(f"Total files updated: {updated_count}")

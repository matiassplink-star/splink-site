import glob

verification_code = 'aHEHNBz0j-5mHSzAb2bTGRdYNlMGnZXwgwKpOoa4TRw'
meta_tag = f'\n    <meta name="google-site-verification" content="{verification_code}" />'

files = glob.glob('*.html')
updated_count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'google-site-verification' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'{meta_tag}\n</head>')
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            updated_count += 1
            print(f"Added verification to: {f}")

print(f"Total files updated: {updated_count}")

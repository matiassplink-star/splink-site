import glob

measurement_id = 'G-9TRYN4VYKG'
analytics_script = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{measurement_id}');
    </script>
"""

files = glob.glob('*.html')
updated_count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if measurement_id not in content:
        if '<head>' in content:
            # Insert right after <head>
            content = content.replace('<head>', f'<head>{analytics_script}')
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            updated_count += 1
            print(f"Added GA4 tracking to: {f}")

print(f"Total files updated: {updated_count}")

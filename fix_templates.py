import os
import re
from pathlib import Path

TEMPLATES_DIR = "backend/urbanatura_cdmx/templates"

def fix_template(file_path):
    with open(file_path, 'r+') as f:
        content = f.read()
        
        # Corregir {% static %} anidadas
        content = re.sub(r'\{% static .*\{% static (.*?) %\}.*%\}', r'{% static \1 %}', content)
        
        # Corregir CDNs mal formados
        content = re.sub(r'href="css/href="(https?://[^"]+)"', r'href="\1"', content)
        
        # Asegurar {% load static %} al inicio
        if not re.search(r'^\s*\{% load static %\}', content, re.MULTILINE):
            content = "{% load static %}\n" + content
        
        f.seek(0)
        f.write(content)
        f.truncate()

if __name__ == "__main__":
    for root, _, files in os.walk(TEMPLATES_DIR):
        for file in files:
            if file.endswith('.html'):
                fix_template(Path(root) / file)
    print("¡Templates corregidos!")
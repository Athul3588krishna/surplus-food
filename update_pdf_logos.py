import re
import base64

with open('d:/surplus-food/ktu_logo.jpg', 'rb') as f:
    ktu_b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

with open('d:/surplus-food/mea_emblem.jpg', 'rb') as f:
    mea_b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

with open('d:/surplus-food/build_full_report.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace student and guide information
content = content.replace("ATHUL KRISHNA R (MEA24MCA-XXXX)", "RISHIN V (MEA25MCA2021)")
content = content.replace("ATHUL KRISHNA R", "RISHIN V")
content = content.replace("MEA24MCA-XXXX", "MEA25MCA2021")
content = content.replace("Ms. Prajina K", "Mrs. Fathimath Hasna")
content = content.replace("Mrs. Sruti Sudevan", "Mr. Sajeesh M")
content = content.replace("Assistant Professor & Head", "Assistant Professor")

# Replace KTU SVG block with KTU image
ktu_img_tag = f'<div style="margin: 12px 0;"><img src="{ktu_b64}" style="width: 85px; height: auto;" alt="KTU Logo" /></div>'
content = re.sub(r'<!-- KTU Logo SVG -->\s*<div style="margin: 10px 0;">\s*<svg.*?</svg>\s*</div>', ktu_img_tag, content, flags=re.DOTALL)

# Replace MEA SVG blocks with MEA image
mea_img_cover = f'<div style="margin: 12px 0;"><img src="{mea_b64}" style="width: 95px; height: auto;" alt="MEA Emblem" /></div>'
content = re.sub(r'<!-- MEA Emblem SVG -->\s*<div style="margin: 10px 0;">\s*<svg.*?</svg>\s*</div>', mea_img_cover, content, flags=re.DOTALL)

mea_img_cert = f'<div style="text-align: center; margin: 20px 0;"><img src="{mea_b64}" style="width: 90px; height: auto;" alt="MEA Emblem" /></div>'
content = re.sub(r'<!-- MEA Emblem -->\s*<div style="text-align: center; margin: 25px 0;">\s*<svg.*?</svg>\s*</div>', mea_img_cert, content, flags=re.DOTALL)

with open('d:/surplus-food/build_full_report.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated build_full_report.py with exact credentials and authentic logos.")

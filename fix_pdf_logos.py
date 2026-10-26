import base64
import os

with open(r"d:\surplus-food\extracted_assets\word\media\image1.png", "rb") as f:
    ktu_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open(r"d:\surplus-food\extracted_assets\word\media\image2.png", "rb") as f:
    mea_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open(r"d:\surplus-food\build_full_report.py", "r", encoding="utf-8") as f:
    code = f.read()

import re

# Find and replace the KTU and MEA embedded images
# In build_full_report.py, look for the cover page img tags
# First img is KTU, second is MEA, third in certificate is MEA

# Let's inspect the exact lines around KTU in build_full_report.py
lines = code.split("\n")
new_lines = []
img_counter = 0

for line in lines:
    if '<img src="data:image/jpeg;base64,' in line:
        img_counter += 1
        if img_counter == 1:
            # KTU logo
            new_lines.append(f'    <div style="margin: 12px 0;"><img src="{ktu_b64}" style="width: 95px; height: auto;" /></div>')
        elif img_counter == 2:
            # MEA crest cover
            new_lines.append(f'    <div style="margin: 12px 0;"><img src="{mea_b64}" style="width: 110px; height: auto;" /></div>')
        elif img_counter == 3:
            # MEA crest certificate
            new_lines.append(f'    <div style="text-align: center; margin: 15px 0;"><img src="{mea_b64}" style="width: 100px; height: auto;" /></div>')
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

print(f"Replaced {img_counter} base64 logo occurrences in build_full_report.py")

with open(r"d:\surplus-food\build_full_report.py", "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))

print("build_full_report.py updated with the EXACT real logos.")

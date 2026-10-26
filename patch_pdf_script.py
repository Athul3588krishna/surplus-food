with open(r"d:\surplus-food\update_pdf_logos.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("Ms. Fathmath Hasna", "Mrs. Fathimath Hasna")
text = text.replace("Fathmath Hasna", "Fathimath Hasna")

with open(r"d:\surplus-food\update_pdf_logos.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated update_pdf_logos.py with Mrs. Fathimath Hasna")

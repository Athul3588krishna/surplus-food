with open(r"d:\surplus-food\create_docx.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("Ms. Fathmath Hasna", "Mrs. Fathimath Hasna")
text = text.replace("Fathmath Hasna", "Fathimath Hasna")

with open(r"d:\surplus-food\create_docx.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated create_docx.py with Mrs. Fathimath Hasna")

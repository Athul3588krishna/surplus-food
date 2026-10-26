with open(r"d:\surplus-food\create_docx.py", "r", encoding="utf-8") as f:
    text = f.read()

old_app = """for filename, caption in screenshots_data:
    img_path = os.path.join("d:/surplus-food/screenshots", filename)
    if os.path.exists(img_path):
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(14)
        p_cap.paragraph_format.space_after = Pt(6)
        r = p_cap.add_run(caption)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(20)
        p_img.add_run().add_picture(img_path, width=Inches(6.2))"""

new_app = """for filename, caption in screenshots_data:
    img_path = os.path.join("d:/surplus-food/screenshots", filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(14)
        p_img.paragraph_format.space_after = Pt(6)
        p_img.add_run().add_picture(img_path, width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(20)
        r = p_cap.add_run(caption)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True"""

assert old_app in text, "old_app snippet not found!"
text = text.replace(old_app, new_app)

with open(r"d:\surplus-food\create_docx.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Appendix layout updated in create_docx.py successfully.")

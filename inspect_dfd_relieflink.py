import docx

doc = docx.Document(r"C:\Users\User\Downloads\ReliefLink_Final_Report_v33.docx")
for i in range(408, 450):
    p = doc.paragraphs[i]
    if p.text.strip() or len(p.runs) > 0:
        has_img = any("drawing" in r._element.xml for r in p.runs)
        print(f"P{i} [img={has_img}]: {p.text.strip()}")

import os

with open(r"d:\surplus-food\create_docx.py", "r", encoding="utf-8") as f:
    text = f.read()

old_uc = '''add_heading_2("6.4 Use Case Diagram")
add_para("A use case diagram is a visual representation that shows how different users (called actors) interact with a system to achieve specific goals. It is one of the primary diagrams used in UML to capture functional requirements. Each use case represents a particular function or service the system provides, and the relationships between actors and use cases show who can perform which actions.")'''

new_uc = '''add_heading_2("6.4 Use Case Diagram")
add_para("A use case diagram is a visual representation that shows how different users (called actors) interact with a system to achieve specific goals. It is one of the primary diagrams used in UML to capture functional requirements. Each use case represents a particular function or service the system provides, and the relationships between actors and use cases show who can perform which actions. This helps developers and stakeholders quickly understand what the system is supposed to do from a user's perspective, without needing to go deep into technical details.")

if os.path.exists("d:/surplus-food/diagrams/use_case_diagram.png"):
    p_uc = doc.add_paragraph()
    p_uc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uc.paragraph_format.space_before = Pt(12)
    p_uc.paragraph_format.space_after = Pt(6)
    p_uc.add_run().add_picture("d:/surplus-food/diagrams/use_case_diagram.png", width=Inches(5.5))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(14)
    rcap = p_cap.add_run("Figure 6.1: UML Use Case Diagram - Surplus Food Rescue & Marketplace")
    rcap.font.name = "Times New Roman"
    rcap.font.size = Pt(10.5)
    rcap.font.bold = True'''

old_dfd = '''add_heading_2("6.6 Data Flow Diagram")
add_para("The Data Flow Diagrams (DFD) represent the logical flow and movement of data throughout the Surplus Food platform across Level 0 (Context Diagram), Level 1 (Role-specific process flows for Admin, Customer, and Restaurant Partner), and Level 2 (Detailed administrative process decomposition).")'''

new_dfd = '''add_heading_2("6.6 Data Flow Diagram")
add_para("The Data Flow Diagrams (DFD) represent the logical flow and movement of data throughout the Surplus Food platform across Level 0 (Context Diagram), Level 1 (Role-specific process flows for Admin, Customer, and Restaurant Partner), and Level 2 (Detailed administrative process decomposition).")

add_heading_3("Level 0 (Context Diagram)")
if os.path.exists("d:/surplus-food/diagrams/dfd_level_0.png"):
    p_dfd0 = doc.add_paragraph()
    p_dfd0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dfd0.paragraph_format.space_before = Pt(10)
    p_dfd0.paragraph_format.space_after = Pt(6)
    p_dfd0.add_run().add_picture("d:/surplus-food/diagrams/dfd_level_0.png", width=Inches(5.8))
    
    p_cap0 = doc.add_paragraph()
    p_cap0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap0.paragraph_format.space_after = Pt(14)
    rcap0 = p_cap0.add_run("Figure 6.2: DFD Level 0 (Context Diagram) - Surplus Food Rescue System")
    rcap0.font.name = "Times New Roman"
    rcap0.font.size = Pt(10.5)
    rcap0.font.bold = True

add_heading_3("Level 1 (Administrator Module)")
if os.path.exists("d:/surplus-food/diagrams/dfd_level_1_admin.png"):
    p_dfd1a = doc.add_paragraph()
    p_dfd1a.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dfd1a.paragraph_format.space_before = Pt(10)
    p_dfd1a.paragraph_format.space_after = Pt(6)
    p_dfd1a.add_run().add_picture("d:/surplus-food/diagrams/dfd_level_1_admin.png", width=Inches(5.8))
    
    p_cap1a = doc.add_paragraph()
    p_cap1a.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap1a.paragraph_format.space_after = Pt(14)
    rcap1a = p_cap1a.add_run("Figure 6.3: DFD Level 1 - Administrator Management Flow")
    rcap1a.font.name = "Times New Roman"
    rcap1a.font.size = Pt(10.5)
    rcap1a.font.bold = True

add_heading_3("Level 1 (Customer Module)")
if os.path.exists("d:/surplus-food/diagrams/dfd_level_1_customer.png"):
    p_dfd1c = doc.add_paragraph()
    p_dfd1c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dfd1c.paragraph_format.space_before = Pt(10)
    p_dfd1c.paragraph_format.space_after = Pt(6)
    p_dfd1c.add_run().add_picture("d:/surplus-food/diagrams/dfd_level_1_customer.png", width=Inches(5.8))
    
    p_cap1c = doc.add_paragraph()
    p_cap1c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap1c.paragraph_format.space_after = Pt(14)
    rcap1c = p_cap1c.add_run("Figure 6.4: DFD Level 1 - Customer Discovery, Booking & Collection Flow")
    rcap1c.font.name = "Times New Roman"
    rcap1c.font.size = Pt(10.5)
    rcap1c.font.bold = True

add_heading_3("Level 1 (Restaurant Partner Module)")
if os.path.exists("d:/surplus-food/diagrams/dfd_level_1_restaurant.png"):
    p_dfd1r = doc.add_paragraph()
    p_dfd1r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dfd1r.paragraph_format.space_before = Pt(10)
    p_dfd1r.paragraph_format.space_after = Pt(6)
    p_dfd1r.add_run().add_picture("d:/surplus-food/diagrams/dfd_level_1_restaurant.png", width=Inches(5.8))
    
    p_cap1r = doc.add_paragraph()
    p_cap1r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap1r.paragraph_format.space_after = Pt(14)
    rcap1r = p_cap1r.add_run("Figure 6.5: DFD Level 1 - Restaurant Partner Inventory & Order Queue Flow")
    rcap1r.font.name = "Times New Roman"
    rcap1r.font.size = Pt(10.5)
    rcap1r.font.bold = True

add_heading_3("Level 2 (Administrator Process Decomposition)")
if os.path.exists("d:/surplus-food/diagrams/dfd_level_2_admin.png"):
    p_dfd2a = doc.add_paragraph()
    p_dfd2a.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dfd2a.paragraph_format.space_before = Pt(10)
    p_dfd2a.paragraph_format.space_after = Pt(6)
    p_dfd2a.add_run().add_picture("d:/surplus-food/diagrams/dfd_level_2_admin.png", width=Inches(5.8))
    
    p_cap2a = doc.add_paragraph()
    p_cap2a.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap2a.paragraph_format.space_after = Pt(14)
    rcap2a = p_cap2a.add_run("Figure 6.6: DFD Level 2 - Detailed Administrator Process Decomposition")
    rcap2a.font.name = "Times New Roman"
    rcap2a.font.size = Pt(10.5)
    rcap2a.font.bold = True'''

assert old_uc in text, "old_uc not found!"
assert old_dfd in text, "old_dfd not found!"

text = text.replace(old_uc, new_uc)
text = text.replace(old_dfd, new_dfd)

with open(r"d:\surplus-food\create_docx.py", "w", encoding="utf-8") as f:
    f.write(text)

print("create_docx.py updated with diagrams successfully.")

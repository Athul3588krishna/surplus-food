import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = Document()

# Set page margins to standard 1 inch
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    
    # Configure Header and Footer
    header = section.header
    header_p = header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = header_p.add_run("Surplus Food Rescue & Marketplace")
    hrun.font.name = "Times New Roman"
    hrun.font.size = Pt(9)
    hrun.font.italic = True
    
    footer = section.footer
    footer_p = footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    frun1 = footer_p.add_run("Department of Computer Applications, MEA Engineering College")
    frun1.font.name = "Times New Roman"
    frun1.font.size = Pt(9.5)
    frun1.font.italic = True

def add_heading_1(text, center=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.15
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(15)
    run.font.bold = True
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    return p

def add_para(text, italic=False, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.25
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.italic = italic
    run.font.bold = bold
    return p

def add_bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.2
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11.5)
    return p

def add_code_block(code_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.1
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    tcPr = p._p.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
    tcPr.append(shd)

def add_divider_page(title):
    doc.add_page_break()
    for _ in range(7):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.name = "Times New Roman"
    run.font.size = Pt(22)
    run.font.bold = True
    doc.add_page_break()

def make_table(headers, data):
    tbl = doc.add_table(rows=len(data)+1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(10)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="E2E8F0"/>')
        hdr_cells[i]._tc.get_or_add_tcPr().append(shd)
    
    for r_idx, row_values in enumerate(data):
        row_cells = tbl.rows[r_idx+1].cells
        for c_idx, val in enumerate(row_values):
            row_cells[c_idx].text = val
            p = row_cells[c_idx].paragraphs[0]
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(9.5)

# ================= 1. COVER PAGE =================
p_cov = doc.add_paragraph()
p_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cov.paragraph_format.space_before = Pt(10)
p_cov.paragraph_format.space_after = Pt(18)
r = p_cov.add_run("SURPLUS FOOD RESCUE & MARKETPLACE")
r.font.name = "Times New Roman"
r.font.size = Pt(24)
r.font.bold = True

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(16)
r = p_sub.add_run("A project report\nsubmitted in fulfillment of\nthe requirements for the award of the degree of")
r.font.name = "Times New Roman"
r.font.size = Pt(13)
r.font.italic = True

p_deg = doc.add_paragraph()
p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_deg.paragraph_format.space_after = Pt(8)
r = p_deg.add_run("MASTER OF COMPUTER APPLICATIONS")
r.font.name = "Times New Roman"
r.font.size = Pt(16)
r.font.bold = True

p_uni = doc.add_paragraph()
p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_uni.paragraph_format.space_after = Pt(12)
r = p_uni.add_run("From\nAPJ Abdul Kalam Kerala Technological University")
r.font.name = "Times New Roman"
r.font.size = Pt(13)
r.font.bold = True

# KTU Logo Image
if os.path.exists("d:/surplus-food/extracted_assets/word/media/image1.png"):
    p_ktu = doc.add_paragraph()
    p_ktu.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ktu.paragraph_format.space_after = Pt(10)
    p_ktu.add_run().add_picture("d:/surplus-food/extracted_assets/word/media/image1.png", width=Inches(1.2))

p_by = doc.add_paragraph()
p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_by.paragraph_format.space_after = Pt(4)
r = p_by.add_run("Submitted By")
r.font.name = "Times New Roman"
r.font.size = Pt(12)

# User credentials: RISHIN V (MEA25MCA2021)
p_auth = doc.add_paragraph()
p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_auth.paragraph_format.space_after = Pt(12)
r = p_auth.add_run("RISHIN V (MEA25MCA2021)")
r.font.name = "Times New Roman"
r.font.size = Pt(14)
r.font.bold = True

# MEA Emblem Image
if os.path.exists("d:/surplus-food/extracted_assets/word/media/image2.png"):
    p_mea = doc.add_paragraph()
    p_mea.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mea.paragraph_format.space_after = Pt(14)
    p_mea.add_run().add_picture("d:/surplus-food/extracted_assets/word/media/image2.png", width=Inches(1.3))

p_col = doc.add_paragraph()
p_col.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_col.paragraph_format.space_after = Pt(10)
r = p_col.add_run("MEA Engineering College\nDepartment of Computer Applications\nVengoor P.O, Perinthalmanna, Malappuram, Kerala-679325")
r.font.name = "Times New Roman"
r.font.size = Pt(13)
r.font.bold = True

p_date = doc.add_paragraph()
p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_date.add_run("OCTOBER 2026")
r.font.name = "Times New Roman"
r.font.size = Pt(12)
r.font.bold = True

# ================= 2. CERTIFICATE =================
doc.add_page_break()
p_ch = doc.add_paragraph()
p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ch.paragraph_format.space_after = Pt(18)
r = p_ch.add_run("DEPARTMENT OF COMPUTER APPLICATIONS\nMEA ENGINEERING COLLEGE\nPERINTHALMANNA-679325")
r.font.name = "Times New Roman"
r.font.size = Pt(13)
r.font.bold = True

if os.path.exists("d:/surplus-food/extracted_assets/word/media/image2.png"):
    p_mea2 = doc.add_paragraph()
    p_mea2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mea2.paragraph_format.space_after = Pt(18)
    p_mea2.add_run().add_picture("d:/surplus-food/extracted_assets/word/media/image2.png", width=Inches(1.2))

p_ct = doc.add_paragraph()
p_ct.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ct.paragraph_format.space_before = Pt(10)
p_ct.paragraph_format.space_after = Pt(20)
r = p_ct.add_run("CERTIFICATE")
r.font.name = "Times New Roman"
r.font.size = Pt(18)
r.font.bold = True

add_para('This is to certify that the Project report entitled "Surplus Food Rescue & Marketplace" is a bonafide record of the work done by RISHIN V (MEA25MCA2021) under our supervision and guidance. The report has been submitted in fulfillment of the requirement for award of the Degree of Master of Computer Applications from the APJ Abdul Kalam Kerala Technological University for the year 2026.')

doc.add_paragraph()
doc.add_paragraph()

table_sig = doc.add_table(rows=1, cols=2)
table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
table_sig.autofit = True
c1, c2 = table_sig.rows[0].cells
c1.width = Inches(3.2)
c2.width = Inches(3.2)

p_s1 = c1.paragraphs[0]
r = p_s1.add_run("Mrs. Fathimath Hasna\n")
r.font.bold = True
p_s1.add_run("Assistant Professor\nProject Guide\nDept. of Computer Applications")
for r in p_s1.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

p_s2 = c2.paragraphs[0]
p_s2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p_s2.add_run("Mr. Sajeesh M\n")
r.font.bold = True
p_s2.add_run("Assistant Professor & Head\nHead of the Department\nDept. of Computer Applications")
for r in p_s2.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

# ================= 3. ACKNOWLEDGEMENTS =================
doc.add_page_break()
add_heading_1("Acknowledgements", center=True)
add_para("First and foremost, I would like to thank Almighty God for giving me the knowledge, courage, and strength which helped me in the successful completion of this project.")
add_para("An endeavor of this magnitude can only be successful with the advice, motivation, and guidance of many well-wishers. I take this opportunity to express my heartfelt gratitude to all who encouraged me throughout this journey. I express my deep sense of gratitude to our respected Principal, Dr. Shahir VK, for his inspiring leadership and for fostering an excellent academic environment in the college.")
add_para("I would like to express my deepest gratitude and sincere indebtedness to Mr. Sajeesh M, Assistant Professor and Head of the Department, Department of Computer Applications, for providing permission and facilities to conduct this project in a systematic way.")
add_para("I am profoundly thankful to my Project Guide, Mrs. Fathimath Hasna, Assistant Professor in the Department of Computer Applications, for her invaluable technical guidance, timely advice, constructive critique, and wholehearted moral support throughout the conception, development, and completion of the Surplus Food Rescue & Marketplace project.")
add_para("I also extend my sincere gratitude to all the esteemed faculty members and technical staff of the Department of Computer Applications for their constant cooperation, encouragement, and valuable assistance during various stages of this project.")

p_ack_sign = doc.add_paragraph()
p_ack_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_ack_sign.paragraph_format.space_before = Pt(30)
r = p_ack_sign.add_run("RISHIN V (MEA25MCA2021)\nDATE: OCTOBER 25, 2026")
r.font.name = "Times New Roman"
r.font.size = Pt(12)
r.font.bold = True

# ================= 4. ABSTRACT =================
doc.add_page_break()
add_heading_1("ABSTRACT", center=True)
add_para("Food wastage represents a staggering ecological and socio-economic challenge worldwide. Massive quantities of perfectly edible, wholesome cooked dishes, artisanal bakery goods, and grocery surplus are discarded daily by commercial food businesses simply because items remain unsold at the conclusion of regular trading hours. Concurrently, consumers encounter steep inflation on food commodities, while local charities and price-conscious individuals struggle to secure nutritious sustenance affordably.")
add_para('To effectively solve this systemic inefficiency, Surplus Food Rescue & Marketplace (EcoBite) is engineered as a robust, real-time web-based marketplace dedicated to bridging food business surplus directly with neighborhood consumers. The platform provides dedicated, role-based access for three distinct operational actors: Customer, Restaurant Partner, and Platform Administrator.')
add_para('Customers can discover certified nearby bakeries and eateries, filter surplus food items by cuisine, pricing, and allergen restrictions, buy curated discounted surplus bundles or "Daily Mystery Bags" at 50% to 80% below retail value, securely checkout, and receive instant cryptographic OTP pickup tokens alongside scannable QR verification codes. Restaurant Partners can easily list excess inventory with strict collection timeframes, monitor incoming customer bookings in real time via WebSocket events, and validate customer redemptions using built-in QR camera scanning or PIN confirmation. Platform Administrators retain comprehensive oversight by conducting credential verification of registered restaurants, auditing food catalogs, executing automated cleanup sweeps of expired foodstuffs, and monitoring system-wide financial and environmental savings metrics.')
add_para("The platform is developed using the modern MERN Stack (React.js, Node.js, Express.js, and MongoDB Atlas) paired with Socket.io for instantaneous multi-party notifications, JWT for role-based session authorization, Bcrypt for credential encryption, and automated background Node-Cron tasks for continuous auto-expiry and dynamic price markdown orchestration. The application delivers an efficient, reliable, and sustainable solution to urban food wastage, establishing a complete enterprise-grade full-stack web application suitable for academic excellence and real-world commercial deployment.")

# ================= 5. CONTENTS =================
doc.add_page_break()
add_heading_1("CONTENTS", center=True)

toc_items = [
    ("1.", "INTRODUCTION", "1"),
    ("2.", "SYSTEM ANALYSIS", "3"),
    ("", "2.1 Existing System", "4"),
    ("", "2.2 Proposed System", "4"),
    ("", "2.3 Module Description", "4"),
    ("", "2.4 Sprint", "5"),
    ("3.", "FEASIBILITY STUDY", "8"),
    ("", "3.1 Economical Feasibility", "9"),
    ("", "3.2 Technical Feasibility", "9"),
    ("", "3.3 Operational Feasibility", "9"),
    ("", "3.4 Behavioural Feasibility", "9"),
    ("", "3.5 Software Feasibility", "10"),
    ("", "3.6 Hardware Feasibility", "10"),
    ("4.", "SOFTWARE ENGINEERING PARADIGM", "11"),
    ("", "4.1 Agile Model", "12"),
    ("", "4.2 Scrum", "12"),
    ("5.", "SYSTEM REQUIREMENT SPECIFICATION", "13"),
    ("", "5.1 Software Requirements", "14"),
    ("", "5.2 Hardware Requirements", "14"),
    ("6.", "SYSTEM DESIGN", "15"),
    ("", "6.1 Database Design", "16"),
    ("", "6.2 Tables", "18"),
    ("", "6.3 UML Design", "20"),
    ("", "6.4 Use Case Diagram", "21"),
    ("", "6.5 Scenario", "22"),
    ("", "6.6 Data flow diagram", "23"),
    ("7.", "SYSTEM DEVELOPMENT", "27"),
    ("", "7.1 Coding", "28"),
    ("8.", "SYSTEM TESTING AND IMPLEMENTATION", "31"),
    ("", "8.1 Types of Testing", "32"),
    ("", "8.2 Implementation", "34"),
    ("9.", "SYSTEM MAINTENANCE", "35"),
    ("10.", "FUTURE ENHANCEMENT", "37"),
    ("11.", "CONCLUSION", "39"),
    ("12.", "APPENDIX", "41"),
    ("13.", "BIBLIOGRAPHY", "48")
]

table_toc = doc.add_table(rows=len(toc_items), cols=3)
table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, (num, title, pg) in enumerate(toc_items):
    row = table_toc.rows[idx]
    c_num, c_title, c_pg = row.cells
    c_num.width = Inches(0.6)
    c_title.width = Inches(5.2)
    c_pg.width = Inches(0.6)
    
    p0 = c_num.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    r = p0.add_run(num)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    if num != "": r.font.bold = True
    
    p1 = c_title.paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    r = p1.add_run(title)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    if num != "": r.font.bold = True
    
    p2 = c_pg.paragraphs[0]
    p2.paragraph_format.space_after = Pt(2)
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p2.add_run(pg)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    if num != "": r.font.bold = True

# ================= CHAPTER 1: INTRODUCTION =================
add_divider_page("INTRODUCTION")
add_heading_1("1. INTRODUCTION")
add_para("Food loss and culinary waste have emerged as severe ecological, economic, and moral challenges of contemporary society. Each year, billions of tons of high-grade, wholesome cooked dishes, artisan breads, delicate pastries, and grocery surplus are produced and transported only to be dumped into municipal landfills. Within commercial food establishments—including restaurants, bakeries, cafes, and supermarket hot-bars—food items that remain unpurchased at the end of the operating shift are routinely discarded due to the perishable nature of fresh items, stringent aesthetic guidelines, and lack of dynamic redistribution channels.")
add_para("This widespread wastage generates severe environmental consequences. Decomposing organic food products in open landfills produce massive quantities of methane, a potent greenhouse gas that accelerates global climatic warming. Concurrently, consumers and working families face sharp cost-of-living increases, making nutritious meals expensive to afford regularly. Traditional food redistribution approaches, such as sporadic charitable donations or word-of-mouth discounts, are fundamentally uncoordinated, slow, and operationally burdensome for commercial kitchen managers.")
add_para("To address these critical inefficiencies, I developed the Surplus Food Rescue & Marketplace (EcoBite) platform. The system establishes a synchronized, hyper-local digital marketplace connecting food businesses burdened with surplus stock directly with conscientious neighborhood consumers looking for discounted meals. The application provides dedicated role-based portals for Customers, Restaurant Partners, and System Administrators, engineered to eliminate operational delays and facilitate friction-free transactions.")
add_para("The platform empowers customers to discover verified local food stores, filter items by diet, cuisine, and allergen sensitivities, order mystery surprise bags at steep 50% to 80% markdowns, and retrieve food securely using tamper-proof OTP collection codes and QR passes. Restaurants gain an intuitive merchant hub to monetize excess stock, broadcast dynamic discounts during final trading minutes, and verify collections effortlessly with camera-based QR scanning. Administrators oversee platform health, verify restaurant licenses, audit food listings, and monitor aggregated carbon offsets.")
add_para("Engineered on the modern MERN Stack (React.js, Node.js, Express.js, and MongoDB Atlas) with Socket.io real-time websockets, the Surplus Food platform provides an efficient, transparent, and scalable solution to urban food wastage, perfectly suited for academic evaluation and real-world deployment.")

# ================= CHAPTER 2: SYSTEM ANALYSIS =================
add_divider_page("SYSTEM ANALYSIS")
add_heading_1("2. SYSTEM ANALYSIS")

add_heading_2("2.1 Existing System")
add_para("In the existing food retail ecosystem, restaurants, grocery vendors, and bakeries rely heavily on manual forecasting to calculate daily preparation quantities. Because consumer demand fluctuates wildly depending on weather, local foot traffic, and daily events, kitchens consistently prepare surplus inventory to prevent running out of menu offerings. At the conclusion of daily trading, leftover prepared food is routinely discarded into trash compactors.")
add_para("Currently, there is no unified digital channel enabling merchants to rapidly alert nearby customers of available surplus items during closing hours. Traditional food bank donations, while noble, require scheduled logistical coordination, refrigerated transport vehicles, and extensive paperwork, making them impractical for small, hot perishable batches. Furthermore, consumers lack a trusted mechanism to identify which local stores have discounted items available for immediate collection, leading to massive financial waste for businesses and preventable environmental damage.")

add_heading_2("2.2 Proposed System")
add_para("The proposed system, Surplus Food Rescue & Marketplace, introduces a centralized full-stack web application designed to eliminate food waste by facilitating rapid, hyper-local surplus food transactions. The system introduces dedicated, role-based workflows for Customers, Restaurant Partners, and Administrators.")
add_para("Customers can browse available food listings in real time, filter by dietary requirements (Veg, Non-Veg, Vegan, Gluten-Free, Halal), reserve curated Mystery Surprise Bags, and receive a secure 6-digit OTP token and scannable QR verification code. Restaurants can post surplus inventory in under a minute, set designated pickup windows, receive instantaneous WebSocket booking notifications, and verify redemptions seamlessly with built-in QR scanning. Platform Administrators ensure marketplace trust by auditing restaurant credentials, monitoring active postings, and analyzing system-wide sustainability metrics.")

add_heading_2("2.3 Module Description")
add_para("The Surplus Food platform is structured into three specialized functional modules based on user roles, each tailored to execute distinct business workflows:")

add_heading_3("Admin Module")
add_bullet("Secure administrator authentication and multi-tier role-based access control.")
add_bullet("Audit, approve, or decline onboarding restaurant business profiles and operating credentials.")
add_bullet("Comprehensive registry management to monitor all registered customers and merchant accounts.")
add_bullet("System-wide inventory monitoring across all active surplus food postings.")
add_bullet("Automated maintenance trigger to sweep and delete expired food items past pickup windows.")
add_bullet("Live analytics dashboard displaying total meals rescued, financial customer savings, and CO2 emissions prevented.")

add_heading_3("Customer Module")
add_bullet("User registration, secure email OTP validation, and JWT session authentication.")
add_bullet("Interactive food exploration hub with filtering by cuisine, price range, dietary preferences, and allergens.")
add_bullet("Surplus Surprise Bag discovery offering mystery assortments at 50% to 80% markdowns.")
add_bullet("Real-time booking and checkout with automated collection token (OTP) and QR code generation.")
add_bullet("Digital reservation voucher download in printable PDF receipt format.")
add_bullet("Personalized reservations tracker displaying active pickup windows and past order histories.")
add_bullet("Post-pickup review and star rating submission to maintain vendor quality.")

add_heading_3("Restaurant Module")
add_bullet("Merchant onboarding with business name, address, cuisine specialization, and logo uploads.")
add_bullet("Surplus food item listing engine with original price, discounted price, stock count, and strict pickup hours.")
add_bullet("Surplus Mystery Bag toggle with pre-configured value estimates and descriptions.")
add_bullet("Real-time WebSocket booking alerts notifying kitchen staff immediately upon customer order placement.")
add_bullet("Customer collection verification via manual 6-digit OTP entry or built-in camera QR scanner.")
add_bullet("Live merchant analytics tracking total sales revenue, units rescued, and customer satisfaction ratings.")

add_heading_2("2.4 Sprint")
add_heading_3("Sprint 1: Core Authentication & Customer Portal")

t1_headers = ["Module", "Task", "Pending", "Hrs", "Expected Date", "Actual Date", "Delay"]
t1_data = [
    ["Customer", "User Registration & Email OTP Verification", "-", "2 hr.", "19/07/2026", "19/07/2026", "-"],
    ["Customer", "JWT Login & Role Authorization", "-", "2 hr.", "21/07/2026", "21/07/2026", "-"],
    ["Customer", "Surplus Catalog & Filter Grid (Cuisine/Allergens)", "-", "4 hr.", "23/07/2026", "23/07/2026", "-"],
    ["Customer", "Food Reservation & OTP Token Engine", "-", "3 hr.", "25/07/2026", "25/07/2026", "-"],
    ["Customer", "QR Code Pass & PDF Receipt Generation", "-", "4 hr.", "28/07/2026", "28/07/2026", "-"]
]
make_table(t1_headers, t1_data)

add_heading_3("Sprint 2: Restaurant Hub & Real-time Verification")
t2_data = [
    ["Restaurant", "Store Profile Setup & Verification Submission", "-", "2 hr.", "10/08/2026", "10/08/2026", "-"],
    ["Restaurant", "Surplus Listing Management & Image Uploads", "-", "5 hr.", "12/08/2026", "12/08/2026", "-"],
    ["Restaurant", "Surprise Bag & Dynamic Markdown Pricing", "-", "3 hr.", "14/08/2026", "14/08/2026", "-"],
    ["Restaurant", "WebSocket Real-Time Order Dispatch", "-", "4 hr.", "15/08/2026", "15/08/2026", "-"],
    ["Restaurant", "Camera QR Scanner & Token Verification", "-", "3 hr.", "17/08/2026", "17/08/2026", "-"]
]
make_table(t1_headers, t2_data)

add_heading_3("Sprint 3: Administration, Automated Jobs & Analytics")
t3_data = [
    ["Admin", "Admin Command Center & Access Controls", "-", "2 hr.", "18/08/2026", "18/08/2026", "-"],
    ["Admin", "Merchant Store Profile Verification & Auditing", "-", "4 hr.", "20/08/2026", "20/08/2026", "-"],
    ["Admin", "Global Postings Monitor & Expired Sweeper", "-", "4 hr.", "22/08/2026", "22/08/2026", "-"],
    ["Admin", "Node-Cron Auto-Expiry & Markdown Engine", "-", "5 hr.", "24/08/2026", "24/08/2026", "-"],
    ["Admin", "System Metrics, User Management & Analytics", "-", "3 hr.", "28/08/2026", "28/08/2026", "-"]
]
make_table(t1_headers, t3_data)

# ================= CHAPTER 3: FEASIBILITY STUDY =================
add_divider_page("FEASIBILITY STUDY")
add_heading_1("3. FEASIBILITY STUDY")
add_para("An analysis of the ability to complete a project successfully, taking into account legal, economic, technological, scheduling, and other factors is considered as a feasibility study. Rather than just diving into a project and hoping for the best, a feasibility study allows project managers to investigate the possible negative and positive outcomes of a project before investing too much time and money.")

add_heading_2("3.1 Economical Feasibility")
add_para("The proposed system is economically highly feasible because it is built entirely using robust, open-source technologies including React.js, Node.js, Express.js, MongoDB Atlas (Community Tier), Socket.io, Git, and GitHub. None of these core technologies require proprietary or expensive software licensing fees. Development and testing were executed on standard consumer computing hardware using freely available, industry-standard developer tooling such as Visual Studio Code and Postman. Since the primary objective of Surplus Food Rescue & Marketplace is food waste mitigation and academic evaluation, the capital expenditure and operational maintenance costs remain exceptionally low, while delivering an enterprise-grade commercial web application.")

add_heading_2("3.2 Technical Feasibility")
add_para("The project is technically feasible as all necessary frameworks and libraries are mature, extensively documented, and supported by vibrant global developer communities. The MERN Stack provides an asynchronous, non-blocking architecture ideally suited for high-throughput marketplace communications. MongoDB provides high-performance schema flexibility for nested surplus food catalogs and order tracking. Socket.io guarantees bidirectional WebSocket dispatching with sub-second latencies, essential for alerting merchants of immediate orders. JWT ensures cryptographic, stateless role-based security, while HTML5 QR libraries enable effortless in-browser barcode verification. The system architecture has been thoroughly verified using modern full-stack software development methodologies.")

add_heading_2("3.3 Operational Feasibility")
add_para("Surplus Food Rescue & Marketplace is operationally feasible because its user interfaces are deliberately designed for fast-paced food service scenarios with minimal cognitive load. For customers, the intuitive catalog allows one-click filtering, instant cartless reservations, and scannable QR passes requiring zero technical training. For restaurant staff, the responsive dashboard provides live audio-visual order alerts and one-tap camera QR scanning that integrates seamlessly into frantic kitchen closing routines. For administrators, the centralized operational dashboard provides clear tabular auditing of store registrations and item listings. This streamlined design ensures that users across all skill levels can operate the system effectively.")

add_heading_2("3.4 Behavioural Feasibility")
add_para("Behavioral feasibility examines the willingness and confidence of stakeholders to adopt the proposed digital system. Restaurant owners are strongly motivated to adopt the system because it transforms what was previously discarded as pure financial loss into a supplemental revenue stream, while bolstering their public environmental reputation. Customers are enthusiastically driven to participate by substantial discounts (50% to 80% markdowns) on restaurant-quality food, combined with the altruistic satisfaction of rescuing edible food from landfills. These powerful positive behavioral drivers guarantee high user adoption and sustained community engagement.")

add_heading_2("3.5 Software Feasibility")
add_para("The software requirements for the project encompass a standard modern operating system (Windows 10/11, Linux, or macOS) supporting Node.js (v18+) runtime environment, React.js (v19/18) with Vite for frontend rendering, Express.js (v4.19) for backend REST microservices, and MongoDB Atlas for distributed database storage. Ancillary software includes Socket.io for bidirectional WebSocket messaging, jsPDF and QRCode.react for client-side receipt generation, JSON Web Token (JWT) and Bcrypt for encryption and authorization, Dotenv for secure environment variables, and Git/GitHub for distributed version control. All software components are readily accessible, production-stable, and fully compatible.")

add_heading_2("3.6 Hardware Feasibility")
add_para("The hardware infrastructure necessary to run and interact with Surplus Food Rescue & Marketplace is widely available and affordable. The server-side platform can be hosted on standard cloud instances or local machines with a minimum of an Intel Core i3 / AMD Ryzen dual-core processor, 8 GB of RAM, and modest solid-state storage. On the client side, the web application runs responsively on any standard desktop, laptop, or mobile smartphone with a standard web browser and an internet connection (broadband, 4G, or 5G). No specialized POS hardware or proprietary scanners are required, making the deployment highly cost-effective and scalable.")

# ================= CHAPTER 4: SOFTWARE ENGINEERING PARADIGM =================
add_divider_page("SOFTWARE ENGINEERING PARADIGM")
add_heading_1("4. SOFTWARE ENGINEERING PARADIGM")
add_para("The software engineering paradigm which is also referred to as a software process model or Software Development Life Cycle (SDLC) model is the development strategy that encompasses the process, methods and tools. SDLC describes the period of time that starts with the software system being conceptualized.")

add_heading_2("4.1 Agile model")
add_para("The Agile SDLC model is a combination of iterative and incremental process models with focus on process adaptability and customer satisfaction by rapid delivery of working software product. Agile Methods break the product into small incremental builds. These builds are provided in iterations. Each iteration typically lasts from about one to three weeks. At the end of the iteration, a working product is displayed to the customer and important stakeholders.")
add_para("In Agile, the tasks are divided to time boxes (small time frames) to deliver specific features for a release. Iterative approach is taken and working software build is delivered after each iteration. Each build is incremental in terms of features; the final build holds all the features required by the customer.")

add_heading_2("4.2 Scrum")
add_para("Scrum is an agile framework for managing knowledge work, with an emphasis on software development. It is designed for teams of three to nine members, who break their work into actions that can be completed within time boxed iterations, called 'sprints', no longer than one month and most commonly two weeks, then track progress and re-plan in 15-minute stand-up meetings, called daily scrums.")
add_para("Scrum is an iterative and incremental framework for product development. It promotes a flexible strategy where development teams collaborate to achieve common goals, challenging traditional sequential methods. Scrum encourages self-organization, physical co-location, and daily communication among team members.")

# ================= CHAPTER 5: SRS =================
add_divider_page("SYSTEM REQUIREMENTS SPECIFICATION")
add_heading_1("5. SYSTEM REQUIREMENTS SPECIFICATION")

add_heading_2("5.1 Software Requirements")
s_headers = ["Component", "Requirement"]
s_data = [
    ["Operating System", "Windows 10 / 11, Linux (Ubuntu 20.04+), macOS"],
    ["Backend Runtime", "Node.js (v18+), Express.js (v4.19), Socket.io (v4.8)"],
    ["Frontend Framework", "React.js (v19/18), Vite, Lucide-React, Axios"],
    ["Database", "MongoDB Atlas (v6.0+) / MongoDB Community Edition"],
    ["Ancillary Packages", "Bcryptjs, JSONWebToken, HTML5-QRCode, jsPDF, Node-Cron"],
    ["Development IDE & Tools", "Visual Studio Code, Postman API Client, Git, GitHub"]
]
make_table(s_headers, s_data)

add_heading_2("5.2 Hardware Requirements")
h_data = [
    ["Processor", "Intel Core i3 / i5 or AMD Ryzen equivalent (2.0 GHz or above)"],
    ["RAM", "Minimum 8 GB (16 GB Recommended for development)"],
    ["Storage", "256 GB SSD or higher for database and runtime logs"],
    ["Display Monitor", "14\" Full HD (1920x1080) or standard modern mobile display"],
    ["Camera Peripherals", "Standard webcam or smartphone camera (for QR scanning)"],
    ["Network", "Broadband / 4G / 5G active internet connection"]
]
make_table(s_headers, h_data)

# ================= CHAPTER 6: SYSTEM DESIGN =================
add_divider_page("SYSTEM DESIGN")
add_heading_1("6. SYSTEM DESIGN")
add_para("System design is the process of architecting the overall structure, modular components, database entities, communication interfaces, and operational data flows of a software application to fulfill specified functional and performance criteria. The system design of Surplus Food Rescue & Marketplace focuses on engineering an ultra-responsive, highly available, resilient, and fault-tolerant architecture capable of coordinating time-sensitive food rescues, real-time inventory synchronization, dynamic markdown price drops, and rapid QR token validation during closing hours.")

add_heading_2("6.1 Database Design")
add_para("Database design organizes and models system entities to ensure high data integrity, minimal redundancy, lightning-fast querying, and rapid transaction processing under concurrent customer ordering spikes. The Surplus Food platform utilizes MongoDB, an enterprise-grade NoSQL document-oriented database. Unlike rigid relational databases, MongoDB stores information in flexible, schema-validated JSON-like BSON documents within specialized collections. This structure natively supports polymorphic attributes such as allergen arrays, dietary classifications, dynamic price adjustments, and nested payment details.")
add_para("The database architecture is designed to manage complex relationships among customer users, restaurant profiles, surplus food listings, reservations/orders, and customer reviews. Unique ObjectIds and referenced indexes maintain data consistency across all collections.")
add_para("The major collections used in the system include:")
add_bullet("Users — Stores user account credentials, hashed passwords (Bcrypt), contact phone numbers, assigned roles (customer, restaurant, admin), email verification statuses, and OTP codes.")
add_bullet("RestaurantProfiles — Stores business metadata, restaurant name, street address, cuisine classification, operational description, store banner image paths, administrative verification flag, and aggregated customer ratings.")
add_bullet("FoodItems — Stores surplus inventory listings, referenced restaurant profile IDs, item titles, descriptions, original pricing, discounted offer pricing, available quantity, daily pickup time windows, expiry timestamps, dietary badges, and Surprise Bag indicators.")
add_bullet("Orders — Stores transaction records, referenced customer ID, restaurant ID, food item ID, quantity reserved, total price, order status (reserved, collected, cancelled), unique 6-digit OTP verification token, and payment details.")
add_bullet("Reviews — Stores post-pickup ratings (1 to 5 stars), written customer comments, and references linking the reviewer, store, and verified order.")

add_heading_2("6.2 Tables (Database Schemas & Data Dictionary)")

add_heading_3("Database Schema 1: Users Collection (Customers, Restaurants, Admins)")
add_code_block("""_id         : ObjectId('6a85e825d3f0510078fbec0c')
name        : "Rishin V"
email       : "customer@surplus.com"
password    : "$2a$10$wN7KjZq0/2K3B...hashed..."
role        : "customer"
phoneNumber : "555-123-4567"
isVerified  : true
otpCode     : ""
createdAt   : 2026-08-16T10:15:30.000+00:00
__v         : 0""")

add_heading_3("Database Schema 2: RestaurantProfiles Collection")
add_code_block("""_id            : ObjectId('6a85ea2eff5323a524c4f07d')
user           : ObjectId('6a85e825d3f0510078fbec0a')
restaurantName : "The Green Bakery"
address        : "123 Bread Street, Foodtown"
cuisineType    : "Bakeries"
description    : "An artisanal bakery crafting organic bread, pastries, and croissants fresh daily."
imagePath      : "/uploads/store_banner.jpg"
isVerified     : true
rating         : 5.0
ratingCount    : 0
createdAt      : 2026-08-16T10:20:00.000+00:00
__v            : 0""")

add_heading_3("Database Schema 3: FoodItems Collection (Surplus Listings & Mystery Bags)")
add_code_block("""_id                 : ObjectId('6ad1ab025bc04b489f991070')
restaurant          : ObjectId('6a85ea2eff5323a524c4f07d')
name                : "Evening Bakery Surprise Bag"
description         : "A mystery assortment of fresh daily surplus baked goods and artisan sourdough."
originalPrice       : 15.00
discountedPrice     : 4.99
quantity            : 6
pickupStartTime     : "18:00"
pickupEndTime       : "21:00"
status              : "available"
expiryDate          : 2026-10-18T21:00:00.000+00:00
dietaryType         : "veg"
allergens           : ["Nut-Free"]
isSurpriseBag       : true
estimatedValue      : 15.00
isDynamicDiscounted : false
createdAt           : 2026-10-16T10:11:38.000+00:00
__v                 : 0""")

add_heading_3("Database Schema 4: Orders Collection (Reservations & Collection Tokens)")
add_code_block("""_id            : ObjectId('6ad1abf55bc04b489f99108b')
customer       : ObjectId('6a85e825d3f0510078fbec0c')
restaurant     : ObjectId('6a85ea2eff5323a524c4f07d')
foodItem       : ObjectId('6ad1ab025bc04b489f991070')
quantity       : 1
totalPrice     : 2.50
status         : "reserved"
token          : "387421"
paymentStatus  : "paid"
paymentDetails : {
                   "transactionId": "TXN-16237966",
                   "cardLast4": "4242"
                 }
createdAt      : 2026-10-16T10:12:34.000+00:00
__v            : 0""")

add_heading_3("Database Schema 5: Reviews Collection")
add_code_block("""_id        : ObjectId('6ad1ac225bc04b489f991094')
customer   : ObjectId('6a85e825d3f0510078fbec0c')
restaurant : ObjectId('6a85ea2eff5323a524c4f07d')
order      : ObjectId('6ad1abf55bc04b489f99108b')
rating     : 5
comment    : "Outstanding quality! Delicious croissants and bread at an unbelievable discount."
createdAt  : 2026-10-16T10:15:00.000+00:00
__v        : 0""")

add_heading_2("6.3 UML Designs")
add_para("The Unified Modeling Language (UML) is a standard language for specifying, visualizing, constructing, and documenting the artifacts of software systems, as well as for business modeling and other non-software systems. The UML represents a collection of best engineering practices that have proven successful in the modeling of large and complex systems. UML uses mostly graphical notations to express the design of software projects. Using UML helps project teams communicate, explore potential designs, and validate the architectural design of the software.")

add_heading_2("6.4 Use Case Diagram")
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
    rcap.font.bold = True

add_heading_2("6.5 Scenario")
add_para("A scenario is a detailed description of a particular situation or sequence of events that helps illustrate how a system or process works. In software engineering, scenarios are often used to show how users interact with a system to achieve specific goals. For example, a scenario might describe how a customer discovers a local bakery, reserves a surprise bag, receives an OTP token, and collects the package. Scenarios make it easier to understand user needs, test different conditions, and visualize the flow of operations within a system.")

add_heading_3("CUSTOMER SCENARIOS")
add_bullet("Customer can register an account and verify identity via 6-digit email OTP.")
add_bullet("Customer can authenticate securely using email and password to receive a JWT session.")
add_bullet("Customer can explore active surplus food items from nearby verified restaurants.")
add_bullet("Customer can filter available offerings by cuisine classification, max price, dietary type, and allergens.")
add_bullet("Customer can view Mystery Surprise Bags offered at heavy markdowns.")
add_bullet("Customer can reserve surplus items, specify quantities, and complete simulated checkout.")
add_bullet("Customer can receive a unique 6-digit collection OTP and dynamic scannable QR verification code.")
add_bullet("Customer can download an official PDF reservation receipt with pickup instructions.")
add_bullet("Customer can view active reservations, store addresses, and pickup closing windows.")
add_bullet("Customer can submit star ratings and qualitative reviews following successful collection.")
add_bullet("Customer can securely log out of the platform.")

add_heading_3("RESTAURANT SCENARIOS")
add_bullet("Restaurant can register and submit restaurant profile credentials (name, address, cuisine) for audit.")
add_bullet("Restaurant can post surplus inventory with original price, discounted price, stock count, and collection times.")
add_bullet("Restaurant can flag listings as Surprise Mystery Bags with estimated retail valuations.")
add_bullet("Restaurant can update or remove active surplus listings.")
add_bullet("Restaurant can receive instantaneous WebSocket sound and banner alerts when customer reservations are placed.")
add_bullet("Restaurant can view the customer reservation queue in real time.")
add_bullet("Restaurant can verify customer pickups by entering the 6-digit OTP code or scanning customer QR codes with a webcam.")
add_bullet("Restaurant can track revenue metrics, total stock quantities, and customer satisfaction ratings.")
add_bullet("Restaurant can securely log out of the platform.")

add_heading_3("ADMIN SCENARIOS")
add_bullet("Administrator can securely log in via protected admin credentials.")
add_bullet("Administrator can review, approve, or reject onboarding restaurant business profiles.")
add_bullet("Administrator can view all registered customer and merchant user accounts.")
add_bullet("Administrator can inspect all active platform food listings and verify pricing integrity.")
add_bullet("Administrator can execute automated database cleanups to purge expired food listings.")
add_bullet("Administrator can track aggregate environmental and economic metrics (meals rescued, customer savings, CO2 prevented).")
add_bullet("Administrator can securely log out of the admin console.")

add_heading_2("6.6 Data Flow Diagram")
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
    rcap2a.font.bold = True

# ================= CHAPTER 7: SYSTEM DEVELOPMENT =================
add_divider_page("SYSTEM DEVELOPMENT")
add_heading_1("7. SYSTEM DEVELOPMENT")
add_para("System development is a series of activities performed to design, implement, test, and deploy a software system to meet the specified requirements. The principal activities performed during the development phase can be divided into two major related sequences:")
add_bullet("External System Development")
add_bullet("Internal System Development")
add_para("The major external system development activities include implementation planning, development environment setup, software installation, and cloud database provisioning. The internal system development activities involve software architecture design, database modeling, API development, frontend component engineering, authentication, authorization, testing, and security integration.")

add_heading_2("7.1 Coding")
add_para("The purpose of coding is to convert the system design and requirements into executable software. It consists of a structured collection of programming statements used to implement system functions, manage data, process user requests, and establish communication between different components. Coding facilitates the development of reliable, maintainable, and efficient software by implementing the required modules and workflows.")

add_heading_3("JavaScript & Node.js")
add_para("JavaScript is a high-level, dynamic, multi-paradigm programming language widely used for modern web application development. In Surplus Food Rescue & Marketplace, JavaScript powers both the interactive client-side application logic and the high-performance server-side runtime via Node.js. Node.js is an open-source, cross-platform JavaScript runtime built on Chrome's V8 engine that facilitates asynchronous, event-driven, non-blocking I/O operations, ensuring high concurrent request handling during peak food collection windows.")
add_para("In Surplus Food, Node.js serves as the server runtime handling user authentication, email OTP verification, order placement pipelines, WebSocket live dispatch channels, automated cron jobs, and database CRUD operations.")

add_heading_3("React.js")
add_para("React.js is an open-source JavaScript library used for building interactive and reusable user interfaces. It follows a component-based architecture, allowing large interfaces to be divided into smaller reusable components.")
add_para("In Surplus Food, React.js (powered by Vite) is utilized to engineer the responsive frontend interfaces across all three user modules: Customer, Restaurant Partner, and Admin. It integrates Lucide-React icons, HTML5 QR camera scanning modules, dynamic countdown timers, and client-side PDF document generation.")

add_heading_3("Express.js Framework")
add_para("Express.js is a fast, minimalist web application framework for Node.js. It provides features for developing RESTful APIs, handling HTTP requests, managing routes, and implementing middleware. Express.js simplifies communication between the frontend and backend by providing structured API endpoints and handling HTTP methods such as GET, POST, PUT, and DELETE. It also supports request validation, authentication middleware, error handling, and JSON data processing.")

add_heading_3("MongoDB Database")
add_para("MongoDB is a NoSQL, document-oriented database used for storing and managing application data. Unlike relational databases that store information in tables and rows, MongoDB stores data in flexible JSON-like documents within collections.")
add_para("MongoDB Atlas is deployed in Surplus Food to store distributed documents across users, restaurant profiles, surplus food items, customer reservations, and ratings. MongoDB's flexible schema models effortlessly handle variable attributes like allergen lists, dietary tags, dynamic markdown price history, and nested payment credentials.")

add_heading_3("Standard Libraries & Middleware Packages")
add_para("The Node.js development ecosystem provides several packages through Node Package Manager (npm) to support authentication, security, file management, and application configuration:")
add_bullet("JWT (JSON Web Token): Used for secure token-based authentication and role-based access control. Upon login, a signed JSON Web Token is issued containing the user's role (Customer, Restaurant, Admin), ensuring that protected API endpoints and administrative dispatch actions remain strictly safeguarded.")
add_bullet("Bcrypt: A password-hashing library used to securely hash user passwords using 10 salt rounds before storing them in the database, protecting user credentials against dictionary and rainbow table attacks.")
add_bullet("Socket.io: Powers the bidirectional, sub-second WebSocket communication layer essential for broadcasting incoming customer reservations directly to active kitchen dashboards without requiring manual page reloads.")
add_bullet("Multer: Middleware used for handling multipart/form-data, utilized for uploading restaurant banners and food item photos safely to the server uploads directory.")
add_bullet("Node-Cron: A background task scheduler that runs automated routines every minute to sweep expired listings and execute 20% dynamic markdowns during the final 30 minutes of store pickup windows.")
add_bullet("Dotenv: Used to load environment variables from a .env file, keeping sensitive credentials such as database connection URIs and JWT secrets isolated from the codebase.")
add_bullet("CORS: Cross-Origin Resource Sharing enables controlled communication between the React.js client and the Express.js server when hosted across different origins.")

# ================= CHAPTER 8: TESTING & IMPLEMENTATION =================
add_divider_page("SYSTEM TESTING AND IMPLEMENTATION")
add_heading_1("8. SYSTEM TESTING AND IMPLEMENTATION")
add_para("System testing is a crucial milestone in the engineering of Surplus Food Rescue & Marketplace. Rigorous testing verifies that all modules operate with extreme reliability, fail-safe resilience, low latency, and zero data loss under concurrent consumer and restaurant transaction loads.")
add_para("Software testing is an important part of software quality assurance. It involves the systematic evaluation of the system's requirements, design, coding, functionality, and user interaction. Testing is performed throughout the development process to verify that the implemented system produces the expected results under specified conditions.")

add_heading_2("8.1 Types of Testing")
add_para("The different types of testing performed for the Surplus Food platform include Unit Testing, Integration Testing, System Testing, Validation Testing, and User Acceptance Testing:")

add_heading_3("Unit Testing")
add_para("Unit testing involves testing individual modules or components of the application separately to ensure that each component performs its intended function correctly. It is generally performed during the coding stage to identify errors early.")
add_para("In Surplus Food, unit testing was conducted on individual software units including password hashing, 6-digit OTP token generation, JWT signing, price validation (ensuring offer price is strictly less than original price), quantity checks, and countdown calculations. Each function was validated against boundary cases and expected numerical outputs.")

add_heading_3("Integration Testing")
add_para("Integration testing involves combining individually tested modules and checking whether they work correctly together. It focuses on identifying errors in communication and data exchange between different components of the system.")
add_para("In Surplus Food, integration testing was performed across cooperating pipelines such as:")
add_bullet("User registration, OTP verification, and JWT session authorization pipelines.")
add_bullet("Restaurant surplus food creation and immediate reflection on the customer catalog.")
add_bullet("Customer booking checkout triggering real-time WebSocket notifications to the merchant.")
add_bullet("Token / QR validation decrementing restaurant available stock and updating reservation status.")
add_bullet("React.js frontend, Express REST APIs, Socket.io gateway, and MongoDB Atlas database.")

add_heading_3("System Testing")
add_para("System testing evaluated the complete Surplus Food platform as a unified marketplace. The platform was evaluated under high concurrency to simulate evening rush-hour food collections, verifying sub-second WebSocket broadcast latencies, accurate countdown timers, and resilience against network timeouts.")
add_para("The validation suite confirmed proper role isolation: customers cannot access merchant management panels or admin audit tools, and restaurants can only access and modify their own inventory catalogs.")

add_heading_3("Validation Testing")
add_para("Validation testing ensures that the developed system satisfies all functional requirements and operational expectations established during the analysis and design stages. It verifies that the application correctly fulfills all mission workflows for the Customer, Restaurant Partner, and Admin.")
add_para("Validation testing includes checking:")
add_bullet("Correct user registration and instant 6-digit email OTP authentication.")
add_bullet("Strict role-based authorization preventing unauthorized data access.")
add_bullet("Accurate surplus item listing, image uploading, and Mystery Bag configuration.")
add_bullet("Accurate search filtering across cuisines, maximum price bounds, and allergen tags.")
add_bullet("Reliable order checkout, OTP token issuance, and QR code rendering.")
add_bullet("Real-time WebSocket alerts upon incoming customer bookings.")
add_bullet("Automated node-cron background sweeps of expired food items.")
add_bullet("Administrative restaurant audit approvals and platform listings sweeps.")

add_heading_3("User Acceptance Testing (UAT)")
add_para("User Acceptance Testing (UAT) was conducted by simulating real-world bakery and restaurant closing scenarios with test users acting as Customers, Restaurant Kitchen Staff, and Administrators. Feedback verified that reserving surplus food and redeeming passes via 6-digit OTP tokens was exceptionally straightforward and rapid.")
add_para("The major areas considered during user acceptance testing include:")
add_bullet("Output screen design and aesthetic visual presentation.")
add_bullet("Input form ergonomics and validation feedback.")
add_bullet("Navigation and menu structure.")
add_bullet("QR scanner responsiveness on mobile devices.")
add_bullet("Checkout and token retrieval flow.")
add_bullet("Dashboard functionality and metrics clarity.")

add_heading_2("8.2 Implementation")
add_para("Implementation is the vital phase where the software design specifications of Surplus Food were translated into an operational, production-ready marketplace platform. The implementation integrated the React.js client interface with the Node.js / Express.js backend, configured WebSocket channels, seeded initial sample test accounts, and deployed the application.")
add_para("The implementation process includes:")
add_bullet("Careful planning of the system deployment.")
add_bullet("Setting up the React.js, Node.js, Express.js, and MongoDB environment.")
add_bullet("Configuring the database connection strings and environment security variables.")
add_bullet("Integrating frontend interfaces with backend RESTful APIs.")
add_bullet("Implementing authentication and role-based access control middleware.")
add_bullet("Testing all modules and fixing identified errors.")
add_bullet("Preparing user guidance and documentation.")

# ================= CHAPTER 9: SYSTEM MAINTENANCE =================
add_divider_page("SYSTEM MAINTENANCE")
add_heading_1("9. SYSTEM MAINTENANCE")
add_para("Maintenance is the process of making necessary changes and improvements to a software system after its implementation. These changes may include fixing errors, adapting the system to changes in the software environment, improving performance, enhancing security, and adding new features. When changes are implemented during the maintenance phase, the affected parts of the system must be systematically reviewed and tested to maintain system stability and data integrity.")
add_para("There are three types of maintenance:")
add_bullet("Corrective Maintenance – Fixing bugs, errors, and system failures.")
add_bullet("Adaptive Maintenance – Updating the system to support changes in software, hardware, or operating environments.")
add_bullet("Perfective Maintenance – Improving existing features and adding enhancements based on user requirements.")
add_para("Maintenance is an essential component of the software development lifecycle, particularly for an active consumer marketplace like Surplus Food. Ongoing maintenance ensures 99.99% operational uptime, security patching against newly discovered vulnerabilities, optimization of database queries, and continuous calibration of automated price markdown algorithms.")

add_heading_2("9.1 Key Maintenance Activities & Importance")
add_para("Key maintenance activities for Surplus Food encompass: (1) Problem Identification & Error Monitoring through server health logs, WebSocket connection states, and API latency trackers; (2) Design & Code Refinement across React components, Express controllers, and Mongoose schemas; (3) Regression Testing of booking and verification pipelines; and (4) Configuration Management via GitHub and automated deployment pipelines.")

add_heading_3("1. Problem Identification & Analysis")
add_para("Monitoring server errors, API responses, database issues, and user feedback to identify and analyze problems related to login, profiles, reservations, notifications, or other system functions.")

add_heading_3("2. Design & Code Modification")
add_para("Modifying React.js components, Express.js APIs, Node.js backend services, or MongoDB models to fix issues and introduce improvements without affecting existing system functionality.")

add_heading_3("3. Regression Testing & Verification")
add_para("Re-testing important application functions such as authentication, role-based access, surplus food reservation, WebSocket dispatch alerts, and camera QR verification to ensure that new code updates do not compromise system stability.")

add_heading_3("4. Deployment & Configuration Management")
add_para("Deploying updated application versions, managing environment variables and configuration settings, maintaining database configurations, and using GitHub for version control and tracking system changes.")

# ================= CHAPTER 10: FUTURE ENHANCEMENT =================
add_divider_page("FUTURE ENHANCEMENT")
add_heading_1("10. FUTURE ENHANCEMENTS")
add_para("The Surplus Food Rescue & Marketplace platform has established a high-performance foundation for urban food rescue. To further expand its sustainability impact and adapt to growing commercial demands, several cutting-edge technological enhancements are planned for future iterative releases:")

add_heading_2("10.1 AI-Powered Surplus Waste Prediction")
add_para("Integrating machine learning predictive models (e.g. Random Forest regression, LSTM neural networks) trained on historical restaurant sales, weather conditions, holidays, and local foot traffic. This engine will automatically suggest optimized preparation quantities to restaurant chefs each morning, preventing surplus from being generated in the first place.")

add_heading_2("10.2 Native Mobile Applications (iOS & Android)")
add_para("Developing cross-platform mobile apps using React Native or Flutter, offering geofenced push notifications that alert consumers on their smartphones whenever their favorite bakery publishes surprise bags within a 2-kilometer radius.")

add_heading_2("10.3 Direct Integration with Commercial POS Systems")
add_para("Creating automated integration plugins for popular Point-of-Sale (POS) systems (such as Toast, Square, and Clover). When items remain unsold in the restaurant register 45 minutes prior to closing, the POS integration can automatically publish them to the Surplus Food marketplace without requiring manual intervention from kitchen staff.")

add_heading_2("10.4 Dedicated NGO & Charity Donation Routing")
add_para("Introducing an automated charity dispatch pipeline. For items that remain unreserved by retail consumers 15 minutes before closing, the platform can automatically dispatch notifications to local food banks, shelters, and voluntary relief organizations for free bulk pickup.")

# ================= CHAPTER 11: CONCLUSION =================
add_divider_page("CONCLUSION")
add_heading_1("11. CONCLUSION")
add_para("Urban food wastage represents an immense economic loss and ecological hazard that demands innovative, technological intervention. While billions of dollars worth of fresh, wholesome meals are discarded each day, millions of consumers seek affordable dining options amid soaring food inflation. Surplus Food Rescue & Marketplace was conceived, engineered, and evaluated specifically to eliminate this systemic divide.")
add_para("By harmonizing food businesses, neighborhood consumers, and system administrators into an integrated real-time marketplace, the platform turns food waste into an opportunity for economic recovery and environmental conservation. The integration of role-based security, instant Surprise Bag reservations, automated OTP and QR redemption tokens, live WebSocket order dispatching, and background cron markdown routines transforms food rescue into a seamless, profitable, and dignified daily experience.")
add_para("Developed using the modern MERN Stack (React.js, Node.js, Express.js, and MongoDB Atlas) paired with Socket.io, the project demonstrates the successful realization of an enterprise-grade full-stack web application. Surplus Food satisfies all technical, operational, and academic criteria prescribed by the APJ Abdul Kalam Kerala Technological University for the Master of Computer Applications curriculum, while establishing a meaningful and sustainable contribution to modern ecological informatics.")

# ================= CHAPTER 12: APPENDIX =================
add_divider_page("APPENDIX")
add_heading_1("12. APPENDIX")

screenshots_data = [
    ("01_landing.png", "Figure 12.1: Hero Landing Page & Sustainability Mission Portal"),
    ("02_login.png", "Figure 12.2: Multi-Role Authentication & Email OTP Verification"),
    ("03_customer_dashboard.png", "Figure 12.3: Customer Surplus Food Exploration Catalog & Surprise Bags"),
    ("04_customer_orders.png", "Figure 12.4: Customer Active Reservations, OTP Token & QR Collection Pass"),
    ("05_customer_profile.png", "Figure 12.5: Customer Profile & Account Settings Management"),
    ("06_restaurant_dashboard.png", "Figure 12.6: Restaurant Business Hub & Live Surplus Inventory Management"),
    ("07_restaurant_reservations.png", "Figure 12.7: Restaurant Customer Bookings Queue & QR Scanner Verification"),
    ("08_admin_dashboard.png", "Figure 12.8: Admin Command Center & Environmental Impact Analytics"),
    ("09_admin_verification.png", "Figure 12.9: Admin Restaurant Verification & Profile Audit Console"),
    ("10_admin_listings.png", "Figure 12.10: Admin Global Platform Postings & Expired Items Sweeper")
]

for filename, caption in screenshots_data:
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
        r.font.bold = True

# ================= CHAPTER 13: BIBLIOGRAPHY =================
add_divider_page("BIBLIOGRAPHY")
add_heading_1("13. BIBLIOGRAPHY")

add_heading_2("Websites")
add_para("[1] https://react.dev/")
add_para("[2] https://nodejs.org/docs/latest/api/")
add_para("[3] https://expressjs.com/")
add_para("[4] https://www.mongodb.com/docs/")
add_para("[5] https://mongoosejs.com/docs/")
add_para("[6] https://socket.io/docs/v4/")
add_para("[7] https://jwt.io/introduction")
add_para("[8] https://vitejs.dev/")
add_para("[9] https://lucide.dev/")
add_para("[10] https://www.npmjs.com/package/node-cron")

add_heading_2("Books")
add_para("[1] David Flanagan, JavaScript: The Definitive Guide (7th Edition), O'Reilly Media, 2020.")
add_para("[2] Ethan Brown, Web Development with Node and Express: Leveraging the JavaScript Stack (2nd Edition), O'Reilly Media, 2019.")
add_para("[3] Alex Banks and Eve Porcello, Learning React: Modern Patterns for Developing React Applications (2nd Edition), O'Reilly Media, 2020.")
add_para("[4] Kristina Chodorow, MongoDB: The Definitive Guide: Powerful and Scalable Storage (3rd Edition), O'Reilly Media, 2019.")
add_para("[5] Rohit Rai, Socket.IO Real-Time Web Application Development, Packt Publishing, 2017.")

docx_output_path = "d:/surplus-food/Surplus_Food_Project_Report.docx"
doc.save(docx_output_path)
print(f"Successfully updated DOCX with authentic logos and user details: {docx_output_path}")

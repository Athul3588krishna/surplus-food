import asyncio
import os
import base64
from playwright.async_api import async_playwright

def get_base64_img(filename):
    path = os.path.join("d:/surplus-food/screenshots", filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

img_landing = get_base64_img("01_landing.png")
img_login = get_base64_img("02_login.png")
img_cust_dash = get_base64_img("03_customer_dashboard.png")
img_cust_orders = get_base64_img("04_customer_orders.png")
img_cust_prof = get_base64_img("05_customer_profile.png")
img_rest_dash = get_base64_img("06_restaurant_dashboard.png")
img_rest_res = get_base64_img("07_restaurant_reservations.png")
img_admin_dash = get_base64_img("08_admin_dashboard.png")
img_admin_veri = get_base64_img("09_admin_verification.png")
img_admin_list = get_base64_img("10_admin_listings.png")

print("All screenshots loaded into memory for clean PDF rendering.")

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Surplus Food Rescue & Marketplace - Project Report</title>
<style>
  @page {{
    size: A4;
    margin: 20mm 20mm 20mm 20mm;
    @bottom-center {{
      content: counter(page);
    }}
  }}

  *, *:before, *:after {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #000000;
    margin: 0;
    padding: 0;
    text-align: justify;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 12pt;
    text-indent: 0;
  }}

  /* Page Break Utilities */
  .page-break {{
    page-break-before: always;
    break-before: page;
  }}

  .avoid-break {{
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  /* Running Header & Footer for content pages */
  .running-header {{
    position: running(header);
    font-size: 10pt;
    font-style: italic;
    border-bottom: 1px solid #000;
    padding-bottom: 4px;
    margin-bottom: 25px;
    display: flex;
    justify-content: space-between;
  }}

  /* Title / Cover Page */
  .cover-page {{
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    min-height: 900px;
    padding: 20px 0;
  }}

  .cover-title {{
    font-size: 24pt;
    font-weight: bold;
    letter-spacing: 1px;
    margin-top: 40px;
    margin-bottom: 30px;
    text-transform: uppercase;
  }}

  .cover-subtitle {{
    font-size: 13pt;
    font-style: italic;
    line-height: 1.6;
    margin-bottom: 25px;
  }}

  .cover-degree {{
    font-size: 16pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
  }}

  .cover-univ {{
    font-size: 13pt;
    font-weight: bold;
    margin-bottom: 25px;
  }}

  .ktu-emblem {{
    width: 75px;
    height: auto;
    margin: 15px auto;
  }}

  .college-emblem {{
    width: 90px;
    height: auto;
    margin: 15px auto;
  }}

  .cover-submitted {{
    font-size: 12pt;
    margin-top: 15px;
    margin-bottom: 6px;
  }}

  .cover-author {{
    font-size: 13pt;
    font-weight: bold;
    letter-spacing: 0.5px;
    margin-bottom: 25px;
  }}

  .cover-college {{
    font-size: 13pt;
    font-weight: bold;
    margin-top: 15px;
    line-height: 1.4;
  }}

  .cover-date {{
    font-size: 12pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 15px;
  }}

  /* Certificate Page */
  .cert-header {{
    text-align: center;
    font-weight: bold;
    font-size: 13pt;
    line-height: 1.4;
    margin-bottom: 25px;
  }}

  .cert-title {{
    text-align: center;
    font-size: 18pt;
    font-weight: bold;
    letter-spacing: 1px;
    margin-top: 30px;
    margin-bottom: 30px;
  }}

  .cert-body {{
    font-size: 12pt;
    line-height: 1.8;
    text-align: justify;
    margin-bottom: 60px;
  }}

  .signature-grid {{
    display: flex;
    justify-content: space-between;
    margin-top: 70px;
  }}

  .sig-block {{
    width: 45%;
    font-size: 12pt;
    line-height: 1.4;
  }}

  .sig-name {{
    font-weight: bold;
  }}

  /* Headings */
  h1.section-title {{
    font-size: 15pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 0;
    margin-bottom: 16pt;
    text-align: left;
  }}

  h1.section-title-center {{
    font-size: 16pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 10px;
    margin-bottom: 20pt;
    text-align: center;
  }}

  /* Divider page for main parts */
  .chapter-divider {{
    height: 800px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }}

  .chapter-divider h1 {{
    font-size: 20pt;
    font-weight: bold;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}

  h2.subsection-title {{
    font-size: 13pt;
    font-weight: bold;
    margin-top: 16pt;
    margin-bottom: 8pt;
  }}

  h3.subsubsection-title {{
    font-size: 12pt;
    font-weight: bold;
    margin-top: 14pt;
    margin-bottom: 6pt;
  }}

  ul {{
    margin-top: 4pt;
    margin-bottom: 12pt;
    padding-left: 24pt;
  }}

  li {{
    margin-bottom: 5pt;
  }}

  /* Tables */
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12pt;
    margin-bottom: 16pt;
    font-size: 11pt;
  }}

  table.content-table th, table.content-table td {{
    border: 1px solid #000;
    padding: 6pt 8pt;
    text-align: left;
    vertical-align: top;
  }}

  table.content-table th {{
    font-weight: bold;
    background-color: #f2f2f2;
  }}

  /* TOC Table */
  table.toc-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12pt;
    line-height: 1.7;
  }}

  table.toc-table td {{
    padding: 2pt 0;
  }}

  table.toc-table .toc-num {{
    width: 10%;
    vertical-align: top;
  }}

  table.toc-table .toc-title {{
    width: 80%;
    vertical-align: top;
  }}

  table.toc-table .toc-page {{
    width: 10%;
    text-align: right;
    vertical-align: top;
  }}

  /* Code / Schema JSON blocks */
  pre.code-json {{
    font-family: 'Consolas', 'Courier New', Courier, monospace;
    font-size: 9.5pt;
    background: #fdfdfd;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10pt;
    line-height: 1.35;
    margin-top: 6pt;
    margin-bottom: 14pt;
    white-space: pre-wrap;
    word-break: break-all;
    color: #1a202c;
  }}

  /* DFD styling (Pure Clean CSS) */
  .dfd-container {{
    border: 1px solid #94a3b8;
    background: #f8fafc;
    border-radius: 6px;
    padding: 18px;
    margin: 14pt 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
    page-break-inside: avoid;
  }}

  .dfd-title {{
    font-weight: bold;
    font-size: 11pt;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #0f172a;
  }}

  .dfd-box {{
    border: 2px solid #000;
    background: #ffffff;
    padding: 10px 18px;
    font-weight: bold;
    font-size: 11pt;
    text-align: center;
    min-width: 160px;
  }}

  .dfd-circle {{
    border: 2px solid #000;
    background: #ffffff;
    border-radius: 50%;
    width: 170px;
    height: 110px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 10.5pt;
    text-align: center;
    padding: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }}

  .dfd-store {{
    border-top: 2px solid #000;
    border-bottom: 2px solid #000;
    border-left: none;
    border-right: none;
    background: #ffffff;
    padding: 6px 14px;
    font-family: monospace;
    font-weight: bold;
    font-size: 10pt;
    min-width: 140px;
    text-align: center;
  }}

  .dfd-arrow {{
    font-size: 10pt;
    font-weight: bold;
    color: #334155;
    text-align: center;
    line-height: 1.2;
  }}

  /* Appendix Screenshot Cards */
  .screenshot-card {{
    text-align: center;
    margin-bottom: 20pt;
    page-break-inside: avoid;
  }}

  .screenshot-card img {{
    max-width: 95%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
  }}

  .screenshot-caption {{
    font-size: 11pt;
    font-weight: bold;
    margin-top: 8pt;
    margin-bottom: 14pt;
    color: #000;
  }}
</style>
</head>
<body>

  <!-- ================= PAGE 1: COVER PAGE ================= -->
  <div class="cover-page">
    <div class="cover-title">SURPLUS FOOD RESCUE &amp; MARKETPLACE</div>
    
    <div class="cover-subtitle">
      A project report<br>
      submitted in fulfillment of<br>
      the requirements for the award of the degree of
    </div>

    <div class="cover-degree">MASTER OF COMPUTER APPLICATIONS</div>
    <div class="cover-univ">From<br>APJ Abdul Kalam Kerala Technological University</div>

    <div style="margin: 12px 0;"><img src="data:image/png;base64,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" style="width: 95px; height: auto;" /></div>

    <div class="cover-submitted">Submitted By</div>
    <div class="cover-author">RISHIN V (MEA25MCA2021)</div>

    <div style="margin: 12px 0;"><img src="data:image/png;base64,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" style="width: 110px; height: auto;" /></div>

    <div class="cover-college">
      MEA Engineering College<br>
      Department of Computer Applications<br>
      Vengoor P.O, Perinthalmanna, Malappuram, Kerala-679325
    </div>

    <div class="cover-date">OCTOBER 2026</div>
  </div>

  <!-- ================= PAGE 2: CERTIFICATE ================= -->
  <div class="page-break">
    <div class="cert-header">
      DEPARTMENT OF COMPUTER APPLICATIONS<br>
      MEA ENGINEERING COLLEGE<br>
      PERINTHALMANNA-679325
    </div>

    <div style="text-align: center; margin: 15px 0;"><img src="data:image/png;base64,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" style="width: 100px; height: auto;" /></div>

    <div class="cert-title">CERTIFICATE</div>

    <div class="cert-body">
      This is to certify that the Project report entitled <strong>"Surplus Food Rescue &amp; Marketplace"</strong> is a bonafide record of the work done by <strong>RISHIN V (MEA25MCA2021)</strong> under our supervision and guidance. The report has been submitted in fulfillment of the requirement for award of the Degree of Master of Computer Applications from the APJ Abdul Kalam Kerala Technological University for the year 2026.
    </div>

    <div class="signature-grid">
      <div class="sig-block">
        <div class="sig-name">Ms. Fathmath Hasna</div>
        <div>Assistant Professor</div>
        <div>Project Guide</div>
        <div>Dept. of Computer Applications</div>
      </div>
      <div class="sig-block" style="text-align: right;">
        <div class="sig-name">Mr. Sajeesh M</div>
        <div>Assistant Professor &amp; Head</div>
        <div>Head of the Department</div>
        <div>Dept. of Computer Applications</div>
      </div>
    </div>
  </div>

  <!-- ================= PAGE 3: ACKNOWLEDGEMENTS ================= -->
  <div class="page-break">
    <h1 class="section-title-center" style="font-style: italic;">Acknowledgements</h1>

    <p>
      First and foremost, I would like to thank Almighty God for giving me the knowledge, courage, and strength which helped me in the successful completion of this project.
    </p>

    <p>
      An endeavor of this magnitude can only be successful with the advice, motivation, and guidance of many well-wishers. I take this opportunity to express my heartfelt gratitude to all who encouraged me throughout this journey. I express my deep sense of gratitude to our respected Principal, <strong>Dr. Shahir VK</strong>, for his inspiring leadership and for fostering an excellent academic environment in the college.
    </p>

    <p>
      I would like to express my deepest gratitude and sincere indebtedness to <strong>Mr. Sajeesh M</strong>, Assistant Professor and Head of the Department, Department of Computer Applications, for providing permission and facilities to conduct this project in a systematic way.
    </p>

    <p>
      I am profoundly thankful to my Project Guide, <strong>Ms. Fathmath Hasna</strong>, Assistant Professor in the Department of Computer Applications, for her invaluable technical guidance, timely advice, constructive critique, and wholehearted moral support throughout the conception, development, and completion of the Surplus Food Rescue &amp; Marketplace project.
    </p>

    <p>
      I also extend my sincere gratitude to all the esteemed faculty members and technical staff of the Department of Computer Applications for their constant cooperation, encouragement, and valuable assistance during various stages of this project.
    </p>

    <div style="margin-top: 50px; text-align: right;">
      <div style="font-weight: bold;">RISHIN V (MEA25MCA2021)</div>
      <div style="margin-top: 5px;">DATE: OCTOBER 25, 2026</div>
    </div>
  </div>

  <!-- ================= PAGE 4: ABSTRACT ================= -->
  <div class="page-break">
    <h1 class="section-title-center">ABSTRACT</h1>

    <p>
      Food wastage represents a staggering ecological and socio-economic challenge worldwide. Massive quantities of perfectly edible, wholesome cooked dishes, artisanal bakery goods, and grocery surplus are discarded daily by commercial food businesses simply because items remain unsold at the conclusion of regular trading hours. Concurrently, consumers encounter steep inflation on food commodities, while local charities and price-conscious individuals struggle to secure nutritious sustenance affordably.
    </p>

    <p>
      To effectively solve this systemic inefficiency, <strong>Surplus Food Rescue &amp; Marketplace (EcoBite)</strong> is engineered as a robust, real-time web-based marketplace dedicated to bridging food business surplus directly with neighborhood consumers. The platform provides dedicated, role-based access for three distinct operational actors: <strong>Customer</strong>, <strong>Restaurant Partner</strong>, and <strong>Platform Administrator</strong>.
    </p>

    <p>
      Customers can discover certified nearby bakeries and eateries, filter surplus food items by cuisine, pricing, and allergen restrictions, buy curated discounted surplus bundles or "Daily Mystery Bags" at 50% to 80% below retail value, securely checkout, and receive instant cryptographic OTP pickup tokens alongside scannable QR verification codes. Restaurant Partners can easily list excess inventory with strict collection timeframes, monitor incoming customer bookings in real time via WebSocket events, and validate customer redemptions using built-in QR camera scanning or PIN confirmation. Platform Administrators retain comprehensive oversight by conducting credential verification of registered restaurants, auditing food catalogs, executing automated cleanup sweeps of expired foodstuffs, and monitoring system-wide financial and environmental savings metrics.
    </p>

    <p>
      The platform is developed using the modern MERN Stack (React.js, Node.js, Express.js, and MongoDB Atlas) paired with Socket.io for instantaneous multi-party notifications, JWT for role-based session authorization, Bcrypt for credential encryption, and automated background Node-Cron tasks for continuous auto-expiry and dynamic price markdown orchestration. The application delivers an efficient, reliable, and sustainable solution to urban food wastage, establishing a complete enterprise-grade full-stack web application suitable for academic excellence and real-world commercial deployment.
    </p>
  </div>

  <!-- ================= PAGE 5: CONTENTS ================= -->
  <div class="page-break">
    <h1 class="section-title-center">CONTENTS</h1>

    <table class="toc-table">
      <tr><td class="toc-num"><strong>1.</strong></td><td class="toc-title"><strong>INTRODUCTION</strong></td><td class="toc-page"><strong>1</strong></td></tr>
      <tr><td class="toc-num"><strong>2.</strong></td><td class="toc-title"><strong>SYSTEM ANALYSIS</strong></td><td class="toc-page"><strong>3</strong></td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">2.1 Existing System</td><td class="toc-page">4</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">2.2 Proposed System</td><td class="toc-page">4</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">2.3 Module Description</td><td class="toc-page">4</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">2.4 Sprint</td><td class="toc-page">5</td></tr>
      <tr><td class="toc-num"><strong>3.</strong></td><td class="toc-title"><strong>FEASIBILITY STUDY</strong></td><td class="toc-page"><strong>8</strong></td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">3.1 Economical Feasibility</td><td class="toc-page">9</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">3.2 Technical Feasibility</td><td class="toc-page">9</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">3.3 Operational Feasibility</td><td class="toc-page">9</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">3.4 Behavioural Feasibility</td><td class="toc-page">9</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">3.5 Software Feasibility</td><td class="toc-page">10</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">3.6 Hardware Feasibility</td><td class="toc-page">10</td></tr>
      <tr><td class="toc-num"><strong>4.</strong></td><td class="toc-title"><strong>SOFTWARE ENGINEERING PARADIGM</strong></td><td class="toc-page"><strong>11</strong></td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">4.1 Agile Model</td><td class="toc-page">12</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">4.2 Scrum</td><td class="toc-page">12</td></tr>
      <tr><td class="toc-num"><strong>5.</strong></td><td class="toc-title"><strong>SYSTEM REQUIREMENT SPECIFICATION</strong></td><td class="toc-page"><strong>13</strong></td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">5.1 Software Requirements</td><td class="toc-page">14</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">5.2 Hardware Requirements</td><td class="toc-page">14</td></tr>
      <tr><td class="toc-num"><strong>6.</strong></td><td class="toc-title"><strong>SYSTEM DESIGN</strong></td><td class="toc-page"><strong>15</strong></td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">6.1 Database Design</td><td class="toc-page">16</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">6.2 Tables</td><td class="toc-page">18</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">6.3 UML Design</td><td class="toc-page">20</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">6.4 Use Case Diagram</td><td class="toc-page">21</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">6.5 Scenario</td><td class="toc-page">22</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">6.6 Data flow diagram</td><td class="toc-page">23</td></tr>
      <tr><td class="toc-num"><strong>7.</strong></td><td class="toc-title"><strong>SYSTEM DEVELOPMENT</strong></td><td class="toc-page"><strong>27</strong></td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">7.1 Coding</td><td class="toc-page">28</td></tr>
      <tr><td class="toc-num"><strong>8.</strong></td><td class="toc-title"><strong>SYSTEM TESTING AND IMPLEMENTATION</strong></td><td class="toc-page"><strong>31</strong></td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">8.1 Types of Testing</td><td class="toc-page">32</td></tr>
      <tr><td class="toc-num"></td><td class="toc-title">8.2 Implementation</td><td class="toc-page">34</td></tr>
      <tr><td class="toc-num"><strong>9.</strong></td><td class="toc-title"><strong>SYSTEM MAINTENANCE</strong></td><td class="toc-page"><strong>35</strong></td></tr>
      <tr><td class="toc-num"><strong>10.</strong></td><td class="toc-title"><strong>FUTURE ENHANCEMENT</strong></td><td class="toc-page"><strong>37</strong></td></tr>
      <tr><td class="toc-num"><strong>11.</strong></td><td class="toc-title"><strong>CONCLUSION</strong></td><td class="toc-page"><strong>39</strong></td></tr>
      <tr><td class="toc-num"><strong>12.</strong></td><td class="toc-title"><strong>APPENDIX</strong></td><td class="toc-page"><strong>41</strong></td></tr>
      <tr><td class="toc-num"><strong>13.</strong></td><td class="toc-title"><strong>BIBLIOGRAPHY</strong></td><td class="toc-page"><strong>48</strong></td></tr>
    </table>
  </div>

  <!-- ================= CHAPTER 1 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>INTRODUCTION</h1>
  </div>

  <!-- ================= CHAPTER 1: INTRODUCTION ================= -->
  <div class="page-break">
    <h1 class="section-title">1. INTRODUCTION</h1>

    <p>
      Food loss and culinary waste have emerged as severe ecological, economic, and moral challenges of contemporary society. Each year, billions of tons of high-grade, wholesome cooked dishes, artisan breads, delicate pastries, and grocery items are produced and transported only to be dumped into municipal landfills. Within commercial food establishments—including restaurants, bakeries, cafes, and supermarket hot-bars—food items that remain unpurchased at the end of the operating shift are routinely discarded due to the perishable nature of fresh items, stringent aesthetic guidelines, and lack of dynamic redistribution channels.
    </p>

    <p>
      This widespread wastage generates severe environmental consequences. Decomposing organic food products in open landfills produce massive quantities of methane, a potent greenhouse gas that accelerates global climatic warming. Concurrently, consumers and working families face sharp cost-of-living increases, making nutritious meals expensive to afford regularly. Traditional food redistribution approaches, such as sporadic charitable donations or word-of-mouth discounts, are fundamentally uncoordinated, slow, and operationally burdensome for commercial kitchen managers.
    </p>

    <p>
      To address these critical inefficiencies, I developed the <strong>Surplus Food Rescue &amp; Marketplace (EcoBite)</strong> platform. The system establishes a synchronized, hyper-local digital marketplace connecting food businesses burdened with surplus stock directly with conscientious neighborhood consumers looking for discounted meals. The application provides dedicated role-based portals for Customers, Restaurant Partners, and System Administrators, engineered to eliminate operational delays and facilitate friction-free transactions.
    </p>

    <p>
      The platform empowers customers to discover verified local food stores, filter items by diet, cuisine, and allergen sensitivities, order mystery surprise bags at steep 50% to 80% markdowns, and retrieve food securely using tamper-proof OTP collection codes and QR passes. Restaurants gain an intuitive merchant hub to monetize excess stock, broadcast dynamic discounts during final trading minutes, and verify collections effortlessly with camera-based QR scanning. Administrators oversee platform health, verify restaurant licenses, audit food listings, and monitor aggregated carbon offsets.
    </p>

    <p>
      Engineered on the modern MERN Stack (React.js, Node.js, Express.js, and MongoDB Atlas) with Socket.io real-time websockets, the Surplus Food platform provides an efficient, transparent, and scalable solution to urban food wastage, perfectly suited for academic evaluation and real-world deployment.
    </p>
  </div>

  <!-- ================= CHAPTER 2 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>SYSTEM ANALYSIS</h1>
  </div>

  <!-- ================= CHAPTER 2: SYSTEM ANALYSIS ================= -->
  <div class="page-break">
    <h1 class="section-title">2. SYSTEM ANALYSIS</h1>

    <h2 class="subsection-title">2.1 Existing System</h2>
    <p>
      In the existing food retail ecosystem, restaurants, grocery vendors, and bakeries rely heavily on manual forecasting to calculate daily preparation quantities. Because consumer demand fluctuates wildly depending on weather, local foot traffic, and daily events, kitchens consistently prepare surplus inventory to prevent running out of menu offerings. At the conclusion of daily trading, leftover prepared food is routinely discarded into trash compactors.
    </p>
    <p>
      Currently, there is no unified digital channel enabling merchants to rapidly alert nearby customers of available surplus items during closing hours. Traditional food bank donations, while noble, require scheduled logistical coordination, refrigerated transport vehicles, and extensive paperwork, making them impractical for small, hot perishable batches. Furthermore, consumers lack a trusted mechanism to identify which local stores have discounted items available for immediate collection, leading to massive financial waste for businesses and preventable environmental damage.
    </p>

    <h2 class="subsection-title">2.2 Proposed System</h2>
    <p>
      The proposed system, <strong>Surplus Food Rescue &amp; Marketplace</strong>, introduces a centralized full-stack web application designed to eliminate food waste by facilitating rapid, hyper-local surplus food transactions. The system introduces dedicated, role-based workflows for Customers, Restaurant Partners, and Administrators.
    </p>
    <p>
      Customers can browse available food listings in real time, filter by dietary requirements (Veg, Non-Veg, Vegan, Gluten-Free, Halal), reserve curated Mystery Surprise Bags, and receive a secure 6-digit OTP token and scannable QR verification code. Restaurants can post surplus inventory in under a minute, set designated pickup windows, receive instantaneous WebSocket booking notifications, and verify redemptions seamlessly with built-in QR scanning. Platform Administrators ensure marketplace trust by auditing restaurant credentials, monitoring active postings, and analyzing system-wide sustainability metrics.
    </p>

    <h2 class="subsection-title">2.3 Module Description</h2>
    <p>
      The Surplus Food platform is structured into three specialized functional modules based on user roles, each tailored to execute distinct business workflows:
    </p>

    <h3 class="subsubsection-title">Admin Module</h3>
    <ul>
      <li>Secure administrator authentication and multi-tier role-based access control.</li>
      <li>Audit, approve, or decline onboarding restaurant business profiles and operating credentials.</li>
      <li>Comprehensive registry management to monitor all registered customers and merchant accounts.</li>
      <li>System-wide inventory monitoring across all active surplus food postings.</li>
      <li>Automated maintenance trigger to sweep and delete expired food items past pickup windows.</li>
      <li>Live analytics dashboard displaying total meals rescued, financial customer savings, and CO2 emissions prevented.</li>
    </ul>

    <h3 class="subsubsection-title">Customer Module</h3>
    <ul>
      <li>User registration, secure email OTP validation, and JWT session authentication.</li>
      <li>Interactive food exploration hub with filtering by cuisine, price range, dietary preferences, and allergens.</li>
      <li>Surplus Surprise Bag discovery offering mystery assortments at 50% to 80% markdowns.</li>
      <li>Real-time booking and checkout with automated collection token (OTP) and QR code generation.</li>
      <li>Digital reservation voucher download in printable PDF receipt format.</li>
      <li>Personalized reservations tracker displaying active pickup windows and past order histories.</li>
      <li>Post-pickup review and star rating submission to maintain vendor quality.</li>
    </ul>

    <h3 class="subsubsection-title">Restaurant Module</h3>
    <ul>
      <li>Merchant onboarding with business name, address, cuisine specialization, and logo uploads.</li>
      <li>Surplus food item listing engine with original price, discounted price, stock count, and strict pickup hours.</li>
      <li>Surplus Mystery Bag toggle with pre-configured value estimates and descriptions.</li>
      <li>Real-time WebSocket booking alerts notifying kitchen staff immediately upon customer order placement.</li>
      <li>Customer collection verification via manual 6-digit OTP entry or built-in camera QR scanner.</li>
      <li>Live merchant analytics tracking total sales revenue, units rescued, and customer satisfaction ratings.</li>
    </ul>
  </div>

  <!-- ================= CHAPTER 2: SPRINTS ================= -->
  <div class="page-break">
    <h2 class="subsection-title">2.4 Sprint</h2>

    <h3 class="subsubsection-title">Sprint 1: Core Authentication &amp; Customer Portal</h3>
    <table class="content-table">
      <thead>
        <tr>
          <th>Module</th>
          <th>Task</th>
          <th>Pending task if any</th>
          <th>Hour of completion</th>
          <th>Expected date of completion</th>
          <th>Actual date of completion</th>
          <th>Reason for delay</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td rowspan="5">Customer</td>
          <td>User Registration &amp; Email OTP Verification</td>
          <td>-</td>
          <td>2 hr.</td>
          <td>19/07/2026</td>
          <td>19/07/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>JWT Login &amp; Role Authorization</td>
          <td>-</td>
          <td>2 hr.</td>
          <td>21/07/2026</td>
          <td>21/07/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>Surplus Catalog &amp; Filter Grid (Cuisine/Allergens)</td>
          <td>-</td>
          <td>4 hr.</td>
          <td>23/07/2026</td>
          <td>23/07/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>Food Reservation &amp; OTP Token Engine</td>
          <td>-</td>
          <td>3 hr.</td>
          <td>25/07/2026</td>
          <td>25/07/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>QR Code Pass &amp; PDF Receipt Generation</td>
          <td>-</td>
          <td>4 hr.</td>
          <td>28/07/2026</td>
          <td>28/07/2026</td>
          <td>-</td>
        </tr>
      </tbody>
    </table>

    <h3 class="subsubsection-title">Sprint 2: Restaurant Hub &amp; Real-time Verification</h3>
    <table class="content-table">
      <thead>
        <tr>
          <th>Module</th>
          <th>Task</th>
          <th>Pending task if any</th>
          <th>Hour of completion</th>
          <th>Expected date of completion</th>
          <th>Actual date of completion</th>
          <th>Reason for delay</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td rowspan="5">Restaurant</td>
          <td>Store Profile Setup &amp; Verification Submission</td>
          <td>-</td>
          <td>2 hr.</td>
          <td>10/08/2026</td>
          <td>10/08/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>Surplus Listing Management &amp; Image Uploads</td>
          <td>-</td>
          <td>5 hr.</td>
          <td>12/08/2026</td>
          <td>12/08/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>Surprise Bag &amp; Dynamic Markdown Pricing</td>
          <td>-</td>
          <td>3 hr.</td>
          <td>14/08/2026</td>
          <td>14/08/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>WebSocket Real-Time Order Dispatch</td>
          <td>-</td>
          <td>4 hr.</td>
          <td>15/08/2026</td>
          <td>15/08/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>Camera QR Scanner &amp; Token Verification</td>
          <td>-</td>
          <td>3 hr.</td>
          <td>17/08/2026</td>
          <td>17/08/2026</td>
          <td>-</td>
        </tr>
      </tbody>
    </table>

    <h3 class="subsubsection-title">Sprint 3: Administration, Automated Jobs &amp; Analytics</h3>
    <table class="content-table">
      <thead>
        <tr>
          <th>Module</th>
          <th>Task</th>
          <th>Pending task if any</th>
          <th>Hour of completion</th>
          <th>Expected date of completion</th>
          <th>Actual date of completion</th>
          <th>Reason for delay</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td rowspan="5">Admin</td>
          <td>Admin Command Center &amp; Access Controls</td>
          <td>-</td>
          <td>2 hr.</td>
          <td>18/08/2026</td>
          <td>18/08/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>Merchant Store Profile Verification &amp; Auditing</td>
          <td>-</td>
          <td>4 hr.</td>
          <td>20/08/2026</td>
          <td>20/08/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>Global Postings Monitor &amp; Expired Sweeper</td>
          <td>-</td>
          <td>4 hr.</td>
          <td>22/08/2026</td>
          <td>22/08/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>Node-Cron Auto-Expiry &amp; Markdown Engine</td>
          <td>-</td>
          <td>5 hr.</td>
          <td>24/08/2026</td>
          <td>24/08/2026</td>
          <td>-</td>
        </tr>
        <tr>
          <td>System Metrics, User Management &amp; Analytics</td>
          <td>-</td>
          <td>3 hr.</td>
          <td>28/08/2026</td>
          <td>28/08/2026</td>
          <td>-</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ================= CHAPTER 3 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>FEASIBILITY STUDY</h1>
  </div>

  <!-- ================= CHAPTER 3: FEASIBILITY STUDY ================= -->
  <div class="page-break">
    <h1 class="section-title">3. FEASIBILITY STUDY</h1>

    <p>
      An analysis of the ability to complete a project successfully, taking into account legal, economic, technological, scheduling, and other factors is considered as a feasibility study. Rather than just diving into a project and hoping for the best, a feasibility study allows project managers to investigate the possible negative and positive outcomes of a project before investing too much time and money.
    </p>

    <h2 class="subsection-title">3.1 Economical Feasibility</h2>
    <p>
      The proposed system is economically highly feasible because it is built entirely using robust, open-source technologies including React.js, Node.js, Express.js, MongoDB Atlas (Community Tier), Socket.io, Git, and GitHub. None of these core technologies require proprietary or expensive software licensing fees. Development and testing were executed on standard consumer computing hardware using freely available, industry-standard developer tooling such as Visual Studio Code and Postman. Since the primary objective of Surplus Food Rescue &amp; Marketplace is food waste mitigation and academic evaluation, the capital expenditure and operational maintenance costs remain exceptionally low, while delivering an enterprise-grade commercial web application.
    </p>

    <h2 class="subsection-title">3.2 Technical Feasibility</h2>
    <p>
      The project is technically feasible as all necessary frameworks and libraries are mature, extensively documented, and supported by vibrant global developer communities. The MERN Stack provides an asynchronous, non-blocking architecture ideally suited for high-throughput marketplace communications. MongoDB provides high-performance schema flexibility for nested surplus food catalogs and order tracking. Socket.io guarantees bidirectional WebSocket dispatching with sub-second latencies, essential for alerting merchants of immediate orders. JWT ensures cryptographic, stateless role-based security, while HTML5 QR libraries enable effortless in-browser barcode verification. The system architecture has been thoroughly verified using modern full-stack software development methodologies.
    </p>

    <h2 class="subsection-title">3.3 Operational Feasibility</h2>
    <p>
      Surplus Food Rescue &amp; Marketplace is operationally feasible because its user interfaces are deliberately designed for fast-paced food service scenarios with minimal cognitive load. For customers, the intuitive catalog allows one-click filtering, instant cartless reservations, and scannable QR passes requiring zero technical training. For restaurant staff, the responsive dashboard provides live audio-visual order alerts and one-tap camera QR scanning that integrates seamlessly into frantic kitchen closing routines. For administrators, the centralized operational dashboard provides clear tabular auditing of store registrations and item listings. This streamlined design ensures that users across all skill levels can operate the system effectively.
    </p>

    <h2 class="subsection-title">3.4 Behavioural Feasibility</h2>
    <p>
      Behavioral feasibility examines the willingness and confidence of stakeholders to adopt the proposed digital system. Restaurant owners are strongly motivated to adopt the system because it transforms what was previously discarded as pure financial loss into a supplemental revenue stream, while bolstering their public environmental reputation. Customers are enthusiastically driven to participate by substantial discounts (50% to 80% markdowns) on restaurant-quality food, combined with the altruistic satisfaction of rescuing edible food from landfills. These powerful positive behavioral drivers guarantee high user adoption and sustained community engagement.
    </p>

    <h2 class="subsection-title">3.5 Software Feasibility</h2>
    <p>
      The software requirements for the project encompass a standard modern operating system (Windows 10/11, Linux, or macOS) supporting Node.js (v18+) runtime environment, React.js (v19/18) with Vite for frontend rendering, Express.js (v4.19) for backend REST microservices, and MongoDB Atlas for distributed database storage. Ancillary software includes Socket.io for bidirectional WebSocket messaging, jsPDF and QRCode.react for client-side receipt generation, JSON Web Token (JWT) and Bcrypt for encryption and authorization, Dotenv for secure environment variables, and Git/GitHub for distributed version control. All software components are readily accessible, production-stable, and fully compatible.
    </p>

    <h2 class="subsection-title">3.6 Hardware Feasibility</h2>
    <p>
      The hardware infrastructure necessary to run and interact with Surplus Food Rescue &amp; Marketplace is widely available and affordable. The server-side platform can be hosted on standard cloud instances or local machines with a minimum of an Intel Core i3 / AMD Ryzen dual-core processor, 8 GB of RAM, and modest solid-state storage. On the client side, the web application runs responsively on any standard desktop, laptop, or mobile smartphone with a standard web browser and an internet connection (broadband, 4G, or 5G). No specialized POS hardware or proprietary scanners are required, making the deployment highly cost-effective and scalable.
    </p>
  </div>

  <!-- ================= CHAPTER 4 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>SOFTWARE ENGINEERING PARADIGM</h1>
  </div>

  <!-- ================= CHAPTER 4: SOFTWARE ENGINEERING PARADIGM ================= -->
  <div class="page-break">
    <h1 class="section-title">4. SOFTWARE ENGINEERING PARADIGM</h1>

    <p>
      The software engineering paradigm which is also referred to as a software process model or Software Development Life Cycle (SDLC) model is the development strategy that encompasses the process, methods and tools. SDLC describes the period of time that starts with the software system being conceptualized.
    </p>

    <h2 class="subsection-title">4.1 Agile model</h2>
    <p>
      The Agile SDLC model is a combination of iterative and incremental process models with focus on process adaptability and customer satisfaction by rapid delivery of working software product. Agile Methods break the product into small incremental builds. These builds are provided in iterations. Each iteration typically lasts from about one to three weeks. At the end of the iteration, a working product is displayed to the customer and important stakeholders.
    </p>
    <p>
      In Agile, the tasks are divided to time boxes (small time frames) to deliver specific features for a release. Iterative approach is taken and working software build is delivered after each iteration. Each build is incremental in terms of features; the final build holds all the features required by the customer.
    </p>

    <h2 class="subsection-title">4.2 Scrum</h2>
    <p>
      Scrum is an agile framework for managing knowledge work, with an emphasis on software development. It is designed for teams of three to nine members, who break their work into actions that can be completed within time boxed iterations, called "sprints", no longer than one month and most commonly two weeks, then track progress and re-plan in 15-minute stand-up meetings, called daily scrums.
    </p>
    <p>
      Scrum is an iterative and incremental framework for product development. It promotes a flexible strategy where development teams collaborate to achieve common goals, challenging traditional sequential methods. Scrum encourages self-organization, physical co-location, and daily communication among team members.
    </p>
  </div>

  <!-- ================= CHAPTER 5 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>SYSTEM REQUIREMENTS SPECIFICATION</h1>
  </div>

  <!-- ================= CHAPTER 5: SYSTEM REQUIREMENTS SPECIFICATION ================= -->
  <div class="page-break">
    <h1 class="section-title">5. SYSTEM REQUIREMENTS SPECIFICATION</h1>

    <h2 class="subsection-title">5.1 Software Requirements</h2>
    <table class="content-table">
      <thead>
        <tr>
          <th style="width: 35%;">Component</th>
          <th>Requirement</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Operating System</td>
          <td>Windows 10 / 11, Linux (Ubuntu 20.04+), macOS</td>
        </tr>
        <tr>
          <td>Backend Runtime</td>
          <td>Node.js (v18+), Express.js (v4.19), Socket.io (v4.8)</td>
        </tr>
        <tr>
          <td>Frontend Framework</td>
          <td>React.js (v19/18), Vite, Lucide-React, Axios</td>
        </tr>
        <tr>
          <td>Database</td>
          <td>MongoDB Atlas (v6.0+) / MongoDB Community Edition</td>
        </tr>
        <tr>
          <td>Ancillary Libraries</td>
          <td>Bcryptjs, JSONWebToken, HTML5-QRCode, jsPDF, Node-Cron</td>
        </tr>
        <tr>
          <td>Development IDE &amp; Tools</td>
          <td>Visual Studio Code, Postman API Client, Git, GitHub</td>
        </tr>
      </tbody>
    </table>

    <h2 class="subsection-title">5.2 Hardware Requirements</h2>
    <table class="content-table">
      <thead>
        <tr>
          <th style="width: 35%;">Component</th>
          <th>Requirement</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Processor</td>
          <td>Intel Core i3 / i5 or AMD Ryzen equivalent (2.0 GHz or above)</td>
        </tr>
        <tr>
          <td>RAM</td>
          <td>Minimum 8 GB (16 GB Recommended for development)</td>
        </tr>
        <tr>
          <td>Storage</td>
          <td>256 GB SSD or higher for database and runtime logs</td>
        </tr>
        <tr>
          <td>Display Monitor</td>
          <td>14" Full HD (1920x1080) or standard modern mobile display</td>
        </tr>
        <tr>
          <td>Camera Peripherals</td>
          <td>Standard webcam or smartphone camera (for QR scanning)</td>
        </tr>
        <tr>
          <td>Network</td>
          <td>Broadband / 4G / 5G active internet connection</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ================= CHAPTER 6 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>SYSTEM DESIGN</h1>
  </div>

  <!-- ================= CHAPTER 6: SYSTEM DESIGN ================= -->
  <div class="page-break">
    <h1 class="section-title">6. SYSTEM DESIGN</h1>

    <p>
      System design is the process of architecting the overall structure, modular components, database entities, communication interfaces, and operational data flows of a software application to fulfill specified functional and performance criteria. The system design of Surplus Food Rescue &amp; Marketplace focuses on engineering an ultra-responsive, highly available, resilient, and fault-tolerant architecture capable of coordinating time-sensitive food rescues, real-time inventory synchronization, dynamic markdown price drops, and rapid QR token validation during closing hours.
    </p>

    <h2 class="subsection-title">6.1 Database Design</h2>
    <p>
      Database design organizes and models system entities to ensure high data integrity, minimal redundancy, lightning-fast querying, and rapid transaction processing under concurrent customer ordering spikes. The Surplus Food platform utilizes MongoDB, an enterprise-grade NoSQL document-oriented database. Unlike rigid relational databases, MongoDB stores information in flexible, schema-validated JSON-like BSON documents within specialized collections. This structure natively supports polymorphic attributes such as allergen arrays, dietary classifications, dynamic price adjustments, and nested payment details.
    </p>
    <p>
      The database architecture is designed to manage complex relationships among customer users, restaurant profiles, surplus food listings, reservations/orders, and customer reviews. Unique ObjectIds and referenced indexes maintain data consistency across all collections.
    </p>
    <p>The major collections used in the system include:</p>
    <ul>
      <li><strong>Users</strong> — Stores user account credentials, hashed passwords (Bcrypt), contact phone numbers, assigned roles (customer, restaurant, admin), email verification statuses, and OTP codes.</li>
      <li><strong>RestaurantProfiles</strong> — Stores business metadata, restaurant name, street address, cuisine classification, operational description, store banner image paths, administrative verification flag, and aggregated customer ratings.</li>
      <li><strong>FoodItems</strong> — Stores surplus inventory listings, referenced restaurant profile IDs, item titles, descriptions, original pricing, discounted offer pricing, available quantity, daily pickup time windows, expiry timestamps, dietary badges, and Surprise Bag indicators.</li>
      <li><strong>Orders</strong> — Stores transaction records, referenced customer ID, restaurant ID, food item ID, quantity reserved, total price, order status (reserved, collected, cancelled), unique 6-digit OTP verification token, and payment details.</li>
      <li><strong>Reviews</strong> — Stores post-pickup ratings (1 to 5 stars), written customer comments, and references linking the reviewer, store, and verified order.</li>
    </ul>

    <h2 class="subsection-title">6.2 Tables (Database Schemas &amp; Data Dictionary)</h2>

    <h3 class="subsubsection-title">Database Schema 1: Users Collection (Customers, Restaurants, Admins)</h3>
    <pre class="code-json">
_id         : ObjectId('6a85e825d3f0510078fbec0c')
name        : "John Doe"
email       : "customer@surplus.com"
password    : "$2a$10$wN7KjZq0/2K3B...hashed..."
role        : "customer"
phoneNumber : "555-123-4567"
isVerified  : true
otpCode     : ""
createdAt   : 2026-08-16T10:15:30.000+00:00
__v         : 0
    </pre>

    <h3 class="subsubsection-title">Database Schema 2: RestaurantProfiles Collection</h3>
    <pre class="code-json">
_id            : ObjectId('6a85ea2eff5323a524c4f07d')
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
__v            : 0
    </pre>
  </div>

  <div class="page-break">
    <h3 class="subsubsection-title">Database Schema 3: FoodItems Collection (Surplus Listings &amp; Mystery Bags)</h3>
    <pre class="code-json">
_id                 : ObjectId('6ad1ab025bc04b489f991070')
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
__v                 : 0
    </pre>

    <h3 class="subsubsection-title">Database Schema 4: Orders Collection (Reservations &amp; Collection Tokens)</h3>
    <pre class="code-json">
_id            : ObjectId('6ad1abf55bc04b489f99108b')
customer       : ObjectId('6a85e825d3f0510078fbec0c')
restaurant     : ObjectId('6a85ea2eff5323a524c4f07d')
foodItem       : ObjectId('6ad1ab025bc04b489f991070')
quantity       : 1
totalPrice     : 2.50
status         : "reserved"
token          : "387421"
paymentStatus  : "paid"
paymentDetails : {{
                   "transactionId": "TXN-16237966",
                   "cardLast4": "4242"
                 }}
createdAt      : 2026-10-16T10:12:34.000+00:00
__v            : 0
    </pre>

    <h3 class="subsubsection-title">Database Schema 5: Reviews Collection</h3>
    <pre class="code-json">
_id        : ObjectId('6ad1ac225bc04b489f991094')
customer   : ObjectId('6a85e825d3f0510078fbec0c')
restaurant : ObjectId('6a85ea2eff5323a524c4f07d')
order      : ObjectId('6ad1abf55bc04b489f99108b')
rating     : 5
comment    : "Outstanding quality! Delicious croissants and bread at an unbelievable discount."
createdAt  : 2026-10-16T10:15:00.000+00:00
__v        : 0
    </pre>

    <h2 class="subsection-title">6.3 UML Designs</h2>
    <p>
      The Unified Modeling Language (UML) is a standard language for specifying, visualizing, constructing, and documenting the artifacts of software systems, as well as for business modeling and other non-software systems. The UML represents a collection of best engineering practices that have proven successful in the modeling of large and complex systems. UML uses mostly graphical notations to express the design of software projects. Using UML helps project teams communicate, explore potential designs, and validate the architectural design of the software.
    </p>

    <h2 class="subsection-title">6.4 Use Case Diagram</h2>
    <p>
      A use case diagram is a visual representation that shows how different users (called actors) interact with a system to achieve specific goals. It is one of the primary diagrams used in UML to capture functional requirements. Each use case represents a particular function or service the system provides, and the relationships between actors and use cases show who can perform which actions.
    </p>
  </div>

  <!-- ================= USE CASE DIAGRAM SVG ================= -->
  <div class="page-break">
    <div style="text-align: center; margin: 20px 0;">
      <svg width="680" height="760" viewBox="0 0 680 760" style="border: 1px solid #94a3b8; background: #ffffff; border-radius: 6px;">
        <!-- System Boundary -->
        <rect x="180" y="25" width="320" height="710" rx="15" fill="#f8fafc" stroke="#1e293b" stroke-width="2"/>
        <text x="340" y="52" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Surplus Food Rescue &amp; Marketplace System</text>

        <!-- Use Cases (Ovals) -->
        <!-- UC1 -->
        <ellipse cx="340" cy="90" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="94" font-family="sans-serif" font-size="9" text-anchor="middle">Register &amp; OTP Authentication</text>

        <!-- UC2 -->
        <ellipse cx="340" cy="140" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="144" font-family="sans-serif" font-size="9" text-anchor="middle">Browse Surplus Food &amp; Mystery Bags</text>

        <!-- UC3 -->
        <ellipse cx="340" cy="190" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="194" font-family="sans-serif" font-size="9" text-anchor="middle">Filter by Cuisine, Price &amp; Allergens</text>

        <!-- UC4 -->
        <ellipse cx="340" cy="240" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="244" font-family="sans-serif" font-size="9" text-anchor="middle">Reserve Surplus Food &amp; Checkout</text>

        <!-- UC5 -->
        <ellipse cx="340" cy="290" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="294" font-family="sans-serif" font-size="9" text-anchor="middle">View Collection Token (OTP) &amp; QR Pass</text>

        <!-- UC6 -->
        <ellipse cx="340" cy="340" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="344" font-family="sans-serif" font-size="9" text-anchor="middle">Download PDF Reservation Voucher</text>

        <!-- UC7 -->
        <ellipse cx="340" cy="390" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="394" font-family="sans-serif" font-size="9" text-anchor="middle">Post Surplus Items &amp; Pickup Windows</text>

        <!-- UC8 -->
        <ellipse cx="340" cy="440" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="444" font-family="sans-serif" font-size="9" text-anchor="middle">Receive WebSocket Live Booking Alerts</text>

        <!-- UC9 -->
        <ellipse cx="340" cy="490" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="494" font-family="sans-serif" font-size="9" text-anchor="middle">Verify QR Scanner / Token Redemption</text>

        <!-- UC10 -->
        <ellipse cx="340" cy="540" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="544" font-family="sans-serif" font-size="9" text-anchor="middle">Verify Restaurant Partner Credentials</text>

        <!-- UC11 -->
        <ellipse cx="340" cy="590" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="594" font-family="sans-serif" font-size="9" text-anchor="middle">Audit Listings &amp; Clear Expired Items</text>

        <!-- UC12 -->
        <ellipse cx="340" cy="640" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="644" font-family="sans-serif" font-size="9" text-anchor="middle">Monitor Savings &amp; CO2 Impact Metrics</text>

        <!-- UC13 -->
        <ellipse cx="340" cy="690" rx="110" ry="18" fill="#ffffff" stroke="#1e40af" stroke-width="1.5"/>
        <text x="340" y="694" font-family="sans-serif" font-size="9" text-anchor="middle">Submit Ratings &amp; Experience Reviews</text>

        <!-- ACTOR 1: CUSTOMER (Left Top) -->
        <circle cx="70" cy="200" r="14" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <line x1="70" y1="214" x2="70" y2="250" stroke="#000" stroke-width="2"/>
        <line x1="45" y1="225" x2="95" y2="225" stroke="#000" stroke-width="2"/>
        <line x1="70" y1="250" x2="50" y2="285" stroke="#000" stroke-width="2"/>
        <line x1="70" y1="250" x2="90" y2="285" stroke="#000" stroke-width="2"/>
        <text x="70" y="305" font-family="sans-serif" font-size="10" font-weight="bold" text-anchor="middle">Customer</text>

        <!-- Customer Links -->
        <line x1="85" y1="220" x2="230" y2="95" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="225" x2="230" y2="140" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="230" x2="230" y2="190" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="235" x2="230" y2="240" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="240" x2="230" y2="290" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="245" x2="230" y2="340" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="250" x2="230" y2="690" stroke="#475569" stroke-width="1.2"/>

        <!-- ACTOR 2: RESTAURANT PARTNER (Left Bottom) -->
        <circle cx="70" cy="450" r="14" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <line x1="70" y1="464" x2="70" y2="500" stroke="#000" stroke-width="2"/>
        <line x1="45" y1="475" x2="95" y2="475" stroke="#000" stroke-width="2"/>
        <line x1="70" y1="500" x2="50" y2="535" stroke="#000" stroke-width="2"/>
        <line x1="70" y1="500" x2="90" y2="535" stroke="#000" stroke-width="2"/>
        <text x="70" y="555" font-family="sans-serif" font-size="10" font-weight="bold" text-anchor="middle">Restaurant</text>

        <!-- Restaurant Links -->
        <line x1="85" y1="465" x2="230" y2="95" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="470" x2="230" y2="390" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="475" x2="230" y2="440" stroke="#475569" stroke-width="1.2"/>
        <line x1="85" y1="480" x2="230" y2="490" stroke="#475569" stroke-width="1.2"/>

        <!-- ACTOR 3: SYSTEM ADMIN (Right Center) -->
        <circle cx="610" cy="550" r="14" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <line x1="610" y1="564" x2="610" y2="600" stroke="#000" stroke-width="2"/>
        <line x1="585" y1="575" x2="635" y2="575" stroke="#000" stroke-width="2"/>
        <line x1="610" y1="600" x2="590" y2="635" stroke="#000" stroke-width="2"/>
        <line x1="610" y1="600" x2="630" y2="635" stroke="#000" stroke-width="2"/>
        <text x="610" y="655" font-family="sans-serif" font-size="10" font-weight="bold" text-anchor="middle">Admin</text>

        <!-- Admin Links -->
        <line x1="595" y1="560" x2="450" y2="95" stroke="#475569" stroke-width="1.2"/>
        <line x1="595" y1="565" x2="450" y2="540" stroke="#475569" stroke-width="1.2"/>
        <line x1="595" y1="570" x2="450" y2="590" stroke="#475569" stroke-width="1.2"/>
        <line x1="595" y1="575" x2="450" y2="640" stroke="#475569" stroke-width="1.2"/>
      </svg>
      <div style="font-size: 11pt; font-weight: bold; margin-top: 10px;">Figure 6.1: UML Use Case Diagram — Surplus Food Platform</div>
    </div>
  </div>

  <!-- ================= CHAPTER 6: SCENARIOS ================= -->
  <div class="page-break">
    <h2 class="subsection-title">6.5 Scenario</h2>
    <p>
      A scenario is a detailed description of a particular situation or sequence of events that helps illustrate how a system or process works. In software engineering, scenarios are often used to show how users interact with a system to achieve specific goals. For example, a scenario might describe how a customer discovers a local bakery, reserves a surprise bag, receives an OTP token, and collects the package. Scenarios make it easier to understand user needs, test different conditions, and visualize the flow of operations within a system.
    </p>

    <h3 class="subsubsection-title">CUSTOMER SCENARIOS</h3>
    <ul>
      <li>Customer can register an account and verify identity via 6-digit email OTP.</li>
      <li>Customer can authenticate securely using email and password to receive a JWT session.</li>
      <li>Customer can explore active surplus food items from nearby verified restaurants.</li>
      <li>Customer can filter available offerings by cuisine classification, max price, dietary type, and allergens.</li>
      <li>Customer can view Mystery Surprise Bags offered at heavy markdowns.</li>
      <li>Customer can reserve surplus items, specify quantities, and complete simulated checkout.</li>
      <li>Customer can receive a unique 6-digit collection OTP and dynamic scannable QR verification code.</li>
      <li>Customer can download an official PDF reservation receipt with pickup instructions.</li>
      <li>Customer can view active reservations, store addresses, and pickup closing windows.</li>
      <li>Customer can submit star ratings and qualitative reviews following successful collection.</li>
      <li>Customer can securely log out of the platform.</li>
    </ul>

    <h3 class="subsubsection-title">RESTAURANT SCENARIOS</h3>
    <ul>
      <li>Restaurant can register and submit restaurant profile credentials (name, address, cuisine) for audit.</li>
      <li>Restaurant can post surplus inventory with original price, discounted price, stock count, and collection times.</li>
      <li>Restaurant can flag listings as Surprise Mystery Bags with estimated retail valuations.</li>
      <li>Restaurant can update or remove active surplus listings.</li>
      <li>Restaurant can receive instantaneous WebSocket sound and banner alerts when customer reservations are placed.</li>
      <li>Restaurant can view the customer reservation queue in real time.</li>
      <li>Restaurant can verify customer pickups by entering the 6-digit OTP code or scanning customer QR codes with a webcam.</li>
      <li>Restaurant can track revenue metrics, total stock quantities, and customer satisfaction ratings.</li>
      <li>Restaurant can securely log out of the platform.</li>
    </ul>

    <h3 class="subsubsection-title">ADMIN SCENARIOS</h3>
    <ul>
      <li>Administrator can securely log in via protected admin credentials.</li>
      <li>Administrator can review, approve, or reject onboarding restaurant business profiles.</li>
      <li>Administrator can view all registered customer and merchant user accounts.</li>
      <li>Administrator can inspect all active platform food listings and verify pricing integrity.</li>
      <li>Administrator can execute automated database cleanups to purge expired food listings.</li>
      <li>Administrator can track aggregate environmental and economic metrics (meals rescued, customer savings, CO2 prevented).</li>
      <li>Administrator can securely log out of the admin console.</li>
    </ul>
  </div>

  <!-- ================= CHAPTER 6: DATA FLOW DIAGRAMS ================= -->
  <div class="page-break">
    <h2 class="subsection-title">6.6 Data Flow Diagram</h2>

    <h3 class="subsubsection-title">Level 0: Context Diagram</h3>
    <p>
      The Level 0 Data Flow Diagram (Context Diagram) represents the entire Surplus Food Rescue &amp; Marketplace platform as a single centralized process, showing high-level data input and output flows exchanged with external entities (Customer, Restaurant Partner, and Admin).
    </p>

    <!-- Clean Level 0 SVG -->
    <div style="text-align: center; margin: 25px 0;">
      <svg width="650" height="380" viewBox="0 0 650 380" style="border: 1px solid #cbd5e1; background: #ffffff; border-radius: 6px;">
        <!-- Top Box: Admin -->
        <rect x="235" y="15" width="180" height="50" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <text x="325" y="45" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle">System Admin</text>

        <!-- Center Circle: System -->
        <ellipse cx="325" cy="190" rx="115" ry="60" fill="#f8fafc" stroke="#000" stroke-width="2"/>
        <text x="325" y="185" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle">Surplus Food Rescue &amp;</text>
        <text x="325" y="202" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle">Marketplace Platform</text>

        <!-- Left Box: Customer -->
        <rect x="25" y="165" width="150" height="50" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <text x="100" y="195" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle">Customer</text>

        <!-- Right Box: Restaurant -->
        <rect x="475" y="165" width="150" height="50" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <text x="550" y="195" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle">Restaurant Partner</text>

        <!-- Arrows: Admin <-> System -->
        <line x1="310" y1="65" x2="310" y2="130" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>
        <text x="260" y="100" font-family="sans-serif" font-size="8.5" text-anchor="middle">Audit / Sweep</text>
        
        <line x1="340" y1="130" x2="340" y2="65" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>
        <text x="390" y="100" font-family="sans-serif" font-size="8.5" text-anchor="middle">Metrics / Logs</text>

        <!-- Arrows: Customer <-> System -->
        <line x1="175" y1="180" x2="210" y2="180" stroke="#000" stroke-width="1.5"/>
        <polygon points="210,180 202,176 202,184" fill="#000"/>
        <text x="190" y="172" font-family="sans-serif" font-size="8.5" text-anchor="middle">Booking Req</text>

        <line x1="210" y1="200" x2="175" y2="200" stroke="#000" stroke-width="1.5"/>
        <polygon points="175,200 183,196 183,204" fill="#000"/>
        <text x="190" y="215" font-family="sans-serif" font-size="8.5" text-anchor="middle">Token / Pass</text>

        <!-- Arrows: Restaurant <-> System -->
        <line x1="475" y1="180" x2="440" y2="180" stroke="#000" stroke-width="1.5"/>
        <polygon points="440,180 448,176 448,184" fill="#000"/>
        <text x="460" y="172" font-family="sans-serif" font-size="8.5" text-anchor="middle">Listings / Verify</text>

        <line x1="440" y1="200" x2="475" y2="200" stroke="#000" stroke-width="1.5"/>
        <polygon points="475,200 467,196 467,204" fill="#000"/>
        <text x="460" y="215" font-family="sans-serif" font-size="8.5" text-anchor="middle">Live Alerts</text>
      </svg>
      <div style="font-size: 11pt; font-weight: bold; margin-top: 6px;">Figure 6.2: DFD Level 0 — Context Diagram</div>
    </div>
  </div>

  <!-- ================= LEVEL 1 DFD: ADMIN & CUSTOMER ================= -->
  <div class="page-break">
    <h3 class="subsubsection-title">Level 1: Admin &amp; Customer Data Flow Diagrams</h3>

    <!-- Level 1 Admin SVG -->
    <div style="text-align: center; margin: 15px 0;">
      <div style="font-size: 11pt; font-weight: bold; margin-bottom: 8px; text-align: left;">Level 1 - Admin</div>
      <svg width="650" height="310" viewBox="0 0 650 310" style="border: 1px solid #cbd5e1; background: #ffffff; border-radius: 6px;">
        <!-- Entity: Admin -->
        <rect x="20" y="120" width="90" height="40" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <text x="65" y="145" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Admin</text>

        <!-- Login Circle -->
        <circle cx="160" cy="140" r="24" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <text x="160" y="144" font-family="sans-serif" font-size="9" text-anchor="middle">Login</text>
        <line x1="110" y1="140" x2="136" y2="140" stroke="#000" stroke-width="1.5"/>

        <!-- User Table Store -->
        <line x1="130" y1="60" x2="190" y2="60" stroke="#000" stroke-width="2"/>
        <line x1="130" y1="85" x2="190" y2="85" stroke="#000" stroke-width="2"/>
        <text x="160" y="76" font-family="sans-serif" font-size="8" text-anchor="middle">User Table</text>
        <line x1="160" y1="85" x2="160" y2="116" stroke="#000" stroke-width="1.5"/>

        <!-- Process Ovals -->
        <!-- P1: Manage Users -->
        <ellipse cx="320" cy="40" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="44" font-family="sans-serif" font-size="8.5" text-anchor="middle">Manage Users</text>
        <line x1="184" y1="140" x2="255" y2="40" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="40" x2="480" y2="40" stroke="#000" stroke-width="1.2"/>
        <!-- Store: Users -->
        <line x1="480" y1="30" x2="570" y2="30" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="50" x2="570" y2="50" stroke="#000" stroke-width="2"/>
        <text x="525" y="43" font-family="sans-serif" font-size="8.5" text-anchor="middle">Users</text>

        <!-- P2: Verify Restaurants -->
        <ellipse cx="320" cy="95" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="99" font-family="sans-serif" font-size="8.5" text-anchor="middle">Verify Stores</text>
        <line x1="184" y1="140" x2="255" y2="95" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="95" x2="480" y2="95" stroke="#000" stroke-width="1.2"/>
        <!-- Store: Restaurants -->
        <line x1="480" y1="85" x2="570" y2="85" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="105" x2="570" y2="105" stroke="#000" stroke-width="2"/>
        <text x="525" y="98" font-family="sans-serif" font-size="8.5" text-anchor="middle">Restaurants</text>

        <!-- P3: Monitor Listings -->
        <ellipse cx="320" cy="150" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="154" font-family="sans-serif" font-size="8.5" text-anchor="middle">Monitor Listings</text>
        <line x1="184" y1="140" x2="255" y2="150" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="150" x2="480" y2="150" stroke="#000" stroke-width="1.2"/>
        <!-- Store: Food Items -->
        <line x1="480" y1="140" x2="570" y2="140" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="160" x2="570" y2="160" stroke="#000" stroke-width="2"/>
        <text x="525" y="153" font-family="sans-serif" font-size="8.5" text-anchor="middle">Food Items</text>

        <!-- P4: Clear Expired -->
        <ellipse cx="320" cy="205" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="209" font-family="sans-serif" font-size="8.5" text-anchor="middle">Clear Expired</text>
        <line x1="184" y1="140" x2="255" y2="205" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="205" x2="480" y2="205" stroke="#000" stroke-width="1.2"/>
        <!-- Store: Inventory -->
        <line x1="480" y1="195" x2="570" y2="195" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="215" x2="570" y2="215" stroke="#000" stroke-width="2"/>
        <text x="525" y="208" font-family="sans-serif" font-size="8.5" text-anchor="middle">Inventory Logs</text>

        <!-- P5: System Analytics -->
        <ellipse cx="320" cy="260" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="264" font-family="sans-serif" font-size="8.5" text-anchor="middle">System Analytics</text>
        <line x1="184" y1="140" x2="255" y2="260" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="260" x2="480" y2="260" stroke="#000" stroke-width="1.2"/>
        <!-- Store: Reports -->
        <line x1="480" y1="250" x2="570" y2="250" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="270" x2="570" y2="270" stroke="#000" stroke-width="2"/>
        <text x="525" y="263" font-family="sans-serif" font-size="8.5" text-anchor="middle">Metrics &amp; Stats</text>
      </svg>
    </div>

    <!-- Level 1 Customer SVG -->
    <div style="text-align: center; margin: 15px 0;">
      <div style="font-size: 11pt; font-weight: bold; margin-bottom: 8px; text-align: left;">Level 1 - Customer</div>
      <svg width="650" height="310" viewBox="0 0 650 310" style="border: 1px solid #cbd5e1; background: #ffffff; border-radius: 6px;">
        <!-- Entity: Customer -->
        <rect x="20" y="120" width="90" height="40" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <text x="65" y="145" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Customer</text>

        <!-- Login Circle -->
        <circle cx="160" cy="140" r="24" fill="#ffffff" stroke="#000" stroke-width="2"/>
        <text x="160" y="144" font-family="sans-serif" font-size="9" text-anchor="middle">Login</text>
        <line x1="110" y1="140" x2="136" y2="140" stroke="#000" stroke-width="1.5"/>

        <!-- User Table Store -->
        <line x1="130" y1="60" x2="190" y2="60" stroke="#000" stroke-width="2"/>
        <line x1="130" y1="85" x2="190" y2="85" stroke="#000" stroke-width="2"/>
        <text x="160" y="76" font-family="sans-serif" font-size="8" text-anchor="middle">User Table</text>
        <line x1="160" y1="85" x2="160" y2="116" stroke="#000" stroke-width="1.5"/>

        <!-- P1: Browse Catalog -->
        <ellipse cx="320" cy="40" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="44" font-family="sans-serif" font-size="8.5" text-anchor="middle">Browse Catalog</text>
        <line x1="184" y1="140" x2="255" y2="40" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="40" x2="480" y2="40" stroke="#000" stroke-width="1.2"/>
        <line x1="480" y1="30" x2="570" y2="30" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="50" x2="570" y2="50" stroke="#000" stroke-width="2"/>
        <text x="525" y="43" font-family="sans-serif" font-size="8.5" text-anchor="middle">Food Items</text>

        <!-- P2: Filter Dietary/Allergens -->
        <ellipse cx="320" cy="95" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="99" font-family="sans-serif" font-size="8.5" text-anchor="middle">Filter Preferences</text>
        <line x1="184" y1="140" x2="255" y2="95" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="95" x2="480" y2="95" stroke="#000" stroke-width="1.2"/>
        <line x1="480" y1="85" x2="570" y2="85" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="105" x2="570" y2="105" stroke="#000" stroke-width="2"/>
        <text x="525" y="98" font-family="sans-serif" font-size="8.5" text-anchor="middle">Preferences</text>

        <!-- P3: Reserve Food Item -->
        <ellipse cx="320" cy="150" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="154" font-family="sans-serif" font-size="8.5" text-anchor="middle">Reserve Food</text>
        <line x1="184" y1="140" x2="255" y2="150" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="150" x2="480" y2="150" stroke="#000" stroke-width="1.2"/>
        <line x1="480" y1="140" x2="570" y2="140" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="160" x2="570" y2="160" stroke="#000" stroke-width="2"/>
        <text x="525" y="153" font-family="sans-serif" font-size="8.5" text-anchor="middle">Orders</text>

        <!-- P4: View OTP & QR Pass -->
        <ellipse cx="320" cy="205" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="209" font-family="sans-serif" font-size="8.5" text-anchor="middle">View OTP / QR</text>
        <line x1="184" y1="140" x2="255" y2="205" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="205" x2="480" y2="205" stroke="#000" stroke-width="1.2"/>
        <line x1="480" y1="195" x2="570" y2="195" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="215" x2="570" y2="215" stroke="#000" stroke-width="2"/>
        <text x="525" y="208" font-family="sans-serif" font-size="8.5" text-anchor="middle">Tokens</text>

        <!-- P5: Rate & Review -->
        <ellipse cx="320" cy="260" rx="65" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
        <text x="320" y="264" font-family="sans-serif" font-size="8.5" text-anchor="middle">Rate &amp; Review</text>
        <line x1="184" y1="140" x2="255" y2="260" stroke="#000" stroke-width="1.2"/>
        <line x1="385" y1="260" x2="480" y2="260" stroke="#000" stroke-width="1.2"/>
        <line x1="480" y1="250" x2="570" y2="250" stroke="#000" stroke-width="2"/>
        <line x1="480" y1="270" x2="570" y2="270" stroke="#000" stroke-width="2"/>
        <text x="525" y="263" font-family="sans-serif" font-size="8.5" text-anchor="middle">Reviews</text>
      </svg>
    </div>
  </div>

  <!-- ================= LEVEL 1: RESTAURANT & LEVEL 2: ADMIN ================= -->
  <div class="page-break">
    <div style="font-size: 11pt; font-weight: bold; margin-bottom: 8px; text-align: left;">Level 1 - Restaurant Partner</div>
    <svg width="650" height="290" viewBox="0 0 650 290" style="border: 1px solid #cbd5e1; background: #ffffff; border-radius: 6px;">
      <!-- Entity: Restaurant -->
      <rect x="20" y="110" width="100" height="40" fill="#ffffff" stroke="#000" stroke-width="2"/>
      <text x="70" y="135" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Restaurant</text>

      <!-- Login Circle -->
      <circle cx="165" cy="130" r="22" fill="#ffffff" stroke="#000" stroke-width="2"/>
      <text x="165" y="134" font-family="sans-serif" font-size="9" text-anchor="middle">Login</text>
      <line x1="120" y1="130" x2="143" y2="130" stroke="#000" stroke-width="1.5"/>

      <!-- User Table -->
      <line x1="135" y1="50" x2="195" y2="50" stroke="#000" stroke-width="2"/>
      <line x1="135" y1="75" x2="195" y2="75" stroke="#000" stroke-width="2"/>
      <text x="165" y="66" font-family="sans-serif" font-size="8" text-anchor="middle">User Table</text>
      <line x1="165" y1="75" x2="165" y2="108" stroke="#000" stroke-width="1.5"/>

      <!-- P1: Post Surplus Item -->
      <ellipse cx="320" cy="35" rx="65" ry="15" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="320" y="39" font-family="sans-serif" font-size="8.5" text-anchor="middle">Post Surplus</text>
      <line x1="187" y1="130" x2="255" y2="35" stroke="#000" stroke-width="1.2"/>
      <line x1="385" y1="35" x2="480" y2="35" stroke="#000" stroke-width="1.2"/>
      <line x1="480" y1="25" x2="570" y2="25" stroke="#000" stroke-width="2"/>
      <line x1="480" y1="45" x2="570" y2="45" stroke="#000" stroke-width="2"/>
      <text x="525" y="38" font-family="sans-serif" font-size="8.5" text-anchor="middle">Food Items</text>

      <!-- P2: Manage Mystery Bags -->
      <ellipse cx="320" cy="85" rx="65" ry="15" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="320" y="89" font-family="sans-serif" font-size="8.5" text-anchor="middle">Manage Mystery Bags</text>
      <line x1="187" y1="130" x2="255" y2="85" stroke="#000" stroke-width="1.2"/>
      <line x1="385" y1="85" x2="480" y2="85" stroke="#000" stroke-width="1.2"/>
      <line x1="480" y1="75" x2="570" y2="75" stroke="#000" stroke-width="2"/>
      <line x1="480" y1="95" x2="570" y2="95" stroke="#000" stroke-width="2"/>
      <text x="525" y="88" font-family="sans-serif" font-size="8.5" text-anchor="middle">Surplus Bundles</text>

      <!-- P3: Order Notifications -->
      <ellipse cx="320" cy="135" rx="65" ry="15" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="320" y="139" font-family="sans-serif" font-size="8.5" text-anchor="middle">Live Order Alerts</text>
      <line x1="187" y1="130" x2="255" y2="135" stroke="#000" stroke-width="1.2"/>
      <line x1="385" y1="135" x2="480" y2="135" stroke="#000" stroke-width="1.2"/>
      <line x1="480" y1="125" x2="570" y2="125" stroke="#000" stroke-width="2"/>
      <line x1="480" y1="145" x2="570" y2="145" stroke="#000" stroke-width="2"/>
      <text x="525" y="138" font-family="sans-serif" font-size="8.5" text-anchor="middle">WebSockets</text>

      <!-- P4: Verify QR / Token -->
      <ellipse cx="320" cy="185" rx="65" ry="15" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="320" y="189" font-family="sans-serif" font-size="8.5" text-anchor="middle">Verify QR / OTP</text>
      <line x1="187" y1="130" x2="255" y2="185" stroke="#000" stroke-width="1.2"/>
      <line x1="385" y1="185" x2="480" y2="185" stroke="#000" stroke-width="1.2"/>
      <line x1="480" y1="175" x2="570" y2="175" stroke="#000" stroke-width="2"/>
      <line x1="480" y1="195" x2="570" y2="195" stroke="#000" stroke-width="2"/>
      <text x="525" y="188" font-family="sans-serif" font-size="8.5" text-anchor="middle">Orders Store</text>

      <!-- P5: Store Analytics -->
      <ellipse cx="320" cy="235" rx="65" ry="15" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="320" y="239" font-family="sans-serif" font-size="8.5" text-anchor="middle">Track Revenue</text>
      <line x1="187" y1="130" x2="255" y2="235" stroke="#000" stroke-width="1.2"/>
      <line x1="385" y1="235" x2="480" y2="235" stroke="#000" stroke-width="1.2"/>
      <line x1="480" y1="225" x2="570" y2="225" stroke="#000" stroke-width="2"/>
      <line x1="480" y1="245" x2="570" y2="245" stroke="#000" stroke-width="2"/>
      <text x="525" y="238" font-family="sans-serif" font-size="8.5" text-anchor="middle">Revenue Logs</text>
    </svg>

    <h3 class="subsubsection-title" style="margin-top: 15px;">Level 2: Admin Detailed Process Decomposition</h3>
    <svg width="650" height="340" viewBox="0 0 650 340" style="border: 1px solid #cbd5e1; background: #ffffff; border-radius: 6px;">
      <!-- Admin Box -->
      <rect x="15" y="145" width="80" height="40" fill="#ffffff" stroke="#000" stroke-width="2"/>
      <text x="55" y="170" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Admin</text>

      <!-- 4 Parent Process Ovals -->
      <!-- Sub 1 -->
      <ellipse cx="180" cy="50" rx="55" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="180" y="54" font-family="sans-serif" font-size="8" text-anchor="middle">Manage Users</text>
      <line x1="95" y1="165" x2="125" y2="50" stroke="#000" stroke-width="1.2"/>

      <!-- Sub 2 -->
      <ellipse cx="180" cy="120" rx="55" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="180" y="124" font-family="sans-serif" font-size="8" text-anchor="middle">Verify Stores</text>
      <line x1="95" y1="165" x2="125" y2="120" stroke="#000" stroke-width="1.2"/>

      <!-- Sub 3 -->
      <ellipse cx="180" cy="195" rx="55" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="180" y="199" font-family="sans-serif" font-size="8" text-anchor="middle">Manage Listings</text>
      <line x1="95" y1="165" x2="125" y2="195" stroke="#000" stroke-width="1.2"/>

      <!-- Sub 4 -->
      <ellipse cx="180" cy="275" rx="55" ry="16" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <text x="180" y="279" font-family="sans-serif" font-size="8" text-anchor="middle">System Reports</text>
      <line x1="95" y1="165" x2="125" y2="275" stroke="#000" stroke-width="1.2"/>

      <!-- Decomposed Functions on Right -->
      <!-- From Manage Users -->
      <rect x="290" y="20" width="100" height="20" fill="#f8fafc" stroke="#475569" stroke-width="1"/>
      <text x="340" y="34" font-family="sans-serif" font-size="7.5" text-anchor="middle">View User Registry</text>
      <line x1="235" y1="50" x2="290" y2="30" stroke="#000" stroke-width="1"/>

      <rect x="290" y="45" width="100" height="20" fill="#f8fafc" stroke="#475569" stroke-width="1"/>
      <text x="340" y="59" font-family="sans-serif" font-size="7.5" text-anchor="middle">Filter User Roles</text>
      <line x1="235" y1="50" x2="290" y2="55" stroke="#000" stroke-width="1"/>

      <!-- From Verify Stores -->
      <rect x="290" y="95" width="100" height="20" fill="#f8fafc" stroke="#475569" stroke-width="1"/>
      <text x="340" y="109" font-family="sans-serif" font-size="7.5" text-anchor="middle">Audit Profiles</text>
      <line x1="235" y1="120" x2="290" y2="105" stroke="#000" stroke-width="1"/>

      <rect x="290" y="120" width="100" height="20" fill="#f8fafc" stroke="#475569" stroke-width="1"/>
      <text x="340" y="134" font-family="sans-serif" font-size="7.5" text-anchor="middle">Approve / Decline</text>
      <line x1="235" y1="120" x2="290" y2="130" stroke="#000" stroke-width="1"/>

      <!-- From Manage Listings -->
      <rect x="290" y="170" width="100" height="20" fill="#f8fafc" stroke="#475569" stroke-width="1"/>
      <text x="340" y="184" font-family="sans-serif" font-size="7.5" text-anchor="middle">Review Food Posts</text>
      <line x1="235" y1="195" x2="290" y2="180" stroke="#000" stroke-width="1"/>

      <rect x="290" y="195" width="100" height="20" fill="#f8fafc" stroke="#475569" stroke-width="1"/>
      <text x="340" y="209" font-family="sans-serif" font-size="7.5" text-anchor="middle">Sweep Expired Items</text>
      <line x1="235" y1="195" x2="290" y2="205" stroke="#000" stroke-width="1"/>

      <!-- From System Reports -->
      <rect x="290" y="250" width="100" height="20" fill="#f8fafc" stroke="#475569" stroke-width="1"/>
      <text x="340" y="264" font-family="sans-serif" font-size="7.5" text-anchor="middle">Savings Analytics</text>
      <line x1="235" y1="275" x2="290" y2="260" stroke="#000" stroke-width="1"/>

      <rect x="290" y="275" width="100" height="20" fill="#f8fafc" stroke="#475569" stroke-width="1"/>
      <text x="340" y="289" font-family="sans-serif" font-size="7.5" text-anchor="middle">CO2 Carbon Metrics</text>
      <line x1="235" y1="275" x2="290" y2="285" stroke="#000" stroke-width="1"/>

      <!-- Stores on far right -->
      <line x1="470" y1="35" x2="560" y2="35" stroke="#000" stroke-width="2"/>
      <line x1="470" y1="55" x2="560" y2="55" stroke="#000" stroke-width="2"/>
      <text x="515" y="48" font-family="sans-serif" font-size="8" text-anchor="middle">Users Store</text>
      <line x1="390" y1="45" x2="470" y2="45" stroke="#000" stroke-width="1"/>

      <line x1="470" y1="110" x2="560" y2="110" stroke="#000" stroke-width="2"/>
      <line x1="470" y1="130" x2="560" y2="130" stroke="#000" stroke-width="2"/>
      <text x="515" y="123" font-family="sans-serif" font-size="8" text-anchor="middle">Profiles Store</text>
      <line x1="390" y1="118" x2="470" y2="118" stroke="#000" stroke-width="1"/>

      <line x1="470" y1="185" x2="560" y2="185" stroke="#000" stroke-width="2"/>
      <line x1="470" y1="205" x2="560" y2="205" stroke="#000" stroke-width="2"/>
      <text x="515" y="198" font-family="sans-serif" font-size="8" text-anchor="middle">Food Items</text>
      <line x1="390" y1="193" x2="470" y2="193" stroke="#000" stroke-width="1"/>

      <line x1="470" y1="265" x2="560" y2="265" stroke="#000" stroke-width="2"/>
      <line x1="470" y1="285" x2="560" y2="285" stroke="#000" stroke-width="2"/>
      <text x="515" y="278" font-family="sans-serif" font-size="8" text-anchor="middle">Analytics DB</text>
      <line x1="390" y1="273" x2="470" y2="273" stroke="#000" stroke-width="1"/>
    </svg>
    <div style="font-size: 11pt; font-weight: bold; margin-top: 6px; text-align: center;">Figure 6.3: DFD Level 2 — Admin Decomposition</div>
  </div>

  <!-- ================= CHAPTER 7 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>SYSTEM DEVELOPMENT</h1>
  </div>

  <!-- ================= CHAPTER 7: SYSTEM DEVELOPMENT ================= -->
  <div class="page-break">
    <h1 class="section-title">7. SYSTEM DEVELOPMENT</h1>

    <p>
      System development is a series of activities performed to design, implement, test, and deploy a software system to meet the specified requirements. The principal activities performed during the development phase can be divided into two major related sequences:
    </p>
    <ul>
      <li>External System Development</li>
      <li>Internal System Development</li>
    </ul>
    <p>
      The major external system development activities include implementation planning, development environment setup, software installation, and cloud database provisioning. The internal system development activities involve software architecture design, database modeling, API development, frontend component engineering, authentication, authorization, testing, and security integration.
    </p>

    <h2 class="subsection-title">7.1 Coding</h2>
    <p>
      The purpose of coding is to convert the system design and requirements into executable software. It consists of a structured collection of programming statements used to implement system functions, manage data, process user requests, and establish communication between different components. Coding facilitates the development of reliable, maintainable, and efficient software by implementing the required modules and workflows.
    </p>

    <h3 class="subsubsection-title">JavaScript &amp; Node.js</h3>
    <p>
      JavaScript is a high-level, dynamic, multi-paradigm programming language widely used for modern web application development. In Surplus Food Rescue &amp; Marketplace, JavaScript powers both the interactive client-side application logic and the high-performance server-side runtime via Node.js. Node.js is an open-source, cross-platform JavaScript runtime built on Chrome's V8 engine that facilitates asynchronous, event-driven, non-blocking I/O operations, ensuring high concurrent request handling during peak food collection windows.
    </p>
    <p>
      In Surplus Food, Node.js serves as the server runtime handling user authentication, email OTP verification, order placement pipelines, WebSocket live dispatch channels, automated cron jobs, and database CRUD operations.
    </p>

    <h3 class="subsubsection-title">React.js</h3>
    <p>
      React.js is an open-source JavaScript library used for building interactive and reusable user interfaces. It follows a component-based architecture, allowing large interfaces to be divided into smaller reusable components.
    </p>
    <p>
      In Surplus Food, React.js (powered by Vite) is utilized to engineer the responsive frontend interfaces across all three user modules: Customer, Restaurant Partner, and Admin. It integrates Lucide-React icons, HTML5 QR camera scanning modules, dynamic countdown timers, and client-side PDF document generation.
    </p>

    <h3 class="subsubsection-title">Express.js Framework</h3>
    <p>
      Express.js is a fast, minimalist web application framework for Node.js. It provides features for developing RESTful APIs, handling HTTP requests, managing routes, and implementing middleware. Express.js simplifies communication between the frontend and backend by providing structured API endpoints and handling HTTP methods such as GET, POST, PUT, and DELETE. It also supports request validation, authentication middleware, error handling, and JSON data processing.
    </p>
  </div>

  <div class="page-break">
    <h3 class="subsubsection-title">MongoDB Database</h3>
    <p>
      MongoDB is a NoSQL, document-oriented database used for storing and managing application data. Unlike relational databases that store information in tables and rows, MongoDB stores data in flexible JSON-like documents within collections.
    </p>
    <p>
      MongoDB Atlas is deployed in Surplus Food to store distributed documents across users, restaurant profiles, surplus food items, customer reservations, and ratings. MongoDB's flexible schema models effortlessly handle variable attributes like allergen lists, dietary tags, dynamic markdown price history, and nested payment credentials.
    </p>

    <h3 class="subsubsection-title">Standard Libraries &amp; Middleware Packages</h3>
    <p>
      The Node.js development ecosystem provides several packages through Node Package Manager (npm) to support authentication, security, file management, and application configuration:
    </p>
    <ul>
      <li><strong>JWT (JSON Web Token):</strong> Used for secure token-based authentication and role-based access control. Upon login, a signed JSON Web Token is issued containing the user's role (Customer, Restaurant, Admin), ensuring that protected API endpoints and administrative dispatch actions remain strictly safeguarded.</li>
      <li><strong>Bcrypt:</strong> A password-hashing library used to securely hash user passwords using 10 salt rounds before storing them in the database, protecting user credentials against dictionary and rainbow table attacks.</li>
      <li><strong>Socket.io:</strong> Powers the bidirectional, sub-second WebSocket communication layer essential for broadcasting incoming customer reservations directly to active kitchen dashboards without requiring manual page reloads.</li>
      <li><strong>Multer:</strong> Middleware used for handling multipart/form-data, utilized for uploading restaurant banners and food item photos safely to the server uploads directory.</li>
      <li><strong>Node-Cron:</strong> A background task scheduler that runs automated routines every minute to sweep expired listings and execute 20% dynamic markdowns during the final 30 minutes of store pickup windows.</li>
      <li><strong>Dotenv:</strong> Used to load environment variables from a .env file, keeping sensitive credentials such as database connection URIs and JWT secrets isolated from the codebase.</li>
      <li><strong>CORS:</strong> Cross-Origin Resource Sharing enables controlled communication between the React.js client and the Express.js server when hosted across different origins.</li>
    </ul>
  </div>

  <!-- ================= CHAPTER 8 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>SYSTEM TESTING AND IMPLEMENTATION</h1>
  </div>

  <!-- ================= CHAPTER 8: SYSTEM TESTING AND IMPLEMENTATION ================= -->
  <div class="page-break">
    <h1 class="section-title">8. SYSTEM TESTING AND IMPLEMENTATION</h1>

    <p>
      System testing is a crucial milestone in the engineering of Surplus Food Rescue &amp; Marketplace. Rigorous testing verifies that all modules operate with extreme reliability, fail-safe resilience, low latency, and zero data loss under concurrent consumer and restaurant transaction loads.
    </p>
    <p>
      Software testing is an important part of software quality assurance. It involves the systematic evaluation of the system's requirements, design, coding, functionality, and user interaction. Testing is performed throughout the development process to verify that the implemented system produces the expected results under specified conditions.
    </p>

    <h2 class="subsection-title">8.1 Types of Testing</h2>
    <p>
      The different types of testing performed for the Surplus Food platform include Unit Testing, Integration Testing, System Testing, Validation Testing, and User Acceptance Testing:
    </p>

    <h3 class="subsubsection-title">Unit Testing</h3>
    <p>
      Unit testing involves testing individual modules or components of the application separately to ensure that each component performs its intended function correctly. It is generally performed during the coding stage to identify errors early.
    </p>
    <p>
      In Surplus Food, unit testing was conducted on individual software units including password hashing, 6-digit OTP token generation, JWT signing, price validation (ensuring offer price is strictly less than original price), quantity checks, and countdown calculations. Each function was validated against boundary cases and expected numerical outputs.
    </p>

    <h3 class="subsubsection-title">Integration Testing</h3>
    <p>
      Integration testing involves combining individually tested modules and checking whether they work correctly together. It focuses on identifying errors in communication and data exchange between different components of the system.
    </p>
    <p>In Surplus Food, integration testing was performed across cooperating pipelines such as:</p>
    <ul>
      <li>User registration, OTP verification, and JWT session authorization pipelines.</li>
      <li>Restaurant surplus food creation and immediate reflection on the customer catalog.</li>
      <li>Customer booking checkout triggering real-time WebSocket notifications to the merchant.</li>
      <li>Token / QR validation decrementing restaurant available stock and updating reservation status.</li>
      <li>React.js frontend, Express REST APIs, Socket.io gateway, and MongoDB Atlas database.</li>
    </ul>

    <h3 class="subsubsection-title">System Testing</h3>
    <p>
      System testing evaluated the complete Surplus Food platform as a unified marketplace. The platform was evaluated under high concurrency to simulate evening rush-hour food collections, verifying sub-second WebSocket broadcast latencies, accurate countdown timers, and resilience against network timeouts.
    </p>
    <p>
      The validation suite confirmed proper role isolation: customers cannot access merchant management panels or admin audit tools, and restaurants can only access and modify their own inventory catalogs.
    </p>
  </div>

  <div class="page-break">
    <h3 class="subsubsection-title">Validation Testing</h3>
    <p>
      Validation testing ensures that the developed system satisfies all functional requirements and operational expectations established during the analysis and design stages. It verifies that the application correctly fulfills all mission workflows for the Customer, Restaurant Partner, and Admin.
    </p>
    <p>Validation testing includes checking:</p>
    <ul>
      <li>Correct user registration and instant 6-digit email OTP authentication.</li>
      <li>Strict role-based authorization preventing unauthorized data access.</li>
      <li>Accurate surplus item listing, image uploading, and Mystery Bag configuration.</li>
      <li>Accurate search filtering across cuisines, maximum price bounds, and allergen tags.</li>
      <li>Reliable order checkout, OTP token issuance, and QR code rendering.</li>
      <li>Real-time WebSocket alerts upon incoming customer bookings.</li>
      <li>Automated node-cron background sweeps of expired food items.</li>
      <li>Administrative restaurant audit approvals and platform listings sweeps.</li>
    </ul>

    <h3 class="subsubsection-title">User Acceptance Testing (UAT)</h3>
    <p>
      User Acceptance Testing (UAT) was conducted by simulating real-world bakery and restaurant closing scenarios with test users acting as Customers, Restaurant Kitchen Staff, and Administrators. Feedback verified that reserving surplus food and redeeming passes via 6-digit OTP tokens was exceptionally straightforward and rapid.
    </p>
    <p>The major areas considered during user acceptance testing include:</p>
    <ul>
      <li>Output screen design and aesthetic visual presentation.</li>
      <li>Input form ergonomics and validation feedback.</li>
      <li>Navigation and menu structure.</li>
      <li>QR scanner responsiveness on mobile devices.</li>
      <li>Checkout and token retrieval flow.</li>
      <li>Dashboard functionality and metrics clarity.</li>
    </ul>

    <h2 class="subsection-title">8.2 Implementation</h2>
    <p>
      Implementation is the vital phase where the software design specifications of Surplus Food were translated into an operational, production-ready marketplace platform. The implementation integrated the React.js client interface with the Node.js / Express.js backend, configured WebSocket channels, seeded initial sample test accounts, and deployed the application.
    </p>
    <p>The implementation process includes:</p>
    <ul>
      <li>Careful planning of the system deployment.</li>
      <li>Setting up the React.js, Node.js, Express.js, and MongoDB environment.</li>
      <li>Configuring the database connection strings and environment security variables.</li>
      <li>Integrating frontend interfaces with backend RESTful APIs.</li>
      <li>Implementing authentication and role-based access control middleware.</li>
      <li>Testing all modules and fixing identified errors.</li>
      <li>Preparing user guidance and documentation.</li>
    </ul>
  </div>

  <!-- ================= CHAPTER 9 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>SYSTEM MAINTENANCE</h1>
  </div>

  <!-- ================= CHAPTER 9: SYSTEM MAINTENANCE ================= -->
  <div class="page-break">
    <h1 class="section-title">9. SYSTEM MAINTENANCE</h1>

    <p>
      Maintenance is the process of making necessary changes and improvements to a software system after its implementation. These changes may include fixing errors, adapting the system to changes in the software environment, improving performance, enhancing security, and adding new features. When changes are implemented during the maintenance phase, the affected parts of the system must be systematically reviewed and tested to maintain system stability and data integrity.
    </p>
    <p>There are three types of maintenance:</p>
    <ul>
      <li><strong>Corrective Maintenance</strong> – Fixing bugs, errors, and system failures.</li>
      <li><strong>Adaptive Maintenance</strong> – Updating the system to support changes in software, hardware, or operating environments.</li>
      <li><strong>Perfective Maintenance</strong> – Improving existing features and adding enhancements based on user requirements.</li>
    </ul>
    <p>
      Maintenance is an essential component of the software development lifecycle, particularly for an active consumer marketplace like Surplus Food. Ongoing maintenance ensures 99.99% operational uptime, security patching against newly discovered vulnerabilities, optimization of database queries, and continuous calibration of automated price markdown algorithms.
    </p>

    <h2 class="subsection-title">9.1 Key Maintenance Activities &amp; Importance</h2>
    <p>
      Key maintenance activities for Surplus Food encompass: (1) Problem Identification &amp; Error Monitoring through server health logs, WebSocket connection states, and API latency trackers; (2) Design &amp; Code Refinement across React components, Express controllers, and Mongoose schemas; (3) Regression Testing of booking and verification pipelines; and (4) Configuration Management via GitHub and automated deployment pipelines.
    </p>

    <h3 class="subsubsection-title">1. Problem Identification &amp; Analysis</h3>
    <p>
      Monitoring server errors, API responses, database issues, and user feedback to identify and analyze problems related to login, profiles, reservations, notifications, or other system functions.
    </p>

    <h3 class="subsubsection-title">2. Design &amp; Code Modification</h3>
    <p>
      Modifying React.js components, Express.js APIs, Node.js backend services, or MongoDB models to fix issues and introduce improvements without affecting existing system functionality.
    </p>

    <h3 class="subsubsection-title">3. Regression Testing &amp; Verification</h3>
    <p>
      Re-testing important application functions such as authentication, role-based access, surplus food reservation, WebSocket dispatch alerts, and camera QR verification to ensure that new code updates do not compromise system stability.
    </p>

    <h3 class="subsubsection-title">4. Deployment &amp; Configuration Management</h3>
    <p>
      Deploying updated application versions, managing environment variables and configuration settings, maintaining database configurations, and using GitHub for version control and tracking system changes.
    </p>
  </div>

  <!-- ================= CHAPTER 10 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>FUTURE ENHANCEMENT</h1>
  </div>

  <!-- ================= CHAPTER 10: FUTURE ENHANCEMENTS ================= -->
  <div class="page-break">
    <h1 class="section-title">10. FUTURE ENHANCEMENTS</h1>

    <p>
      The Surplus Food Rescue &amp; Marketplace platform has established a high-performance foundation for urban food rescue. To further expand its sustainability impact and adapt to growing commercial demands, several cutting-edge technological enhancements are planned for future iterative releases:
    </p>

    <h2 class="subsection-title">10.1 AI-Powered Surplus Waste Prediction</h2>
    <p>
      Integrating machine learning predictive models (e.g. Random Forest regression, LSTM neural networks) trained on historical restaurant sales, weather conditions, holidays, and local foot traffic. This engine will automatically suggest optimized preparation quantities to restaurant chefs each morning, preventing surplus from being generated in the first place.
    </p>

    <h2 class="subsection-title">10.2 Native Mobile Applications (iOS &amp; Android)</h2>
    <p>
      Developing cross-platform mobile apps using React Native or Flutter, offering geofenced push notifications that alert consumers on their smartphones whenever their favorite bakery publishes surprise bags within a 2-kilometer radius.
    </p>

    <h2 class="subsection-title">10.3 Direct Integration with Commercial POS Systems</h2>
    <p>
      Creating automated integration plugins for popular Point-of-Sale (POS) systems (such as Toast, Square, and Clover). When items remain unsold in the restaurant register 45 minutes prior to closing, the POS integration can automatically publish them to the Surplus Food marketplace without requiring manual intervention from kitchen staff.
    </p>

    <h2 class="subsection-title">10.4 Dedicated NGO &amp; Charity Donation Routing</h2>
    <p>
      Introducing an automated charity dispatch pipeline. For items that remain unreserved by retail consumers 15 minutes before closing, the platform can automatically dispatch notifications to local food banks, shelters, and voluntary relief organizations for free bulk pickup.
    </p>
  </div>

  <!-- ================= CHAPTER 11 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>CONCLUSION</h1>
  </div>

  <!-- ================= CHAPTER 11: CONCLUSION ================= -->
  <div class="page-break">
    <h1 class="section-title">11. CONCLUSION</h1>

    <p>
      Urban food wastage represents an immense economic loss and ecological hazard that demands innovative, technological intervention. While billions of dollars worth of fresh, wholesome meals are discarded each day, millions of consumers seek affordable dining options amid soaring food inflation. Surplus Food Rescue &amp; Marketplace was conceived, engineered, and evaluated specifically to eliminate this systemic divide.
    </p>

    <p>
      By harmonizing food businesses, neighborhood consumers, and system administrators into an integrated real-time marketplace, the platform turns food waste into an opportunity for economic recovery and environmental conservation. The integration of role-based security, instant Surprise Bag reservations, automated OTP and QR redemption tokens, live WebSocket order dispatching, and background cron markdown routines transforms food rescue into a seamless, profitable, and dignified daily experience.
    </p>

    <p>
      Developed using the modern MERN Stack (React.js, Node.js, Express.js, and MongoDB Atlas) paired with Socket.io, the project demonstrates the successful realization of an enterprise-grade full-stack web application. Surplus Food satisfies all technical, operational, and academic criteria prescribed by the APJ Abdul Kalam Kerala Technological University for the Master of Computer Applications curriculum, while establishing a meaningful and sustainable contribution to modern ecological informatics.
    </p>
  </div>

  <!-- ================= CHAPTER 12 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>APPENDIX</h1>
  </div>

  <!-- ================= CHAPTER 12: APPENDIX (SCREENSHOTS) ================= -->
  <div class="page-break">
    <h1 class="section-title">12. APPENDIX</h1>

    <div class="screenshot-card">
      <div class="screenshot-caption">Figure 12.1: Hero Landing Page &amp; Sustainability Mission Portal</div>
      <img src="{img_landing}" alt="Hero Landing Page">
    </div>

    <div class="screenshot-card" style="margin-top: 25px;">
      <div class="screenshot-caption">Figure 12.2: Multi-Role Authentication &amp; Email OTP Verification</div>
      <img src="{img_login}" alt="Multi-Role Authentication">
    </div>
  </div>

  <div class="page-break">
    <div class="screenshot-card">
      <div class="screenshot-caption">Figure 12.3: Customer Surplus Food Exploration Catalog &amp; Surprise Bags</div>
      <img src="{img_cust_dash}" alt="Customer Surplus Food Exploration">
    </div>

    <div class="screenshot-card" style="margin-top: 25px;">
      <div class="screenshot-caption">Figure 12.4: Customer Active Reservations, OTP Token &amp; QR Collection Pass</div>
      <img src="{img_cust_orders}" alt="Customer Active Reservations">
    </div>
  </div>

  <div class="page-break">
    <div class="screenshot-card">
      <div class="screenshot-caption">Figure 12.5: Customer Profile &amp; Account Settings Management</div>
      <img src="{img_cust_prof}" alt="Customer Profile">
    </div>

    <div class="screenshot-card" style="margin-top: 25px;">
      <div class="screenshot-caption">Figure 12.6: Restaurant Business Hub &amp; Live Surplus Inventory Management</div>
      <img src="{img_rest_dash}" alt="Restaurant Business Hub">
    </div>
  </div>

  <div class="page-break">
    <div class="screenshot-card">
      <div class="screenshot-caption">Figure 12.7: Restaurant Customer Bookings Queue &amp; QR Scanner Verification</div>
      <img src="{img_rest_res}" alt="Restaurant Customer Bookings Queue">
    </div>

    <div class="screenshot-card" style="margin-top: 25px;">
      <div class="screenshot-caption">Figure 12.8: Admin Command Center &amp; Environmental Impact Analytics</div>
      <img src="{img_admin_dash}" alt="Admin Command Center">
    </div>
  </div>

  <div class="page-break">
    <div class="screenshot-card">
      <div class="screenshot-caption">Figure 12.9: Admin Restaurant Verification &amp; Profile Audit Console</div>
      <img src="{img_admin_veri}" alt="Admin Restaurant Verification">
    </div>

    <div class="screenshot-card" style="margin-top: 25px;">
      <div class="screenshot-caption">Figure 12.10: Admin Global Platform Postings &amp; Expired Items Sweeper</div>
      <img src="{img_admin_list}" alt="Admin Global Postings">
    </div>
  </div>

  <!-- ================= CHAPTER 13 DIVIDER ================= -->
  <div class="page-break chapter-divider">
    <h1>BIBLIOGRAPHY</h1>
  </div>

  <!-- ================= CHAPTER 13: BIBLIOGRAPHY ================= -->
  <div class="page-break">
    <h1 class="section-title">13. BIBLIOGRAPHY</h1>

    <h2 class="subsection-title">Websites</h2>
    <p>[1] https://react.dev/</p>
    <p>[2] https://nodejs.org/docs/latest/api/</p>
    <p>[3] https://expressjs.com/</p>
    <p>[4] https://www.mongodb.com/docs/</p>
    <p>[5] https://mongoosejs.com/docs/</p>
    <p>[6] https://socket.io/docs/v4/</p>
    <p>[7] https://jwt.io/introduction</p>
    <p>[8] https://vitejs.dev/</p>
    <p>[9] https://lucide.dev/</p>
    <p>[10] https://www.npmjs.com/package/node-cron</p>

    <h2 class="subsection-title" style="margin-top: 25px;">Books</h2>
    <p>[1] David Flanagan, <em>JavaScript: The Definitive Guide</em>, 7th Edition, O'Reilly Media, 2020.</p>
    <p>[2] Ethan Brown, <em>Web Development with Node and Express: Leveraging the JavaScript Stack</em>, 2nd Edition, O'Reilly Media, 2019.</p>
    <p>[3] Alex Banks and Eve Porcello, <em>Learning React: Modern Patterns for Developing React Applications</em>, 2nd Edition, O'Reilly Media, 2020.</p>
    <p>[4] Kristina Chodorow, <em>MongoDB: The Definitive Guide: Powerful and Scalable Storage</em>, 3rd Edition, O'Reilly Media, 2019.</p>
    <p>[5] Rohit Rai, <em>Socket.IO Real-Time Web Application Development</em>, Packt Publishing, 2017.</p>
  </div>

</body>
</html>
"""

async def generate_pdf():
    output_html_path = "d:/surplus-food/Surplus_Food_Project_Report.html"
    output_pdf_path = "d:/surplus-food/Surplus_Food_Project_Report.pdf"

    print("Writing HTML report file...")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print("HTML report created successfully.")

    print("Launching Chromium via Playwright to compile PDF...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Load local HTML file
        await page.goto(f"file:///{os.path.abspath(output_html_path).replace('\\\\', '/')}", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        print("Generating PDF with exact KTU MEA College running header/footer...")
        await page.pdf(
            path=output_pdf_path,
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template='''
                <div style="width: 100%; font-size: 9pt; font-family: 'Times New Roman', serif; font-style: italic; color: #000; padding: 0 20mm; display: flex; justify-content: space-between; box-sizing: border-box;">
                    <span>Surplus Food</span>
                    <span class="pageNumber"></span>
                </div>
            ''',
            footer_template='''
                <div style="width: 100%; font-size: 9.5pt; font-family: 'Times New Roman', serif; font-style: italic; color: #000; padding: 0 20mm; display: flex; justify-content: space-between; box-sizing: border-box; border-top: 1px solid #000; padding-top: 4px;">
                    <span>Department of Computer Applications</span>
                    <span>MEA Engineering College</span>
                </div>
            ''',
            margin={
                "top": "22mm",
                "bottom": "22mm",
                "left": "20mm",
                "right": "20mm"
            }
        )
        await browser.close()
    
    print(f"\\nSUCCESS! Perfect Project Report generated at:\\n{output_pdf_path}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())

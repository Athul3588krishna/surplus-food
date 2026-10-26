import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("d:/surplus-food/diagrams", exist_ok=True)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def create_dfd_level_0():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Central Process Circle
    circle = patches.Circle((50, 50), 16, edgecolor="#1e3a8a", facecolor="#eff6ff", linewidth=2.5)
    ax.add_patch(circle)
    ax.text(50, 53, "0.0", fontsize=14, fontweight='bold', ha='center', va='center', color="#1e3a8a")
    ax.text(50, 47, "Surplus Food\nRescue System", fontsize=12, fontweight='bold', ha='center', va='center', color="#0f172a")

    # Entities (Rectangles)
    # 1. Customer (Top Left)
    cust_rect = patches.FancyBboxPatch((6, 68), 24, 18, boxstyle="square,pad=0", edgecolor="#0284c7", facecolor="#ffffff", linewidth=2)
    ax.add_patch(cust_rect)
    ax.text(18, 77, "CUSTOMER", fontsize=12, fontweight='bold', ha='center', va='center', color="#0284c7")

    # 2. Restaurant Partner (Top Right)
    rest_rect = patches.FancyBboxPatch((70, 68), 24, 18, boxstyle="square,pad=0", edgecolor="#16a34a", facecolor="#ffffff", linewidth=2)
    ax.add_patch(rest_rect)
    ax.text(82, 77, "RESTAURANT\nPARTNER", fontsize=11, fontweight='bold', ha='center', va='center', color="#16a34a")

    # 3. System Administrator (Bottom Center)
    admin_rect = patches.FancyBboxPatch((38, 6), 24, 16, boxstyle="square,pad=0", edgecolor="#dc2626", facecolor="#ffffff", linewidth=2)
    ax.add_patch(admin_rect)
    ax.text(50, 14, "SYSTEM\nADMINISTRATOR", fontsize=11, fontweight='bold', ha='center', va='center', color="#dc2626")

    # Data Flows (Arrows and Labels)
    # Customer -> System: Search, Food Reservation, OTP Request
    ax.annotate("", xy=(36, 58), xytext=(24, 68),
                arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.6))
    ax.text(23, 60, "Orders, Payment, OTP", fontsize=8.5, fontweight='bold', ha='center', color="#1e293b", rotation=25)

    # System -> Customer: Food Catalog, OTP Token, QR Pass
    ax.annotate("", xy=(28, 70), xytext=(38, 62),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.6))
    ax.text(39, 70, "Food Catalog, QR Receipt", fontsize=8.5, fontweight='bold', ha='center', color="#0284c7", rotation=25)

    # Restaurant -> System: Surplus Listings, Pricing, OTP Validation
    ax.annotate("", xy=(64, 58), xytext=(74, 68),
                arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.6))
    ax.text(77, 60, "Food Items, QR Verification", fontsize=8.5, fontweight='bold', ha='center', color="#1e293b", rotation=-25)

    # System -> Restaurant: Live Orders, Order Confirmation, Sales Reports
    ax.annotate("", xy=(72, 70), xytext=(62, 62),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.6))
    ax.text(61, 70, "Live Orders, Payouts", fontsize=8.5, fontweight='bold', ha='center', color="#16a34a", rotation=-25)

    # Admin -> System: Restaurant Approvals, System Config
    ax.annotate("", xy=(46, 34), xytext=(46, 22),
                arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.6))
    ax.text(37, 28, "Approvals, Sweeps", fontsize=8.5, fontweight='bold', ha='center', color="#1e293b", rotation=90)

    # System -> Admin: Revenue Analytics, Impact Reports
    ax.annotate("", xy=(54, 22), xytext=(54, 34),
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.6))
    ax.text(63, 28, "Analytics, Reports", fontsize=8.5, fontweight='bold', ha='center', color="#dc2626", rotation=-90)

    plt.tight_layout()
    plt.savefig("d:/surplus-food/diagrams/dfd_level_0.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("DFD Level 0 generated.")

def create_dfd_level_1_admin():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Entity: Admin
    admin_rect = patches.FancyBboxPatch((4, 42), 18, 16, boxstyle="square,pad=0", edgecolor="#dc2626", facecolor="#ffffff", linewidth=2)
    ax.add_patch(admin_rect)
    ax.text(13, 50, "ADMINISTRATOR", fontsize=9.5, fontweight='bold', ha='center', va='center', color="#dc2626")

    # Processes
    procs = [
        ("1.1", "Authenticate\nAdmin", 82),
        ("1.2", "Verify Restaurant\nProfiles", 60),
        ("1.3", "Manage Food\nListings", 38),
        ("1.4", "Generate Reports\n& Analytics", 16)
    ]
    for pid, pname, y in procs:
        c = patches.Circle((42, y), 8, edgecolor="#1e3a8a", facecolor="#eff6ff", linewidth=1.8)
        ax.add_patch(c)
        ax.text(42, y + 2, pid, fontsize=9, fontweight='bold', ha='center', color="#1e3a8a")
        ax.text(42, y - 2, pname, fontsize=7.5, fontweight='bold', ha='center', va='center', color="#0f172a")

        # Arrow Admin -> Process
        ax.annotate("", xy=(34, y), xytext=(22, 50),
                    arrowprops=dict(arrowstyle="->", color="#475569", lw=1.3))

    # Data Stores (Open-ended boxes)
    stores = [
        ("D1: Users Collection", 82),
        ("D2: RestaurantProfiles", 60),
        ("D3: FoodItems Collection", 38),
        ("D4: Orders Collection", 16)
    ]
    for sname, y in stores:
        # Top and bottom line of open box
        ax.plot([68, 96], [y + 4, y + 4], color="#0f172a", lw=1.6)
        ax.plot([68, 96], [y - 4, y - 4], color="#0f172a", lw=1.6)
        ax.plot([68, 68], [y - 4, y + 4], color="#0f172a", lw=1.6)
        ax.text(82, y, sname, fontsize=8.5, fontweight='bold', ha='center', va='center', color="#0f172a")

        # Arrow Process <-> Store
        ax.annotate("", xy=(68, y), xytext=(50, y),
                    arrowprops=dict(arrowstyle="<->", color="#0284c7", lw=1.4))

    plt.tight_layout()
    plt.savefig("d:/surplus-food/diagrams/dfd_level_1_admin.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("DFD Level 1 Admin generated.")

def create_dfd_level_1_customer():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Entity: Customer
    cust_rect = patches.FancyBboxPatch((4, 42), 18, 16, boxstyle="square,pad=0", edgecolor="#0284c7", facecolor="#ffffff", linewidth=2)
    ax.add_patch(cust_rect)
    ax.text(13, 50, "CUSTOMER", fontsize=10.5, fontweight='bold', ha='center', va='center', color="#0284c7")

    # Processes
    procs = [
        ("2.1", "Register & Email\nOTP Verification", 82),
        ("2.2", "Search & Browse\nSurplus Listings", 60),
        ("2.3", "Reserve Items &\nCheckout", 38),
        ("2.4", "Collect Food &\nSubmit Review", 16)
    ]
    for pid, pname, y in procs:
        c = patches.Circle((42, y), 8, edgecolor="#0284c7", facecolor="#f0f9ff", linewidth=1.8)
        ax.add_patch(c)
        ax.text(42, y + 2, pid, fontsize=9, fontweight='bold', ha='center', color="#0284c7")
        ax.text(42, y - 2, pname, fontsize=7.5, fontweight='bold', ha='center', va='center', color="#0f172a")

        ax.annotate("", xy=(34, y), xytext=(22, 50),
                    arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.3))

    # Stores
    stores = [
        ("D1: Users Collection", 82),
        ("D3: FoodItems Collection", 60),
        ("D4: Orders Collection", 38),
        ("D5: Reviews Collection", 16)
    ]
    for sname, y in stores:
        ax.plot([68, 96], [y + 4, y + 4], color="#0f172a", lw=1.6)
        ax.plot([68, 96], [y - 4, y - 4], color="#0f172a", lw=1.6)
        ax.plot([68, 68], [y - 4, y + 4], color="#0f172a", lw=1.6)
        ax.text(82, y, sname, fontsize=8.5, fontweight='bold', ha='center', va='center', color="#0f172a")

        ax.annotate("", xy=(68, y), xytext=(50, y),
                    arrowprops=dict(arrowstyle="<->", color="#16a34a", lw=1.4))

    plt.tight_layout()
    plt.savefig("d:/surplus-food/diagrams/dfd_level_1_customer.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("DFD Level 1 Customer generated.")

def create_dfd_level_1_restaurant():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Entity: Restaurant
    rest_rect = patches.FancyBboxPatch((4, 42), 18, 16, boxstyle="square,pad=0", edgecolor="#16a34a", facecolor="#ffffff", linewidth=2)
    ax.add_patch(rest_rect)
    ax.text(13, 50, "RESTAURANT\nPARTNER", fontsize=10, fontweight='bold', ha='center', va='center', color="#16a34a")

    # Processes
    procs = [
        ("3.1", "Store Profile\nManagement", 82),
        ("3.2", "Post Surplus Food\n& Mystery Bags", 60),
        ("3.3", "Live Order Queue\n(WebSocket)", 38),
        ("3.4", "Verify Pickup\n(OTP / QR Scan)", 16)
    ]
    for pid, pname, y in procs:
        c = patches.Circle((42, y), 8, edgecolor="#16a34a", facecolor="#f0fdf4", linewidth=1.8)
        ax.add_patch(c)
        ax.text(42, y + 2, pid, fontsize=9, fontweight='bold', ha='center', color="#16a34a")
        ax.text(42, y - 2, pname, fontsize=7.5, fontweight='bold', ha='center', va='center', color="#0f172a")

        ax.annotate("", xy=(34, y), xytext=(22, 50),
                    arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.3))

    # Stores
    stores = [
        ("D2: RestaurantProfiles", 82),
        ("D3: FoodItems Collection", 60),
        ("D4: Orders Collection", 38),
        ("D4: Orders (Update Status)", 16)
    ]
    for sname, y in stores:
        ax.plot([68, 96], [y + 4, y + 4], color="#0f172a", lw=1.6)
        ax.plot([68, 96], [y - 4, y - 4], color="#0f172a", lw=1.6)
        ax.plot([68, 68], [y - 4, y + 4], color="#0f172a", lw=1.6)
        ax.text(82, y, sname, fontsize=8.5, fontweight='bold', ha='center', va='center', color="#0f172a")

        ax.annotate("", xy=(68, y), xytext=(50, y),
                    arrowprops=dict(arrowstyle="<->", color="#0284c7", lw=1.4))

    plt.tight_layout()
    plt.savefig("d:/surplus-food/diagrams/dfd_level_1_restaurant.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("DFD Level 1 Restaurant generated.")

def create_dfd_level_2_admin():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Entity: Admin
    admin_rect = patches.FancyBboxPatch((4, 42), 18, 16, boxstyle="square,pad=0", edgecolor="#dc2626", facecolor="#ffffff", linewidth=2)
    ax.add_patch(admin_rect)
    ax.text(13, 50, "ADMINISTRATOR", fontsize=10, fontweight='bold', ha='center', va='center', color="#dc2626")

    # Detailed Sub-processes of 1.2 & 1.3
    subprocs = [
        ("1.2.1", "Audit Restaurant\nDocuments", 86),
        ("1.2.2", "Approve / Reject\nAccount", 68),
        ("1.3.1", "Monitor Food\nCatalog Listings", 50),
        ("1.3.2", "Trigger Expired\nItems Sweeper", 32),
        ("1.4.1", "Calculate Meals\n& CO2 Metrics", 14)
    ]
    for pid, pname, y in subprocs:
        c = patches.Circle((42, y), 7.5, edgecolor="#dc2626", facecolor="#fef2f2", linewidth=1.8)
        ax.add_patch(c)
        ax.text(42, y + 2, pid, fontsize=8.5, fontweight='bold', ha='center', color="#dc2626")
        ax.text(42, y - 2, pname, fontsize=7.2, fontweight='bold', ha='center', va='center', color="#0f172a")

        ax.annotate("", xy=(34.5, y), xytext=(22, 50),
                    arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.3))

    # Stores
    substores = [
        ("D2: RestaurantProfiles", 86),
        ("D1: Users (isVerified flag)", 68),
        ("D3: FoodItems Collection", 50),
        ("D3: FoodItems (Status purge)", 32),
        ("D4: Orders & Impact Ledger", 14)
    ]
    for sname, y in substores:
        ax.plot([68, 96], [y + 4, y + 4], color="#0f172a", lw=1.6)
        ax.plot([68, 96], [y - 4, y - 4], color="#0f172a", lw=1.6)
        ax.plot([68, 68], [y - 4, y + 4], color="#0f172a", lw=1.6)
        ax.text(82, y, sname, fontsize=8, fontweight='bold', ha='center', va='center', color="#0f172a")

        ax.annotate("", xy=(68, y), xytext=(49.5, y),
                    arrowprops=dict(arrowstyle="<->", color="#2563eb", lw=1.4))

    plt.tight_layout()
    plt.savefig("d:/surplus-food/diagrams/dfd_level_2_admin.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("DFD Level 2 Admin generated.")

create_dfd_level_0()
create_dfd_level_1_admin()
create_dfd_level_1_customer()
create_dfd_level_1_restaurant()
create_dfd_level_2_admin()

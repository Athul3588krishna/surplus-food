import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("d:/surplus-food/diagrams", exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def create_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 16), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # System boundary box
    sys_rect = patches.FancyBboxPatch((28, 4), 44, 91, boxstyle="round,pad=1", edgecolor="#1e3a8a", facecolor="#f8fafc", linewidth=2.5, linestyle="--")
    ax.add_patch(sys_rect)
    ax.text(50, 93, "Surplus Food Rescue & Marketplace", fontsize=15, fontweight='bold', ha='center', color="#1e3a8a")

    # Use Cases (Ellipses)
    use_cases = [
        # (id, name, y_pos)
        (1, "User Registration & Email OTP", 88),
        (2, "Secure Multi-Role Login (JWT)", 81),
        (3, "Browse & Filter Surplus Food", 74),
        (4, "View & Reserve Mystery Bags", 67),
        (5, "Simulated Checkout & Payment", 60),
        (6, "Generate 6-Digit OTP & QR Pass", 53),
        (7, "Manage Restaurant Profile", 46),
        (8, "Post Surplus Inventory & Pricing", 39),
        (9, "Real-Time Order Alert (Socket.io)", 32),
        (10, "Validate Pickup via QR Scanner/OTP", 25),
        (11, "Verify / Reject Restaurant Partners", 18),
        (12, "Audit Listings & Auto-Expiry Sweep", 11),
        (13, "Track Revenue & Impact Analytics", 6),
    ]

    uc_centers = {}
    for uid, name, y in use_cases:
        ellipse = patches.Ellipse((50, y), 38, 4.8, edgecolor="#2563eb", facecolor="#ffffff", linewidth=1.8)
        ax.add_patch(ellipse)
        ax.text(50, y, name, fontsize=10, fontweight='bold', ha='center', va='center', color="#0f172a")
        uc_centers[uid] = (50, y)

    # Helper for Stickman Actor
    def draw_actor(x, y, label, color="#0f172a"):
        # Head
        ax.add_patch(patches.Circle((x, y + 4.5), 1.5, edgecolor=color, facecolor="#ffffff", linewidth=2))
        # Torso
        ax.plot([x, x], [y + 3, y - 1], color=color, linewidth=2.2)
        # Arms
        ax.plot([x - 2.8, x + 2.8], [y + 1.8, y + 1.8], color=color, linewidth=2.2)
        # Legs
        ax.plot([x, x - 2.2], [y - 1, y - 4.5], color=color, linewidth=2.2)
        ax.plot([x, x + 2.2], [y - 1, y - 4.5], color=color, linewidth=2.2)
        # Label
        ax.text(x, y - 6.5, label, fontsize=11, fontweight='bold', ha='center', color=color)

    # Actors
    draw_actor(12, 70, "Customer\n(Consumer)", "#0284c7")
    draw_actor(88, 50, "Restaurant\nPartner", "#16a34a")
    draw_actor(12, 22, "System\nAdministrator", "#dc2626")

    # Actor connections to Use Cases
    # Customer connections (1, 2, 3, 4, 5, 6)
    customer_pos = (12, 70)
    for target in [1, 2, 3, 4, 5, 6]:
        ax.annotate("", xy=(31, uc_centers[target][1]), xytext=(15, customer_pos[1]),
                    arrowprops=dict(arrowstyle="-", color="#0284c7", lw=1.4))

    # Restaurant connections (1, 2, 7, 8, 9, 10)
    rest_pos = (88, 50)
    for target in [1, 2, 7, 8, 9, 10]:
        ax.annotate("", xy=(69, uc_centers[target][1]), xytext=(85, rest_pos[1]),
                    arrowprops=dict(arrowstyle="-", color="#16a34a", lw=1.4))

    # Admin connections (2, 11, 12, 13)
    admin_pos = (12, 22)
    for target in [2, 11, 12, 13]:
        ax.annotate("", xy=(31, uc_centers[target][1]), xytext=(15, admin_pos[1]),
                    arrowprops=dict(arrowstyle="-", color="#dc2626", lw=1.4))

    plt.tight_layout()
    plt.savefig("d:/surplus-food/diagrams/use_case_diagram.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Use case diagram generated successfully.")

create_use_case_diagram()

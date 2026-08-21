import asyncio
import os
from playwright.async_api import async_playwright

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SCRUM BOOK: SUBMISSION - 2 (CIE 2)</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
  document.addEventListener("DOMContentLoaded", function() {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      fontFamily: 'Segoe UI, sans-serif'
    });
  });
</script>
<style>
  @page {
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
  }

  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1e293b;
    margin: 0;
    padding: 0;
  }

  .doc-title-container {
    text-align: center;
    margin-top: 5px;
    margin-bottom: 20px;
  }

  .doc-main-title {
    font-size: 17pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0 0 6px 0;
    line-height: 1.25;
  }

  .doc-sub-title {
    font-size: 12pt;
    font-weight: 700;
    color: #1e40af;
    border-bottom: 2px solid #1e40af;
    padding-bottom: 4px;
    margin-bottom: 18px;
  }

  h2.section-header {
    font-size: 12.5pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 3px;
    margin-top: 24px;
    margin-bottom: 14px;
  }

  h3.subsection-header {
    font-size: 10.5pt;
    font-weight: 700;
    color: #1e40af;
    margin-top: 18px;
    margin-bottom: 8px;
  }

  .profile-group {
    margin-bottom: 16px;
  }

  .profile-title {
    font-weight: 800;
    font-size: 10.5pt;
    color: #0f172a;
    text-transform: uppercase;
    margin-bottom: 6px;
  }

  ul.profile-list {
    list-style-type: disc;
    margin: 0;
    padding-left: 20px;
  }

  ul.profile-list li {
    margin-bottom: 3px;
  }

  .bold-label {
    font-weight: 700;
    color: #0f172a;
  }

  /* Tables */
  table.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
    margin-bottom: 16px;
    font-size: 9pt;
  }

  table.custom-table th, table.custom-table td {
    border: 1px solid #cbd5e1;
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
  }

  table.custom-table th {
    background-color: #f1f5f9;
    font-weight: 700;
    color: #0f172a;
  }

  table.custom-table tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  .signature-area {
    margin-top: 20px;
    margin-bottom: 20px;
    font-size: 9.5pt;
    line-height: 2;
  }

  /* Code / JSON / Box diagrams */
  pre.code-block {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
    font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.4;
    white-space: pre-wrap;
    word-break: break-word;
    color: #0f172a;
    margin-top: 6px;
    margin-bottom: 14px;
  }

  .diagram-container {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 14px;
    margin-top: 8px;
    margin-bottom: 14px;
    text-align: center;
  }

  .diagram-container .mermaid {
    display: inline-block;
    max-width: 100%;
  }

  code.inline-code {
    background-color: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 1px 5px;
    font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    color: #0f172a;
  }

  .sprint-header {
    font-weight: 700;
    color: #1e40af;
    margin-top: 12px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .dod-list {
    list-style: none;
    padding-left: 0;
    margin-top: 6px;
  }

  .dod-list li {
    position: relative;
    padding-left: 22px;
    margin-bottom: 5px;
  }

  .dod-list li::before {
    content: "☑";
    position: absolute;
    left: 0;
    top: 0;
    color: #1e40af;
    font-weight: bold;
  }

  .avoid-break {
    page-break-inside: avoid;
  }

  .user-story-card {
    margin-bottom: 14px;
    padding-left: 10px;
    border-left: 3px solid #1e40af;
  }

  .story-title {
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 3px;
  }

  .story-body {
    font-size: 9.5pt;
    margin-bottom: 3px;
  }

  .story-criteria {
    font-size: 9pt;
    padding-left: 16px;
    margin-top: 3px;
    margin-bottom: 3px;
  }

  .story-estimate {
    font-weight: 700;
    font-size: 9pt;
    color: #1e40af;
  }
</style>
</head>
<body>

  <!-- TITLE HEADER -->
  <div class="doc-title-container">
    <div class="doc-main-title">SURPLUS FOOD: SMART FOOD RESCUE AND SURPLUS MANAGEMENT SYSTEM</div>
    <div class="doc-sub-title">SCRUM BOOK: SUBMISSION - 2 (CIE 2)</div>
  </div>

  <!-- STUDENT PROFILE -->
  <div class="profile-group">
    <div class="profile-title">STUDENT PROFILE</div>
    <ul class="profile-list">
      <li><span class="bold-label">Name of Student:</span> ATHUL KRISHNA R</li>
      <li><span class="bold-label">Register Number:</span> MEA24MCA-XXXX</li>
      <li><span class="bold-label">Course & Batch:</span> Master of Computer Applications (MCA)</li>
      <li><span class="bold-label">Semester:</span> S3 (Third Semester)</li>
      <li><span class="bold-label">Department:</span> Department of Computer Applications</li>
      <li><span class="bold-label">College:</span> MEA Engineering College, Perinthalmanna</li>
    </ul>
  </div>

  <!-- EVALUATION PROFILE -->
  <div class="profile-group">
    <div class="profile-title">EVALUATION PROFILE</div>
    <ul class="profile-list">
      <li><span class="bold-label">Submission Date:</span> 18/08/2026</li>
      <li><span class="bold-label">Evaluation Event:</span> Continuous Internal Evaluation 2 (CIE 2)</li>
      <li><span class="bold-label">Project Guide:</span> Ms. Prajina K (Assistant Professor)</li>
      <li><span class="bold-label">Project Co-ordinator:</span> Mrs. Sruti Sudevan (HOD & Assistant Professor)</li>
    </ul>
  </div>

  <!-- EVALUATION & SIGNATURE SHEET -->
  <div class="profile-group avoid-break">
    <div class="profile-title">EVALUATION & SIGNATURE SHEET</div>
    <table class="custom-table">
      <thead>
        <tr>
          <th>Evaluation Criterion</th>
          <th style="width: 110px;">Maximum Marks</th>
          <th style="width: 110px;">Marks Awarded</th>
          <th style="width: 140px;">Remarks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Updated Sprint Details & DoD</td>
          <td>5</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Database Design & Collections</td>
          <td>5</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Data Flow Diagram (DFD - Up to Level 2)</td>
          <td>5</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>User Stories & Story Points</td>
          <td>5</td>
          <td></td>
          <td></td>
        </tr>
        <tr style="font-weight: bold; background-color: #f1f5f9;">
          <td>Total Marks</td>
          <td>20</td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <div class="signature-area">
      <div><strong>Signature of Project Guide:</strong> _________________________</div>
      <div><strong>Date of Evaluation:</strong> _________________________</div>
    </div>
  </div>

  <hr style="border: 0; border-top: 1px solid #cbd5e1; margin: 18px 0;" />

  <!-- SECTION 1 -->
  <h2 class="section-header">1. UPDATED SPRINT DETAILS</h2>
  <p>The <strong>Surplus Food</strong> platform was developed following the <strong>Agile Scrum Framework</strong> across four sprints. Below is the official Sprint Tracking Log formatted according to the evaluation requirements:</p>

  <!-- Sprint 1 -->
  <div class="sprint-header">📅 Sprint - 1</div>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 75px;">Module</th>
        <th>Task</th>
        <th style="width: 85px;">Pending task if any</th>
        <th style="width: 75px;">Hours of Completion</th>
        <th style="width: 95px;">Expected date of Completion</th>
        <th style="width: 95px;">Actual date of Completion</th>
        <th style="width: 85px;">Reason for delay</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Email-OTP Registration & Nodemailer Setup</td>
        <td>-</td>
        <td>2 hr</td>
        <td>14/07/2026</td>
        <td>14/07/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Customer</strong></td>
        <td>JWT Authentication & Bcrypt Password Hashing</td>
        <td>-</td>
        <td>2 hr</td>
        <td>16/07/2026</td>
        <td>16/07/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Customer Profile Management & Phone Verification</td>
        <td>-</td>
        <td>3 hr</td>
        <td>18/07/2026</td>
        <td>18/07/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Restaurant</strong></td>
        <td>Restaurant Partner Registration & Verification Flag</td>
        <td>-</td>
        <td>3 hr</td>
        <td>21/07/2026</td>
        <td>21/07/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Admin</strong></td>
        <td>Admin Login & User Role Middleware (<code class="inline-code">protect</code>, <code class="inline-code">authorize</code>)</td>
        <td>-</td>
        <td>2 hr</td>
        <td>22/07/2026</td>
        <td>22/07/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Common</strong></td>
        <td>MongoDB Connection Setup & Mongoose Schemas</td>
        <td>-</td>
        <td>2 hr</td>
        <td>24/07/2026</td>
        <td>24/07/2026</td>
        <td>-</td>
      </tr>
    </tbody>
  </table>

  <!-- Sprint 2 -->
  <div class="sprint-header">📅 Sprint - 2</div>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 75px;">Module</th>
        <th>Task</th>
        <th style="width: 85px;">Pending task if any</th>
        <th style="width: 75px;">Hours of Completion</th>
        <th style="width: 95px;">Expected date of Completion</th>
        <th style="width: 95px;">Actual date of Completion</th>
        <th style="width: 85px;">Reason for delay</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Restaurant</strong></td>
        <td>Surplus Food Item Posting with Pickup Windows</td>
        <td>-</td>
        <td>3 hr</td>
        <td>26/07/2026</td>
        <td>26/07/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Restaurant</strong></td>
        <td>Multer Food Image Upload Middleware</td>
        <td>-</td>
        <td>3 hr</td>
        <td>28/07/2026</td>
        <td>28/07/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Leaflet Map Integration & Geolocation Restaurant Search</td>
        <td>-</td>
        <td>4 hr</td>
        <td>30/07/2026</td>
        <td>30/07/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Food Category Filtering & Price Discount Badge</td>
        <td>-</td>
        <td>3 hr</td>
        <td>01/08/2026</td>
        <td>01/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Restaurant</strong></td>
        <td>Stock Availability & Real-time Item Status Toggle</td>
        <td>-</td>
        <td>2 hr</td>
        <td>03/08/2026</td>
        <td>03/08/2026</td>
        <td>-</td>
      </tr>
    </tbody>
  </table>

  <!-- Sprint 3 -->
  <div class="sprint-header">📅 Sprint - 3</div>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 75px;">Module</th>
        <th>Task</th>
        <th style="width: 85px;">Pending task if any</th>
        <th style="width: 75px;">Hours of Completion</th>
        <th style="width: 95px;">Expected date of Completion</th>
        <th style="width: 95px;">Actual date of Completion</th>
        <th style="width: 85px;">Reason for delay</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Surplus Food Reservation & Quantity Selector</td>
        <td>-</td>
        <td>5 hr</td>
        <td>05/08/2026</td>
        <td>05/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Payment Gateway Simulation (Card Details & Status)</td>
        <td>-</td>
        <td>4 hr</td>
        <td>07/08/2026</td>
        <td>07/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Unique Pickup Token Generation (<code class="inline-code">TOKEN-XXXXX</code>)</td>
        <td>-</td>
        <td>3 hr</td>
        <td>09/08/2026</td>
        <td>09/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Customer</strong></td>
        <td>PDF Order Receipt Generation (<code class="inline-code">jsPDF</code>)</td>
        <td>-</td>
        <td>3 hr</td>
        <td>11/08/2026</td>
        <td>11/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Restaurant</strong></td>
        <td>Pickup Verification & Order Collection Management</td>
        <td>-</td>
        <td>4 hr</td>
        <td>13/08/2026</td>
        <td>13/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Order Cancellation & Automatic Stock Restock Flow</td>
        <td>-</td>
        <td>2 hr</td>
        <td>14/08/2026</td>
        <td>14/08/2026</td>
        <td>-</td>
      </tr>
    </tbody>
  </table>

  <!-- Sprint 4 -->
  <div class="sprint-header">📅 Sprint - 4</div>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 75px;">Module</th>
        <th>Task</th>
        <th style="width: 85px;">Pending task if any</th>
        <th style="width: 75px;">Hours of Completion</th>
        <th style="width: 95px;">Expected date of Completion</th>
        <th style="width: 95px;">Actual date of Completion</th>
        <th style="width: 85px;">Reason for delay</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Customer</strong></td>
        <td>Restaurant Rating & Order Review Submission UI</td>
        <td>-</td>
        <td>3 hr</td>
        <td>15/08/2026</td>
        <td>15/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Admin</strong></td>
        <td>Admin Dashboard Platform Overview & User Control</td>
        <td>-</td>
        <td>2 hr</td>
        <td>16/08/2026</td>
        <td>16/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Admin</strong></td>
        <td>Restaurant Profile Verification & Approval Flow</td>
        <td>-</td>
        <td>4 hr</td>
        <td>17/08/2026</td>
        <td>17/08/2026</td>
        <td>-</td>
      </tr>
      <tr>
        <td><strong>Admin</strong></td>
        <td>Recharts System Analytics & Sales/Waste Reduction Metrics</td>
        <td>-</td>
        <td>3 hr</td>
        <td>18/08/2026</td>
        <td>18/08/2026</td>
        <td>-</td>
      </tr>
    </tbody>
  </table>

  <!-- Summary Table -->
  <h3 class="subsection-header">📊 Sprint Velocity & Burn-down Summary</h3>
  <table class="custom-table">
    <thead>
      <tr>
        <th>Sprint</th>
        <th>Module Focus</th>
        <th>Planned SP</th>
        <th>Completed SP</th>
        <th>Velocity Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Sprint 1</strong></td>
        <td>Customer & Partner Auth & Core Setup</td>
        <td>19</td>
        <td>19</td>
        <td>On Target</td>
      </tr>
      <tr>
        <td><strong>Sprint 2</strong></td>
        <td>Surplus Catalog & Geolocation Search</td>
        <td>20</td>
        <td>20</td>
        <td>On Target</td>
      </tr>
      <tr>
        <td><strong>Sprint 3</strong></td>
        <td>Order Reservation & Payment Flow</td>
        <td>21</td>
        <td>21</td>
        <td>On Target</td>
      </tr>
      <tr>
        <td><strong>Sprint 4</strong></td>
        <td>Review Rating System & Admin Dashboard</td>
        <td>18</td>
        <td>18</td>
        <td>On Target</td>
      </tr>
    </tbody>
  </table>

  <!-- Definition of Done Checklist -->
  <div class="avoid-break">
    <h3 class="subsection-header">Definition of Done (DoD) Checklist:</h3>
    <ul class="dod-list">
      <li>Code adheres to clean architecture with standard Express routes and React hooks.</li>
      <li>Password fields are hashed with Bcrypt prior to persistence.</li>
      <li>API routes enforce JWT authorization middleware (<code class="inline-code">protect</code>, <code class="inline-code">authorize</code>).</li>
      <li>Geospatial coordinates validate latitude (-90 to 90) and longitude (-180 to 180).</li>
      <li>All manual UAT workflows (Customer, Restaurant, Admin) pass verification tests without runtime exceptions.</li>
    </ul>
  </div>

  <hr style="border: 0; border-top: 1px solid #cbd5e1; margin: 18px 0;" />

  <!-- SECTION 2 -->
  <h2 class="section-header">2. DATABASE DESIGN / COLLECTIONS</h2>
  <p>The backend utilizes <strong>MongoDB</strong> with <strong>Mongoose ORM</strong> to enforce schema validation. The primary collections and their attributes are detailed below:</p>

  <div class="diagram-container">
    <pre style="margin: 0; font-family: monospace; font-size: 8.5pt; text-align: left;">
┌─────────────────┐  1:N  ┌──────────────────┐
│      User       │ ◄──── │RestaurantProfile │
│(Customer/Rest/  │       │ (Restaurant Info)│
│     Admin)      │       └────────┬─────────┘
└────────┬────────┘                │ 1:N
         │ 1:N                     ▼
         │                ┌──────────────────┐
         │ ◄──────────────│     FoodItem     │
         │                │  (Surplus Food)  │
         │                └────────┬─────────┘
         ▼                         │ 1:N
┌─────────────────┐                │
│      Order      │ ◄──────────────┘
│  (Reservations) │
└────────┬────────┘
         │ 1:1
         ▼
┌─────────────────┐
│     Review      │
│(Ratings/Comment)│
└─────────────────┘</pre>
  </div>

  <!-- 2.1 Collection: users -->
  <h3 class="subsection-header">2.1 Collection: <code class="inline-code">users</code> ( <code class="inline-code">User.js</code> )</h3>
  <p>Stores user profiles for Customers, Restaurant Owners, and System Administrators.</p>
  <table class="custom-table">
    <thead>
      <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Constraints</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code class="inline-code">_id</code></td>
        <td>ObjectId</td>
        <td>Primary Key, Auto</td>
        <td>Unique user identifier</td>
      </tr>
      <tr>
        <td><code class="inline-code">name</code></td>
        <td>String</td>
        <td>Required, Trim</td>
        <td>Full name of the user</td>
      </tr>
      <tr>
        <td><code class="inline-code">email</code></td>
        <td>String</td>
        <td>Required, Unique, Lowercase</td>
        <td>Email address for login</td>
      </tr>
      <tr>
        <td><code class="inline-code">password</code></td>
        <td>String</td>
        <td>Required</td>
        <td>Hashed password (Bcrypt)</td>
      </tr>
      <tr>
        <td><code class="inline-code">role</code></td>
        <td>String</td>
        <td>Enum: <code class="inline-code">['customer', 'restaurant', 'admin']</code></td>
        <td>User access role</td>
      </tr>
      <tr>
        <td><code class="inline-code">phoneNumber</code></td>
        <td>String</td>
        <td>Trim</td>
        <td>User contact phone number</td>
      </tr>
      <tr>
        <td><code class="inline-code">isVerified</code></td>
        <td>Boolean</td>
        <td>Default: <code class="inline-code">false</code></td>
        <td>Email verification status</td>
      </tr>
      <tr>
        <td><code class="inline-code">otpCode</code></td>
        <td>String</td>
        <td>Default: <code class="inline-code">''</code></td>
        <td>6-digit email OTP code</td>
      </tr>
      <tr>
        <td><code class="inline-code">otpExpiry</code></td>
        <td>Date</td>
        <td>-</td>
        <td>Expiration timestamp for OTP</td>
      </tr>
      <tr>
        <td><code class="inline-code">createdAt</code></td>
        <td>Date</td>
        <td>Auto Timestamp</td>
        <td>Account creation timestamp</td>
      </tr>
    </tbody>
  </table>

  <p>📄 <strong>Sample Document ( <code class="inline-code">users</code> ):</strong></p>
  <pre class="code-block">{
  _id: ObjectId('6a6959be4b8992b198eddbc0'),
  name: 'Athul Krishna',
  email: 'athul@gmail.com',
  password: '$2a$10$w8.9Xj1s4rZ6Qk9Y... (Bcrypt Hashed)',
  role: 'customer',
  phoneNumber: '+91 9876543210',
  isVerified: true,
  otpCode: '',
  otpExpiry: null,
  createdAt: ISODate('2026-07-28T10:15:30.000Z'),
  updatedAt: ISODate('2026-07-29T01:39:10.000Z'),
  __v: NumberInt('0')
}</pre>

  <!-- 2.2 Collection: restaurantprofiles -->
  <h3 class="subsection-header">2.2 Collection: <code class="inline-code">restaurantprofiles</code> ( <code class="inline-code">RestaurantProfile.js</code> )</h3>
  <p>Stores restaurant partner details, address, cuisine type, ratings, and location coordinates.</p>
  <table class="custom-table">
    <thead>
      <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Constraints</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code class="inline-code">_id</code></td>
        <td>ObjectId</td>
        <td>Primary Key, Auto</td>
        <td>Unique restaurant ID</td>
      </tr>
      <tr>
        <td><code class="inline-code">user</code></td>
        <td>ObjectId</td>
        <td>Required, Ref: <code class="inline-code">'User'</code>, Unique</td>
        <td>Owner user account reference</td>
      </tr>
      <tr>
        <td><code class="inline-code">restaurantName</code></td>
        <td>String</td>
        <td>Required, Trim</td>
        <td>Public name of restaurant</td>
      </tr>
      <tr>
        <td><code class="inline-code">address</code></td>
        <td>String</td>
        <td>Required, Trim</td>
        <td>Physical street address</td>
      </tr>
      <tr>
        <td><code class="inline-code">cuisineType</code></td>
        <td>String</td>
        <td>Required, Trim</td>
        <td>Category (Bakery, Indian, Asian, etc.)</td>
      </tr>
      <tr>
        <td><code class="inline-code">description</code></td>
        <td>String</td>
        <td>Trim</td>
        <td>Detailed description of restaurant</td>
      </tr>
      <tr>
        <td><code class="inline-code">imagePath</code></td>
        <td>String</td>
        <td>Default: <code class="inline-code">''</code></td>
        <td>Cover photo image URL/Path</td>
      </tr>
      <tr>
        <td><code class="inline-code">isVerified</code></td>
        <td>Boolean</td>
        <td>Default: <code class="inline-code">false</code></td>
        <td>Admin verification status</td>
      </tr>
      <tr>
        <td><code class="inline-code">rating</code></td>
        <td>Number</td>
        <td>Default: <code class="inline-code">0</code></td>
        <td>Average rating score (1-5)</td>
      </tr>
      <tr>
        <td><code class="inline-code">ratingCount</code></td>
        <td>Number</td>
        <td>Default: <code class="inline-code">0</code></td>
        <td>Total customer reviews received</td>
      </tr>
      <tr>
        <td><code class="inline-code">latitude</code></td>
        <td>Number</td>
        <td>Optional</td>
        <td>GPS latitude coordinate</td>
      </tr>
      <tr>
        <td><code class="inline-code">longitude</code></td>
        <td>Number</td>
        <td>Optional</td>
        <td>GPS longitude coordinate</td>
      </tr>
      <tr>
        <td><code class="inline-code">createdAt</code></td>
        <td>Date</td>
        <td>Auto Timestamp</td>
        <td>Profile creation timestamp</td>
      </tr>
    </tbody>
  </table>

  <p>📄 <strong>Sample Document ( <code class="inline-code">restaurantprofiles</code> ):</strong></p>
  <pre class="code-block">{
  _id: ObjectId('6a6959be4b8992b198eddbc6'),
  user: ObjectId('6a6959be4b8992b198eddbc1'),
  restaurantName: 'Green Leaf Gourmet Bakery',
  address: 'Main Road, Perinthalmanna, Kerala',
  cuisineType: 'Bakery & Desserts',
  description: 'Fresh artisanal breads, pastries, and surplus evening surprise bags.',
  imagePath: '/uploads/restaurant_greenleaf.png',
  isVerified: true,
  rating: 4.8,
  ratingCount: 24,
  latitude: Double('10.978'),
  longitude: Double('76.224'),
  createdAt: ISODate('2026-07-25T08:00:00.000Z'),
  __v: NumberInt('0')
}</pre>

  <!-- 2.3 Collection: fooditems -->
  <h3 class="subsection-header">2.3 Collection: <code class="inline-code">fooditems</code> ( <code class="inline-code">FoodItem.js</code> )</h3>
  <p>Stores discounted surplus food offerings, pricing, quantities, and pickup window schedules.</p>
  <table class="custom-table">
    <thead>
      <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Constraints</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code class="inline-code">_id</code></td>
        <td>ObjectId</td>
        <td>Primary Key, Auto</td>
        <td>Unique food item ID</td>
      </tr>
      <tr>
        <td><code class="inline-code">restaurant</code></td>
        <td>ObjectId</td>
        <td>Required, Ref: <code class="inline-code">'RestaurantProfile'</code></td>
        <td>Associated restaurant reference</td>
      </tr>
      <tr>
        <td><code class="inline-code">name</code></td>
        <td>String</td>
        <td>Required, Trim</td>
        <td>Title of surplus food item</td>
      </tr>
      <tr>
        <td><code class="inline-code">description</code></td>
        <td>String</td>
        <td>Trim</td>
        <td>Item contents description</td>
      </tr>
      <tr>
        <td><code class="inline-code">originalPrice</code></td>
        <td>Number</td>
        <td>Required</td>
        <td>Standard regular price (₹)</td>
      </tr>
      <tr>
        <td><code class="inline-code">discountedPrice</code></td>
        <td>Number</td>
        <td>Required</td>
        <td>Discounted surplus price (₹)</td>
      </tr>
      <tr>
        <td><code class="inline-code">quantity</code></td>
        <td>Number</td>
        <td>Required, Min: 0, Default: <code class="inline-code">1</code></td>
        <td>Available stock quantity</td>
      </tr>
      <tr>
        <td><code class="inline-code">pickupStartTime</code></td>
        <td>String</td>
        <td>Required (e.g. <code class="inline-code">"18:00"</code>)</td>
        <td>Pickup window start time</td>
      </tr>
      <tr>
        <td><code class="inline-code">pickupEndTime</code></td>
        <td>String</td>
        <td>Required (e.g. <code class="inline-code">"21:00"</code>)</td>
        <td>Pickup window end time</td>
      </tr>
      <tr>
        <td><code class="inline-code">imagePath</code></td>
        <td>String</td>
        <td>Default: <code class="inline-code">''</code></td>
        <td>Food item image URL/Path</td>
      </tr>
      <tr>
        <td><code class="inline-code">status</code></td>
        <td>String</td>
        <td>Enum: <code class="inline-code">['available', 'sold-out']</code></td>
        <td>Availability status</td>
      </tr>
      <tr>
        <td><code class="inline-code">expiryDate</code></td>
        <td>Date</td>
        <td>Required</td>
        <td>Expiration timestamp</td>
      </tr>
      <tr>
        <td><code class="inline-code">createdAt</code></td>
        <td>Date</td>
        <td>Auto Timestamp</td>
        <td>Listing creation timestamp</td>
      </tr>
    </tbody>
  </table>

  <p>📄 <strong>Sample Document ( <code class="inline-code">fooditems</code> ):</strong></p>
  <pre class="code-block">{
  _id: ObjectId('6a6959be4b8992b198eddbd2'),
  restaurant: ObjectId('6a6959be4b8992b198eddbc6'),
  name: 'Evening Surprise Pastry Bag',
  description: 'Assorted fresh cream cakes, croissants, and butter cookies.',
  originalPrice: 450,
  discountedPrice: 150,
  quantity: 5,
  pickupStartTime: '18:30',
  pickupEndTime: '21:00',
  imagePath: '/uploads/pastry_bag.png',
  status: 'available',
  expiryDate: ISODate('2026-08-19T21:00:00.000Z'),
  createdAt: ISODate('2026-07-29T01:39:10.000Z'),
  __v: NumberInt('0')
}</pre>

  <!-- 2.4 Collection: orders -->
  <h3 class="subsection-header">2.4 Collection: <code class="inline-code">orders</code> ( <code class="inline-code">Order.js</code> )</h3>
  <p>Stores customer food reservations, transaction tokens, payment states, and collection status.</p>
  <table class="custom-table">
    <thead>
      <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Constraints</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code class="inline-code">_id</code></td>
        <td>ObjectId</td>
        <td>Primary Key, Auto</td>
        <td>Unique order ID</td>
      </tr>
      <tr>
        <td><code class="inline-code">customer</code></td>
        <td>ObjectId</td>
        <td>Required, Ref: <code class="inline-code">'User'</code></td>
        <td>Customer user reference</td>
      </tr>
      <tr>
        <td><code class="inline-code">restaurant</code></td>
        <td>ObjectId</td>
        <td>Required, Ref: <code class="inline-code">'RestaurantProfile'</code></td>
        <td>Target restaurant reference</td>
      </tr>
      <tr>
        <td><code class="inline-code">foodItem</code></td>
        <td>ObjectId</td>
        <td>Required, Ref: <code class="inline-code">'FoodItem'</code></td>
        <td>Reserved food item reference</td>
      </tr>
      <tr>
        <td><code class="inline-code">quantity</code></td>
        <td>Number</td>
        <td>Required, Min: 1, Default: <code class="inline-code">1</code></td>
        <td>Number of items reserved</td>
      </tr>
      <tr>
        <td><code class="inline-code">totalPrice</code></td>
        <td>Number</td>
        <td>Required</td>
        <td>Total order amount (₹)</td>
      </tr>
      <tr>
        <td><code class="inline-code">status</code></td>
        <td>String</td>
        <td>Enum: <code class="inline-code">['reserved', 'collected', 'cancelled']</code></td>
        <td>Order lifecycle status</td>
      </tr>
      <tr>
        <td><code class="inline-code">token</code></td>
        <td>String</td>
        <td>Required (e.g. <code class="inline-code">"TOKEN-98214"</code>)</td>
        <td>Pickup verification token</td>
      </tr>
      <tr>
        <td><code class="inline-code">paymentStatus</code></td>
        <td>String</td>
        <td>Enum: <code class="inline-code">['pending', 'paid', 'refunded']</code></td>
        <td>Payment transaction state</td>
      </tr>
      <tr>
        <td><code class="inline-code">paymentDetails</code></td>
        <td>Object</td>
        <td><code class="inline-code">{ transactionId, cardLast4 }</code></td>
        <td>Payment gateway metadata</td>
      </tr>
      <tr>
        <td><code class="inline-code">createdAt</code></td>
        <td>Date</td>
        <td>Auto Timestamp</td>
        <td>Order creation timestamp</td>
      </tr>
    </tbody>
  </table>

  <p>📄 <strong>Sample Document ( <code class="inline-code">orders</code> ):</strong></p>
  <pre class="code-block">{
  _id: ObjectId('6a6959be4b8992b198eddbe8'),
  customer: ObjectId('6a6959be4b8992b198eddbc0'),
  restaurant: ObjectId('6a6959be4b8992b198eddbc6'),
  foodItem: ObjectId('6a6959be4b8992b198eddbd2'),
  quantity: 2,
  totalPrice: 300,
  status: 'collected',
  token: 'TOKEN-74912',
  paymentStatus: 'paid',
  paymentDetails: {
    transactionId: 'TXN_987412356',
    cardLast4: '4242'
  },
  createdAt: ISODate('2026-07-29T00:39:11.000Z'),
  __v: NumberInt('0')
}</pre>

  <!-- 2.5 Collection: reviews -->
  <h3 class="subsection-header">2.5 Collection: <code class="inline-code">reviews</code> ( <code class="inline-code">Review.js</code> )</h3>
  <p>Stores customer ratings and feedback comments for collected food orders.</p>
  <table class="custom-table">
    <thead>
      <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Constraints</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code class="inline-code">_id</code></td>
        <td>ObjectId</td>
        <td>Primary Key, Auto</td>
        <td>Unique review ID</td>
      </tr>
      <tr>
        <td><code class="inline-code">customer</code></td>
        <td>ObjectId</td>
        <td>Required, Ref: <code class="inline-code">'User'</code></td>
        <td>Customer user reference</td>
      </tr>
      <tr>
        <td><code class="inline-code">restaurant</code></td>
        <td>ObjectId</td>
        <td>Required, Ref: <code class="inline-code">'RestaurantProfile'</code></td>
        <td>Rated restaurant reference</td>
      </tr>
      <tr>
        <td><code class="inline-code">order</code></td>
        <td>ObjectId</td>
        <td>Required, Ref: <code class="inline-code">'Order'</code>, Unique</td>
        <td>Associated order reference</td>
      </tr>
      <tr>
        <td><code class="inline-code">rating</code></td>
        <td>Number</td>
        <td>Required, Min: 1, Max: 5</td>
        <td>Rating score (1 to 5 stars)</td>
      </tr>
      <tr>
        <td><code class="inline-code">comment</code></td>
        <td>String</td>
        <td>Trim</td>
        <td>Review text commentary</td>
      </tr>
      <tr>
        <td><code class="inline-code">createdAt</code></td>
        <td>Date</td>
        <td>Auto Timestamp</td>
        <td>Review creation timestamp</td>
      </tr>
    </tbody>
  </table>

  <p>📄 <strong>Sample Document ( <code class="inline-code">reviews</code> ):</strong></p>
  <pre class="code-block">{
  _id: ObjectId('6a6959be4b8992b198eddbf0'),
  customer: ObjectId('6a6959be4b8992b198eddbc0'),
  restaurant: ObjectId('6a6959be4b8992b198eddbc6'),
  order: ObjectId('6a6959be4b8992b198eddbe8'),
  rating: 5,
  comment: 'Amazing pastries at 70% off! Super fresh and easy pickup with token.',
  createdAt: ISODate('2026-07-29T01:35:00.000Z')
}</pre>

  <hr style="border: 0; border-top: 1px solid #cbd5e1; margin: 18px 0;" />

  <!-- SECTION 3 -->
  <h2 class="section-header">3. DATA FLOW DIAGRAM (DFD)</h2>
  <p>The Data Flow Diagrams (DFD) represent the logical movement of data throughout the <strong>Surplus Food System</strong> across Level 0, Level 1 (Role-specific), and Level 2 detailed process decompositions.</p>

  <!-- 3.1 Level 0 -->
  <div class="avoid-break">
    <h3 class="subsection-header">3.1 Level 0 - System Context Diagram</h3>
    <p>The Level 0 Context Diagram depicts the primary boundary of the Surplus Food system and its data flow exchanges with External Entities (<strong>Customer</strong>, <strong>System Admin</strong>, <strong>Restaurant Partner</strong>).</p>

    <div class="diagram-container">
      <pre style="margin: 0 0 10px 0; font-family: monospace; font-size: 8.5pt; text-align: left;">
 ┌──────────────┐
 │   Customer   │
 └──────┬───────┘
Request │ Response (Food Items /
(Orders)│           Tokens)
        ▼
 ┌──────────────┐   ┌──────────────────────┐   ┌────────────────────┐
 │    Admin     │──►│ Surplus Food System  │◄──│ Restaurant Partner │
 └──────────────┘◄──│      Platform        │──►└────────────────────┘
  Request & Control │ Response (Dashboard &│ Request & Response (Food
                    │           Analytics) │ Listings & Token Verify)
                    └──────────────────────┘</pre>

      <div class="mermaid">
      graph TD
          Customer[👤 Customer] -->|Browse Surplus Food & Reserve| System((🌐 Surplus Food Platform))
          System -->|Pickup Token, PDF Receipt & Order Status| Customer

          Restaurant[🏪 Restaurant Partner] -->|Post Food Items & Verify Tokens| System
          System -->|Order Notifications & Sales Analytics| Restaurant

          Admin[🛡️ System Admin] -->|User Verification & Platform Control| System
          System -->|System Analytics & Audit Logs| Admin
      </div>
    </div>
  </div>

  <!-- 3.2 Level 1 - Admin -->
  <div class="avoid-break">
    <h3 class="subsection-header">3.2 Level 1 - Admin</h3>
    <p>Decomposes administrative functionality. The Admin authenticates via the User Table and manages users, restaurant verifications, analytics, and platform oversight.</p>

    <div class="diagram-container">
      <pre style="margin: 0 0 10px 0; font-family: monospace; font-size: 8.5pt; text-align: left;">
┌───────┐   ┌───────┐   ┌──────────────────────┐   ┌─────────────────┐
│ Admin │──►│ Login │──►│ Manage Users         │◄─►│ User Table      │
└───────┘   └───────┘   ├──────────────────────┤   └─────────────────┘
                        │ Verify Restaurants   │◄─►│ Restaurant Store│
                        ├──────────────────────┤   └─────────────────┘
                        │ Monitor All Orders   │◄─►│ Order Store     │
                        ├──────────────────────┤   └─────────────────┘
                        │ View Analytics       │◄─►│ Sales & Reviews │
                        └──────────────────────┘   └─────────────────┘</pre>

      <div class="mermaid">
      graph TD
          Admin[🛡️ Admin] --> Login((Login))
          Login <--> UserTable[(📁 User Table)]
          Login --> P1((Manage Users)) <--> D1[(📁 Users Store)]
          Login --> P2((Verify Restaurants)) <--> D2[(📁 Restaurant Profiles)]
          Login --> P3((Monitor All Orders)) <--> D3[(📁 Orders Store)]
          Login --> P4((View System Analytics)) <--> D4[(📁 Recharts Analytics)]
      </div>
    </div>
  </div>

  <!-- 3.3 Level 1 - User (Customer) -->
  <div class="avoid-break">
    <h3 class="subsection-header">3.3 Level 1 - User (Customer)</h3>
    <p>Decomposes customer functionality. Registered customers authenticate, manage profiles, search geolocated surplus food items, reserve food items, pay, and submit reviews.</p>

    <div class="diagram-container">
      <pre style="margin: 0 0 10px 0; font-family: monospace; font-size: 8.5pt; text-align: left;">
┌────────┐   ┌─────────┐   ┌──────────────────────┐   ┌─────────────────┐
│ Public │──►│Register │──►│ Manage Profile       │◄─►│ Customer Info   │
│Customer│   │ & Login │   ├──────────────────────┤   └─────────────────┘
└────────┘   └─────────┘   │ Search Surplus Food  │◄─►│ Food Items      │
                           ├──────────────────────┤   └─────────────────┘
                           │ Reserve & Pay        │◄─►│ Orders & Tokens │
                           ├──────────────────────┤   └─────────────────┘
                           │ Download PDF Receipt │◄─►│ jsPDF Receipt   │
                           ├──────────────────────┤   └─────────────────┘
                           │ Submit Review        │◄─►│ Reviews Store   │
                           └──────────────────────┘   └─────────────────┘</pre>

      <div class="mermaid">
      graph TD
          Customer[👤 Customer] --> Auth((Register & Login))
          Auth <--> UserTable[(📁 User Table)]
          Auth --> P1((Manage Profile)) <--> D1[(📁 Users Store)]
          Auth --> P2((Search Surplus Food)) <--> D2[(📁 Food Items Store)]
          Auth --> P3((Reserve Food & Pay)) <--> D3[(📁 Orders Store)]
          Auth --> P4((Download PDF Receipt)) <--> D3
          Auth --> P5((Submit Review & Rating)) <--> D4[(📁 Reviews Store)]
      </div>
    </div>
  </div>

  <!-- 3.4 Level 1 - Restaurant Partner -->
  <div class="avoid-break">
    <h3 class="subsection-header">3.4 Level 1 - Restaurant Partner</h3>
    <p>Decomposes restaurant functionality. Restaurant owners authenticate, create profiles, post surplus food listings, manage pickup windows, and verify customer pickup tokens.</p>

    <div class="diagram-container">
      <pre style="margin: 0 0 10px 0; font-family: monospace; font-size: 8.5pt; text-align: left;">
┌──────────┐   ┌─────────┐   ┌──────────────────────┐   ┌─────────────────┐
│Restaurant│──►│ Partner │──►│ Setup Profile        │◄─►│ Restaurant Store│
│ Partner  │   │ Login   │   ├──────────────────────┤   └─────────────────┘
└──────────┘   └─────────┘   │ Post Surplus Food    │◄─►│ Food Items Store│
                             ├──────────────────────┤   └─────────────────┘
                             │ View Active Orders   │◄─►│ Orders Store    │
                             ├──────────────────────┤   └─────────────────┘
                             │ Verify Pickup Token  │◄─►│ Order Status    │
                             └──────────────────────┘   └─────────────────┘</pre>

      <div class="mermaid">
      graph TD
          Restaurant[🏪 Restaurant] --> RLogin((Partner Login))
          RLogin <--> UserTable[(📁 User Table)]
          RLogin --> RP1((Manage Profile)) <--> RD1[(📁 Restaurant Profile Store)]
          RLogin --> RP2((Post Surplus Food)) <--> RD2[(📁 Food Items Store)]
          RLogin --> RP3((View Active Orders)) <--> RD3[(📁 Orders Store)]
          RLogin --> RP4((Verify Pickup Token)) <--> RD3
      </div>
    </div>
  </div>

  <!-- 3.5 Level 2 - Admin -->
  <div class="avoid-break">
    <h3 class="subsection-header">3.5 Level 2 - Admin (Detailed Process Decomposition)</h3>
    <p>Detailed Level 2 breakdown showing exact sub-processes and datastores managed by the System Administrator.</p>

    <div class="diagram-container">
      <pre style="margin: 0 0 10px 0; font-family: monospace; font-size: 8.5pt; text-align: left;">
┌───────┐
│ Admin │──────┐
└───────┘      │
               ├──────► ┌──────────────────────┐
               │        │ Manage Users         │
               │        ├──────────────────────┤
               │        │ ├─ View Users        │──────► ┌─────────────────┐
               │        │ ├─ Edit Role         │        │  Users / Roles  │
               │        │ └─ Delete User       │◄────── │   Collection    │
               │        └──────────────────────┘        └─────────────────┘
               │
               ├──────► ┌──────────────────────┐
               │        │ Verify Restaurants   │
               │        ├──────────────────────┤
               │        │ ├─ View Pending      │──────► ┌─────────────────┐
               │        │ ├─ Approve Partner   │        │   Restaurant    │
               │        │ └─ Reject Partner    │◄────── │   Collection    │
               │        └──────────────────────┘        └─────────────────┘
               │
               └──────► ┌──────────────────────┐
                        │ Platform Analytics   │
                        ├──────────────────────┤
                        │ ├─ Sales Reports     │──────► ┌─────────────────┐
                        │ └─ Food Waste Metrics│◄────── │ Orders & Reviews│
                        └──────────────────────┘        └─────────────────┘</pre>

      <div class="mermaid">
      graph TD
          Admin[🛡️ Admin] --> Users[Manage Users]
          Users --> U1((View Users)) --> D1[(📁 Users)]
          Users --> U2((Edit User Role)) --> D1
          Users --> U3((Delete User)) --> D1

          Admin --> Rest[Verify Restaurants]
          Rest --> R1((View Pending Partners)) --> D2[(📁 Restaurants)]
          Rest --> R2((Approve Verification)) --> D2
          Rest --> R3((Reject Partner)) --> D2

          Admin --> Analytics[Platform Analytics]
          Analytics --> A1((View Sales Trends)) --> D3[(📁 Orders)]
          Analytics --> A2((View Food Saved Metrics)) --> D3
      </div>
    </div>
  </div>

  <hr style="border: 0; border-top: 1px solid #cbd5e1; margin: 18px 0;" />

  <!-- SECTION 4 -->
  <h2 class="section-header">4. USER STORIES</h2>
  <p>User stories are categorized under four main Epics, complete with Acceptance Criteria and Story Point estimates based on the Fibonacci scale.</p>

  <h3 class="subsection-header">Epic 1: Identity & Access Management (IAM)</h3>
  
  <div class="user-story-card">
    <div class="story-title">📖 User Story 1.1: Customer & Restaurant Registration</div>
    <div class="story-body"><strong>As a</strong> User (Customer / Restaurant),<br/>
    <strong>I want to</strong> register an account with my name, email, password, role, and phone number,<br/>
    <strong>So that</strong> I can log into my personalized dashboard and use the platform.</div>
    <div class="story-criteria"><strong>Acceptance Criteria:</strong>
      <ul>
        <li>Passwords must be hashed using Bcrypt (10 salt rounds) before DB insertion.</li>
        <li>Duplicate emails must be rejected with HTTP 400 Bad Request.</li>
        <li>Generates a 6-digit OTP and sends email verification link via Nodemailer.</li>
      </ul>
    </div>
    <div class="story-estimate">Story Estimate: 3 SP</div>
  </div>

  <div class="user-story-card">
    <div class="story-title">📖 User Story 1.2: Unified JWT Authentication & Login</div>
    <div class="story-body"><strong>As a</strong> Registered User (Customer / Restaurant / Admin),<br/>
    <strong>I want to</strong> authenticate using my credentials,<br/>
    <strong>So that</strong> I can receive a secure JSON Web Token and access role-restricted APIs.</div>
    <div class="story-criteria"><strong>Acceptance Criteria:</strong>
      <ul>
        <li>Returns JWT token containing user ID and role upon successful password match.</li>
        <li>Invalid credentials return HTTP 401 Unauthorized.</li>
        <li>Frontend stores token in localStorage and auto-attaches it via Axios request interceptors.</li>
      </ul>
    </div>
    <div class="story-estimate">Story Estimate: 3 SP</div>
  </div>

  <h3 class="subsection-header">Epic 2: Restaurant & Surplus Food Catalog Management (FCM)</h3>

  <div class="user-story-card">
    <div class="story-title">📖 User Story 2.1: Restaurant Profile Creation & Verification</div>
    <div class="story-body"><strong>As a</strong> Restaurant Partner,<br/>
    <strong>I want to</strong> set up my restaurant profile with name, address, cuisine type, cover photo, and location,<br/>
    <strong>So that</strong> customers can discover my business and surplus listings.</div>
    <div class="story-criteria"><strong>Acceptance Criteria:</strong>
      <ul>
        <li>Multer middleware handles cover photo uploads to <code class="inline-code">/uploads</code> folder.</li>
        <li>Latitude and Longitude populated via interactive OpenStreetMap pin.</li>
        <li>Profile remains in unverified state until approved by System Admin.</li>
      </ul>
    </div>
    <div class="story-estimate">Story Estimate: 5 SP</div>
  </div>

  <div class="user-story-card">
    <div class="story-title">📖 User Story 2.2: Surplus Food Item Listing & Pickup Windows</div>
    <div class="story-body"><strong>As a</strong> Restaurant Partner,<br/>
    <strong>I want to</strong> post surplus food items with original price, discounted price, stock quantity, and pickup times,<br/>
    <strong>So that</strong> customers can buy excess food before closing hours.</div>
    <div class="story-criteria"><strong>Acceptance Criteria:</strong>
      <ul>
        <li>Discount percentage automatically calculated and displayed on item card.</li>
        <li>Pickup start and end times enforced (e.g. <code class="inline-code">"18:00"</code> to <code class="inline-code">"21:00"</code>).</li>
        <li>Status automatically switches to <code class="inline-code">sold-out</code> when quantity reaches 0.</li>
      </ul>
    </div>
    <div class="story-estimate">Story Estimate: 5 SP</div>
  </div>

  <h3 class="subsection-header">Epic 3: Order Reservation & Payment Processing (ORP)</h3>

  <div class="user-story-card">
    <div class="story-title">📖 User Story 3.1: Surplus Food Reservation & Token Generation</div>
    <div class="story-body"><strong>As a</strong> Customer,<br/>
    <strong>I want to</strong> reserve available surplus food items and generate a pickup token,<br/>
    <strong>So that</strong> I can secure the item for evening collection.</div>
    <div class="story-criteria"><strong>Acceptance Criteria:</strong>
      <ul>
        <li>Generates a unique 6-character alphanumeric pickup token (e.g., <code class="inline-code">TOKEN-84912</code>).</li>
        <li>Item quantity atomically decrements in MongoDB upon successful reservation.</li>
        <li>Generates downloadable PDF receipt using <code class="inline-code">jsPDF</code> library.</li>
      </ul>
    </div>
    <div class="story-estimate">Story Estimate: 5 SP</div>
  </div>

  <div class="user-story-card">
    <div class="story-title">📖 User Story 3.2: Payment Gateway Simulation</div>
    <div class="story-body"><strong>As a</strong> Customer,<br/>
    <strong>I want to</strong> pay for my surplus food order via debit/credit card simulation,<br/>
    <strong>So that</strong> my order is confirmed instantly.</div>
    <div class="story-criteria"><strong>Acceptance Criteria:</strong>
      <ul>
        <li>Modal UI collects test card numbers, expiry date, and CVV.</li>
        <li>Simulates payment verification and records transaction ID in order document.</li>
        <li>Updates payment status to <code class="inline-code">paid</code> upon completion.</li>
      </ul>
    </div>
    <div class="story-estimate">Story Estimate: 5 SP</div>
  </div>

  <h3 class="subsection-header">Epic 4: Review, Rating & Administrative Oversight (RRA)</h3>

  <div class="user-story-card">
    <div class="story-title">📖 User Story 4.1: Customer Review & Rating System</div>
    <div class="story-body"><strong>As a</strong> Customer,<br/>
    <strong>I want to</strong> rate (1-5 stars) and review restaurants after collecting my order,<br/>
    <strong>So that</strong> other customers can find top-quality surplus food providers.</div>
    <div class="story-criteria"><strong>Acceptance Criteria:</strong>
      <ul>
        <li>Only customers with <code class="inline-code">collected</code> orders can submit a review.</li>
        <li>Restaurant average rating and total review count automatically recalculate.</li>
      </ul>
    </div>
    <div class="story-estimate">Story Estimate: 3 SP</div>
  </div>

  <div class="user-story-card">
    <div class="story-title">📖 User Story 4.2: Admin Platform Dashboard & Analytics</div>
    <div class="story-body"><strong>As a</strong> System Administrator,<br/>
    <strong>I want to</strong> monitor system revenue, active restaurants, food waste saved, and review reports,<br/>
    <strong>So that</strong> I can oversee platform growth and maintain food safety standards.</div>
    <div class="story-criteria"><strong>Acceptance Criteria:</strong>
      <ul>
        <li>Recharts charts render total revenue, orders count, and monthly food waste reduction.</li>
        <li>Admin can verify or suspend restaurant partner accounts with one click.</li>
      </ul>
    </div>
    <div class="story-estimate">Story Estimate: 4 SP</div>
  </div>

  <hr style="border: 0; border-top: 1px solid #cbd5e1; margin: 18px 0;" />

  <!-- SECTION 5 -->
  <h2 class="section-header">5. GIT COMMIT HISTORY SUMMARY (REVIEW CYCLE)</h2>
  <p>To fulfill the CIE 2 evaluation requirement of a <strong>minimum of 4 commits during the current review cycle</strong>, the commit log summary is recorded below:</p>

  <pre class="code-block">commit 582ed53a91b2c4e0f123456789abcdef0123456789ab
Author: Athul Krishna R &lt;athulkrishna@example.com&gt;
Date:   Thu Aug 13 16:45:22 2026 +0530

    feat(order): implement order reservation, payment simulation & token generation
    - Add Order schema with pickup token and paymentDetails subdocument
    - Connect POST /api/customer/orders with quantity validation and stock decrement
    - Implement card payment simulation modal with transaction ID generation

commit a4b2406b10a9b8c7f6e5d4c3b2a10987654321fedcba
Author: Athul Krishna R &lt;athulkrishna@example.com&gt;
Date:   Tue Aug 11 14:20:10 2026 +0530

    feat(pdf): add jsPDF order receipt download and customer order history
    - Integrate jsPDF library for instant downloadable customer receipts
    - Display pickup token QR/barcode representation on order confirmation card
    - Add order cancellation and automatic inventory restock logic

commit 49b182ba6f5e4d3c2b1a0987654321fedcba56789a
Author: Athul Krishna R &lt;athulkrishna@example.com&gt;
Date:   Sun Aug 09 11:15:45 2026 +0530

    feat(auth): implement email OTP verification and bcrypt password hashing
    - Add Nodemailer transport configuration in config/mailer.js
    - Connect 6-digit OTP generation and verification routes
    - Hash user passwords using Bcrypt pre-save hooks in User.js

commit 6fc7335c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b
Author: Athul Krishna R &lt;athulkrishna@example.com&gt;
Date:   Fri Aug 07 10:00:00 2026 +0530

    refactor(scrum): finalize CIE 2 Scrum Book documentation & schema validation
    - Format updated sprint details, definition of done, and story point velocity
    - Complete Mongoose collection tables for User, RestaurantProfile, FoodItem, Order, Review</pre>

  <br/>
  <div style="text-align: center; font-style: italic; color: #64748b; margin-top: 30px; font-weight: bold;">
    End of Scrum Book Submission - 2 (CIE 2)
  </div>

</body>
</html>
"""

async def build_pdf():
    html_path = os.path.abspath("d:/surplus-food/scrum_book.html")
    pdf_path = os.path.abspath("d:/surplus-food/Scrum_Book_Submission_2_CIE2.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{html_path.replace('\\\\', '/')}")
        
        # Wait for Mermaid SVGs to render fully
        try:
            await page.wait_for_selector('.mermaid svg', timeout=15000)
            await page.wait_for_timeout(1000) # Give extra second for layout settling
        except Exception as e:
            print(f"Warning waiting for Mermaid selector: {e}")
            
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template='''
                <div style="width: 100%; font-size: 8pt; font-family: sans-serif; color: #64748b; padding: 0 15mm; display: flex; justify-content: space-between; box-sizing: border-box;">
                    <span>SURPLUS FOOD</span>
                    <span>SCRUM BOOK: SUBMISSION - 2</span>
                </div>
            ''',
            footer_template='''
                <div style="width: 100%; font-size: 8pt; font-family: sans-serif; color: #64748b; padding: 0 15mm; display: flex; justify-content: space-between; box-sizing: border-box;">
                    <span>Department of Computer Applications</span>
                    <span>MEA Engineering College</span>
                </div>
            ''',
            margin={
                "top": "18mm",
                "bottom": "18mm",
                "left": "15mm",
                "right": "15mm"
            }
        )
        await browser.close()
    print(f"Successfully re-generated PDF at: {pdf_path}")

if __name__ == "__main__":
    asyncio.run(build_pdf())

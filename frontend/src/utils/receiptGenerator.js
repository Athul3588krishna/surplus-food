import { jsPDF } from 'jspdf';

/**
 * Generates and downloads a beautiful, print-ready client-side PDF receipt for a reservation.
 * @param {Object} order - The populated order object containing foodItem and restaurant details.
 * @param {string} customerName - Fallback customer name in case order.customer isn't populated.
 */
export const generateReceiptPDF = (order, customerName = 'EcoBite Customer') => {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a5' // A5 is compact and looks like a realistic store receipt
  });

  // Color Definitions
  const colorPrimary = '#10b981'; // Emerald
  const colorTextDark = '#1f2937'; // Slate 800
  const colorTextMuted = '#6b7280'; // Gray 500

  // 1. Header Banner Background Rect
  doc.setFillColor(242, 253, 249); // light green background tint
  doc.rect(0, 0, 148, 30, 'F');
  
  // Brand Header
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.setTextColor(16, 185, 129); // Primary Emerald
  doc.text('EcoBite Marketplace', 15, 13);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(100, 116, 139);
  doc.text('Thank you for rescuing surplus food and saving waste!', 15, 18);

  // 2. Receipt Details Card
  const receiptCode = order.paymentDetails?.transactionId || order._id.substring(order._id.length - 8).toUpperCase();
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(31, 41, 55);
  doc.text(`RECEIPT: #${receiptCode}`, 15, 40);

  const orderDate = new Date(order.createdAt || Date.now()).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(colorTextMuted);
  doc.text(`Transaction Date: ${orderDate}`, 15, 45);
  doc.text(`Payment Method: Card (last 4: ${order.paymentDetails?.cardLast4 || '4242'})`, 15, 50);

  // Line Divider
  doc.setDrawColor(243, 244, 246);
  doc.setLineWidth(0.5);
  doc.line(15, 54, 133, 54);

  // 3. User Details & Store Location
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(colorTextDark);
  doc.text('Customer Information', 15, 61);
  doc.text('Store Location', 80, 61);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(75, 85, 99);
  
  // Left: Customer details
  const nameDisplay = order.customer?.name || customerName;
  doc.text(nameDisplay, 15, 66);
  doc.text(`Phone: ${order.customer?.phoneNumber || 'Provided on App'}`, 15, 71);

  // Right: Restaurant details
  const storeName = order.restaurant?.restaurantName || 'EcoBite Partner';
  const storeAddress = order.restaurant?.address || 'Restaurant Address';
  doc.text(storeName, 80, 66);
  const splitAddress = doc.splitTextToSize(storeAddress, 53);
  doc.text(splitAddress, 80, 71);

  // Line Divider
  doc.line(15, 82, 133, 82);

  // 4. Itemized Price Breakdown
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(colorTextDark);
  doc.text('Rescued Item', 15, 89);
  doc.text('Quantity', 95, 89);
  doc.text('Total Paid', 115, 89);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(75, 85, 99);
  const itemName = order.foodItem?.name || 'Surplus Food Box';
  doc.text(itemName, 15, 95);
  doc.text(String(order.quantity), 95, 95);
  doc.text(`$${order.totalPrice.toFixed(2)}`, 115, 95);

  // Line Divider
  doc.line(15, 101, 133, 101);

  // 5. Verification Token Dash-Box
  doc.setFillColor(249, 250, 251); // gray background
  doc.roundedRect(15, 107, 118, 22, 2, 2, 'F');
  doc.setDrawColor(16, 185, 129); // Emerald border
  doc.setLineDashPattern([1.5, 1.5], 0); // dotted line
  doc.rect(15, 107, 118, 22);
  doc.setLineDashPattern([], 0); // reset line

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(7);
  doc.setTextColor(100, 116, 139);
  doc.text('CUSTOMER COLLECTION OTP TOKEN (CLAIM ID)', 74, 112, { align: 'center' });

  const tokenStr = order.token || '000000';
  const formattedToken = `${tokenStr.slice(0, 3)} ${tokenStr.slice(3, 6)}`;
  doc.setFontSize(15);
  doc.setTextColor(31, 41, 55);
  doc.text(formattedToken, 74, 121, { align: 'center', charSpace: 3 });

  // 6. Warnings and Instructions
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(8);
  doc.setTextColor(239, 68, 68); // Red warnings
  const windowStr = `PICKUP WINDOW: ${order.foodItem?.pickupStartTime || '18:00'} - ${order.foodItem?.pickupEndTime || '21:00'}`;
  doc.text(windowStr, 74, 136, { align: 'center' });

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(7.5);
  doc.setTextColor(107, 114, 128);
  doc.text('Please collect during the specified window. Present this token code to claim food.', 74, 141, { align: 'center' });

  // Save/Download Action
  doc.save(`EcoBite-Receipt-${receiptCode}.pdf`);
};

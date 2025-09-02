import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image

st.set_page_config(page_title="DigiReceipt", layout="centered")

# 📊 Basic Analytics
if "invoice_count" not in st.session_state:
    st.session_state.invoice_count = 0

st.title("🧾 DigiReceipt Invoice Generator")
st.markdown("سادہ رسید بنانے والا موبائل ایپ۔ تفصیلات درج کریں، رسید بنائیں، اور PDF ڈاؤنلوڈ کریں۔")

# 🖼️ Optional Logo Upload
logo = st.file_uploader("🔗 اپنی دکان کا لوگو اپلوڈ کریں (اختیاری)", type=["png", "jpg", "jpeg"])
if logo:
    st.image(logo, width=120)

with st.form("invoice_form"):
    st.markdown("### 🧑‍💼 دکاندار اور کسٹمر کی معلومات")
    vendor_name = st.text_input("Vendor Name / دکان کا نام")
    customer_name = st.text_input("Customer Name / کسٹمر کا نام")
    tax_number = st.text_input("Tax Number / ٹیکس نمبر")
    status = st.selectbox("Payment Status / ادائیگی کی حالت", ["Paid", "Unpaid"])
    address = st.text_input("Customer Address / پتہ")
    phone = st.text_input("Phone Number / فون نمبر")
    signature = st.text_input("Signature / دستخط")

    # 🧾 Editable Invoice Number
    default_invoice_no = f"INV-{datetime.today().strftime('%Y%m%d')}-{st.session_state.invoice_count + 1}"
    invoice_no = st.text_input("Invoice Number / رسید نمبر", value=default_invoice_no)

    warranty_note = st.selectbox("Warranty Note / وارنٹی", [
        "14-Day Return Policy",
        "No Returns, Only Replacement",
        "Service Warranty: 7 Days",
        "Product Warranty: 30 Days",
        "No Warranty Provided"
    ])

    st.markdown("### 🛒 اشیاء کی تفصیلات درج کریں")
    items = []
    for i in range(1, 6):
        name = st.text_input(f"Item {i} Name / آئٹم {i} کا نام")
        price = st.number_input(f"Item {i} Price / قیمت", min_value=0.0, step=0.01)
        quantity = st.number_input(f"Item {i} Quantity / مقدار", min_value=0, step=1)
        if name:
            items.append({"name": name, "price": price, "quantity": quantity})

    submitted = st.form_submit_button("🧾 Generate Invoice / رسید بنائیں")

if submitted:
    st.session_state.invoice_count += 1
    date = datetime.today().strftime("%d-%b-%Y")
    total = sum(item['price'] * item['quantity'] for item in items)

    # 📄 Generate PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40

    if logo:
        img = Image.open(logo)
        img_width = 50 * mm
        img_height = img.height / img.width * img_width
        pdf.drawInlineImage(img, 40, y - img_height, width=img_width, height=img_height)
        y -= img_height + 10

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, f"{vendor_name.upper()} - INVOICE")
    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, f"Invoice No: {invoice_no}")
    pdf.drawString(300, y, f"Date: {date}")
    y -= 15
    pdf.drawString(40, y, f"Customer: {customer_name}")
    pdf.drawString(300, y, f"Status: {status}")
    y -= 15
    pdf.drawString(40, y, f"Tax Number: {tax_number}")
    pdf.drawString(40, y - 15, f"Address: {address}")
    pdf.drawString(300, y - 15, f"Phone: {phone}")
    y -= 35

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, y, "No  Item Name           Price     Qty     Total")
    y -= 10
    pdf.line(40, y, 550, y)
    y -= 15

    pdf.setFont("Helvetica", 10)
    for i, item in enumerate(items, start=1):
        line_total = item['price'] * item['quantity']
        pdf.drawString(40, y, f"{i:<3} {item['name']:<20} {item['price']:>7.2f}   x {item['quantity']}   = {line_total:>7.2f}")
        y -= 15

    y -= 10
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, y, f"Total Amount: {total:.2f}")
    y -= 15
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, f"Warranty: {warranty_note}")
    pdf.drawString(300, y, f"Signature: {signature}")
    y -= 30
    pdf.drawString(40, y, "Thank you for your business!")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    st.download_button("📥 Download PDF Invoice / رسید PDF میں ڈاؤنلوڈ کریں", buffer, file_name=f"{invoice_no.replace(' ', '_')}.pdf")

    # 📤 Email Share Option
    st.markdown(f"[📤 Send via Email](mailto:?subject=Invoice&body=Invoice%20for%20{customer_name}%20-%20Total%20{total:.2f})")

# 📊 Show Basic Analytics
st.markdown("---")
st.metric("📊 Total Invoices Created", st.session_state.invoice_count)

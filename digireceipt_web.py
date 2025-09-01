import streamlit as st
from datetime import datetime

st.set_page_config(page_title="DigiReceipt", layout="centered")

st.title("🧾 DigiReceipt Invoice Generator")
st.markdown("Generate simple invoices directly from your phone or browser.")

with st.form("invoice_form"):
    vendor_name = st.text_input("Vendor Name / دکان کا نام")
    customer_name = st.text_input("Customer Name / کسٹمر کا نام")
    tax_number = st.text_input("Tax Number / ٹیکس نمبر")
    status = st.selectbox("Payment Status / ادائیگی کی حالت", ["Paid", "Unpaid"])
    address = st.text_input("Customer Address / پتہ")
    phone = st.text_input("Phone Number / فون نمبر")
    signature = st.text_input("Signature / دستخط")

    warranty_options = [
        "14-Day Return Policy",
        "No Returns, Only Replacement",
        "Service Warranty: 7 Days",
        "Product Warranty: 30 Days",
        "No Warranty Provided"
    ]
    warranty_note = st.selectbox("Warranty Note / وارنٹی", warranty_options)

    st.markdown("### 🛒 Enter Items")
    items = []
    for i in range(1, 6):  # Allow up to 5 items
        name = st.text_input(f"Item {i} Name")
        price = st.number_input(f"Item {i} Price", min_value=0.0, step=0.01)
        quantity = st.number_input(f"Item {i} Quantity", min_value=0, step=1)
        if name:
            items.append({"name": name, "price": price, "quantity": quantity})

    submitted = st.form_submit_button("Generate Invoice")

if submitted:
    date = datetime.today().strftime("%d-%b-%Y")
    item_lines = "No  Item Name           Price      Qty   Total\n"
    item_lines += "------------------------------------------------\n"
    total = 0
    for i, item in enumerate(items, start=1):
        line_total = item['price'] * item['quantity']
        total += line_total
        item_lines += f"{i:<3} {item['name']:<20} {item['price']:>8.2f}   x {item['quantity']:<3} = {line_total:>8.2f}\n"

    invoice = f"""
    ----------------------------------
              🧾 INVOICE
         {vendor_name.upper()}
    ----------------------------------
    Customer     : {customer_name}
    Tax Number   : {tax_number}
    Date         : {date}
    Status       : {status}

    Items:
{item_lines}
    ----------------------------------
    Total Amount : {total:.2f}
    Warranty     : {warranty_note}
    Signature    : {signature}
    ----------------------------------
    Thank you for your business!
    Address      : {address}
    Phone        : {phone}
    ----------------------------------
    """

    st.text_area("📄 Invoice Preview", invoice, height=400)
    st.download_button("📥 Download Invoice", invoice, file_name=f"Invoice_{customer_name.replace(' ', '_')}.txt")


import streamlit as st

menu = [
    {"id": 1, "name": "Latte", "price": 55},
    {"id": 2, "name": "Flat White", "price": 60},
    {"id": 3, "name": "Popcorn Latte", "price": 65},
    {"id": 4, "name": "Americano", "price": 50},
    {"id": 5, "name": "Tiramisu", "price": 85},
    {"id": 6, "name": "Banoffee Pie", "price": 75},
    {"id": 7, "name": "Blueberry Cake", "price": 80},
]

# Initialize States
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False

st.title("☕ ร้านกาแฟ Super Shop")
st.subheader("📋 รายการเมนู")

# 1. แสดงเมนูและปุ่มกด
for item in menu:
    i_id, qty = item["id"], st.session_state.cart.get(item["id"], 0)
    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
    
    col1.write(f"**{item['name']}** ({item['price']} บาท)")
    if col2.button("➕", key=f"+{i_id}", use_container_width=True):
        st.session_state.cart[i_id] = qty + 1
        st.session_state.confirmed = False
        st.rerun()
        
    col3.markdown(f"<div style='text-align: center; font-weight: bold;'>{qty}</div>", unsafe_allow_html=True)
    
    if col4.button("➖", key=f"-{i_id}", use_container_width=True) and i_id in st.session_state.cart:
        st.session_state.cart[i_id] -= 1
        if st.session_state.cart[i_id] <= 0:
            del st.session_state.cart[i_id]
        st.session_state.confirmed = False
        st.rerun()

st.divider()

# 2. คำนวณและสรุปรายการที่เลือก
selected_items = [
    {**item, "qty": st.session_state.cart[item["id"]], "subtotal": item["price"] * st.session_state.cart[item["id"]]}
    for item in menu if st.session_state.cart.get(item["id"], 0) > 0
]
total_price = sum(item["subtotal"] for item in selected_items)

if selected_items:
    st.markdown("### 🛒 รายการที่เลือก")
    for item in selected_items:
        st.write(f"• {item['name']} x {item['qty']} = {item['subtotal']} บาท")
    
    st.markdown(f"## Total : **{total_price}** บาท")
    
    if st.button("✅ ยืนยันรายการอาหาร", type="primary", use_container_width=True):
        st.session_state.confirmed = True
        st.rerun()
else:
    st.info("กรุณาเลือกรายการอาหาร")

# 3. แสดงบิลใบเสร็จ
if st.session_state.confirmed and selected_items:
    st.divider()
    st.subheader("🧾 บิลใบเสร็จรับเงิน")
    for item in selected_items:
        st.write(f"• {item['name']} x {item['qty']} = {item['subtotal']} บาท")
    st.divider()
    st.markdown(f"### ยอดรวมสุทธิ: **{total_price}** บาท")
    st.caption("ขอบคุณที่อุดหนุนค่ะ!")

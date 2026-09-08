import streamlit as st

menu = [
    {"id": 1, "name": "Latte☕", "price": 65},
    {"id": 2, "name": "Flat white🥛", "price": 65},
    {"id": 3, "name": "Popcorn Latte🍿", "price": 70},
    {"id": 4, "name": "Americano🫗", "price": 60},
    {"id": 5, "name": "Tiramisu🍰", "price": 45},
    {"id": 6, "name": "Banoffee Pie🥧", "price": 40},
    {"id": 7, "name": "Blueberry Cake🧁", "price": 40},
]

if "cart" not in st.session_state:
    st.session_state.cart = {}

# ฟังก์ชันสร้างหน้าต่างบิลเด้งกลางหน้าจอ (Modal Dialog)
@st.dialog("🧾 บิลใบเสร็จรับเงิน")
def show_receipt(selected_items, total_price):
    for item in selected_items:
        st.write(f"• **{item['name']}** x {item['qty']} = {item['subtotal']} บาท")
    
    st.divider()
    st.markdown(f"### ยอดรวมสุทธิ: **{total_price}** บาท")
    st.caption("ขอบคุณที่อุดหนุนค่ะ! 🙏")
    
    if st.button("ปิดหน้าต่าง / สั่งซื้อใหม่", use_container_width=True):
        st.session_state.cart = {} # ล้างตะกร้าเมื่อปิดบิล
        st.rerun()

st.title("☕ ร้านกาแฟ Super Shop🍰☕")
st.subheader("📋 รายการเมนู")

# 1. แสดงรายการเมนู
for item in menu:
    i_id, qty = item["id"], st.session_state.cart.get(item["id"], 0)
    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
    
    col1.write(f"**{item['name']}** ({item['price']} บาท)")
    if col2.button("➕", key=f"+{i_id}", use_container_width=True):
        st.session_state.cart[i_id] = qty + 1
        st.rerun()
        
    col3.markdown(f"<div style='text-align: center; font-weight: bold;'>{qty}</div>", unsafe_allow_html=True)
    
    if col4.button("➖", key=f"-{i_id}", use_container_width=True) and i_id in st.session_state.cart:
        st.session_state.cart[i_id] -= 1
        if st.session_state.cart[i_id] <= 0:
            del st.session_state.cart[i_id]
        st.rerun()

st.divider()

# 2. คำนวณสรุปรายการที่เลือก
selected_items = [
    {**item, "qty": st.session_state.cart[item["id"]], "subtotal": item["price"] * st.session_state.cart[item["id"]]}
    for item in menu if st.session_state.cart.get(item["id"], 0) > 0
]
total_price = sum(item["subtotal"] for item in selected_items)

# 3. แสดงสรุปรายการและปุ่มยืนยัน
if selected_items:
    st.markdown("### 🛒 รายการที่เลือก")
    for item in selected_items:
        st.write(f"• {item['name']} x {item['qty']} = {item['subtotal']} บาท")
    
    st.markdown(f"## Total : **{total_price}** บาท")
    
    # เมื่อกดปุ่มจะเรียกใช้ฟังก์ชัน show_receipt() เพื่อเปิด Popup เด้งขึ้นมา
    if st.button("✅ ยืนยันเมนู", type="primary", use_container_width=True):
        show_receipt(selected_items, total_price)
else:
    st.info("กรุณาเลือกรายการอาหาร")
    

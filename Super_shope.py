import streamlit as st

menu_data = [
    {"id": 1, "name": "Latte ☕", "price": 55},
    {"id": 2, "name": "Flat White 🥛", "price": 60},
    {"id": 3, "name": "Popcorn Latte 🍿", "price": 65},
    {"id": 4, "name": "Americano 🫗", "price": 50},
    {"id": 5, "name": "Tiramisu 🍰", "price": 85},
    {"id": 6, "name": "Banoffee Pie 🥧", "price": 75},
    {"id": 7, "name": "Blueberry Cake 🧁", "price": 80},
]

# State สำหรับเก็บตะกร้าสินค้า และสถานะการยืนยันสั่งซื้อ
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "order_confirmed" not in st.session_state:
    st.session_state.order_confirmed = False

st.title("☕ Super Shop")
st.subheader("📋 รายการเมนู")

# แสดงรายการเมนู
for item in menu_data:
    item_id = item["id"]
    qty = st.session_state.cart.get(item_id, 0)

    # จัดเลย์เอาต์: ชื่อเมนู (ฝั่งซ้าย) | ปุ่ม - | ตัวเลข | ปุ่ม + (ฝั่งขวา)
    col_name, col_minus, col_qty, col_plus = st.columns([5, 1, 1, 1])

    with col_name:
        st.write(f"**{item['name']}** ({item['price']} บาท)")

    with col_minus:
        if st.button("➖", key=f"sub_{item_id}", use_container_width=True):
            if item_id in st.session_state.cart:
                st.session_state.cart[item_id] -= 1
                if st.session_state.cart[item_id] <= 0:
                    del st.session_state.cart[item_id]
                st.session_state.order_confirmed = False  # รีเซ็ตการยืนยันเมื่อมีการเปลี่ยนแปลง
                st.rerun()

    with col_qty:
        st.markdown(f"<div style='text-align: center; font-weight: bold; line-height: 2.2;'>{qty}</div>", unsafe_allow_html=True)

    with col_plus:
        if st.button("➕", key=f"add_{item_id}", use_container_width=True):
            st.session_state.cart[item_id] = qty + 1
            st.session_state.order_confirmed = False  # รีเซ็ตการยืนยันเมื่อมีการเปลี่ยนแปลง
            st.rerun()

st.divider()

# คำนวณราคารวมเบื้องต้น
temp_total = sum(item["price"] * st.session_state.cart[item["id"]] for item in menu_data if item["id"] in st.session_state.cart)

if temp_total > 0:
    st.write(f"### ราคารวมเบื้องต้น: **{temp_total}** บาท")
    
    # ปุ่มยืนยันรายการอาหาร
    if st.button("✅ ยืนยันรายการอาหาร", type="primary", use_container_width=True):
        st.session_state.order_confirmed = True
        st.rerun()
else:
    st.info("กรุณาเลือกรายการอาหาร")

# แสดงใบเสร็จเมื่อกด "ยืนยันรายการอาหาร" เท่านั้น
if st.session_state.order_confirmed and temp_total > 0:
    st.divider()
    st.subheader("🧾 บิลใบเสร็จรับเงิน")
    
    final_total = 0
    for item in menu_data:
        item_id = item["id"]
        if item_id in st.session_state.cart:
            item_qty = st.session_state.cart[item_id]
            subtotal = item_qty * item["price"]
            final_total += subtotal
            st.write(f"• {item['name']} x {item_qty} = {subtotal} บาท")

    st.divider()
    st.markdown(f"### ยอดรวมสุทธิ: **{final_total}** บาท")
    st.caption("ขอบคุณที่อุดหนุนค่ะ!")
    ่อุดหนุนค่ะ!")
    

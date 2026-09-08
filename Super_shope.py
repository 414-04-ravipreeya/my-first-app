import streamlit as st

# 1. ข้อมูลเมนู
menu_data = [
    {"id": 1, "name": "Latte", "price": 55},
    {"id": 2, "name": "Flat White", "price": 60},
    {"id": 3, "name": "Popcorn Latte", "price": 65},
    {"id": 4, "name": "Americano", "price": 50},
    {"id": 5, "name": "Tiramisu", "price": 85},
    {"id": 6, "name": "Banoffee Pie", "price": 75},
    {"id": 7, "name": "Blueberry Cake", "price": 80},
]

# 2. ตัวแปรเก็บตะกร้าสินค้าใน Session State ของ Streamlit
if "cart" not in st.session_state:
    st.session_state.cart = {}

st.title("☕ ร้านกาแฟ Super Shop")

# 3. แสดงรายการเมนูให้กดสั่งซื้อ
st.subheader("📋 รายการเมนู")
for item in menu_data:
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.write(f"**{item['name']}** ({item['price']} บาท)")
    with col2:
        if st.button("➕ เพิ่ม", key=f"add_{item['id']}"):
            st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
            st.rerun()
    with col3:
        if st.button("➖ ลด", key=f"remove_{item['id']}"):
            if item['id'] in st.session_state.cart:
                st.session_state.cart[item['id']] -= 1
                if st.session_state.cart[item['id']] <= 0:
                    del st.session_state.cart[item['id']]
                st.rerun()

st.divider()

# 4. ส่วนของใบเสร็จรับเงิน (แทนที่ HTML เดิม)
st.subheader("🧾 บิลใบเสร็จรับเงิน")

total_price = 0
has_items = False

for item in menu_data:
    item_id = item["id"]
    if item_id in st.session_state.cart and st.session_state.cart[item_id] > 0:
        qty = st.session_state.cart[item_id]
        subtotal = qty * item["price"]
        total_price += subtotal
        st.write(f"{item['name']} x {qty} = {subtotal} บาท")
        has_items = True

if not has_items:
    st.info("ยังไม่มีรายการที่เลือก")
else:
    st.divider()
    st.markdown(f"### ยอดรวมสุทธิ: **{total_price}** บาท")
    st.caption("ขอบคุณที่อุดหนุนค่ะ!")
    

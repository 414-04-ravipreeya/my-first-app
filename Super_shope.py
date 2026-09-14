import re
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

# กำหนด Session State สำหรับเก็บข้อมูล
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "step" not in st.session_state:
    st.session_state.step = "cart"  # สถาณะ: 'cart', 'member_ask', 'receipt'
if "phone_number" not in st.session_state:
    st.session_state.phone_number = None


# ฟังก์ชันสร้างหน้าต่างบิลเด้งกลางหน้าจอ (Modal Dialog)
@st.dialog("🧾 บิลใบเสร็จรับเงิน")
def show_receipt(selected_items, total_price):
    if st.session_state.phone_number:
        st.success(f"📱 สมาชิก: {st.session_state.phone_number}")

    for item in selected_items:
        st.write(
            f"• **{item['name']}** x {item['qty']} = {item['subtotal']} บาท"
        )

    # เงื่อนไขโปรโมชัน: ซื้อครบ 350 แถมน้ำราคา 65 บาท 1 แก้ว
    if total_price >= 350:
        st.info("🎉 **โปรโมชันพิเศษ:** ซื้อครบ 350 บาท รับฟรี! เครื่องดื่มราคา 65 บาท 1 แก้ว")

    st.divider()
    st.markdown(f"### ยอดรวมสุทธิ: **{total_price}** บาท")
    st.caption("ขอบคุณที่อุดหนุนค่ะ! 🙏")

    if st.button("ปิดหน้าต่าง / สั่งซื้อใหม่", use_container_width=True):
        st.session_state.cart = {}  # ล้างตะกร้าเมื่อปิดบิล
        st.session_state.step = "cart"
        st.session_state.phone_number = None
        st.rerun()


# ฟังก์ชัน Popup ถามการสมัครสมาชิก
@st.dialog("👤 สมัครสมาชิก")
def show_member_dialog(selected_items, total_price):
    st.write("คุณต้องการสมัครสมาชิกเพื่อสะสมแต้มและรับสิทธิประโยชน์หรือไม่?")
    st.caption("📌 **เงื่อนไข:** ซื้อครบ 350 บาท แถมน้ำราคา 65 บาท 1 แก้ว")

    phone_input = st.text_input(
        "กรุณากรอกเบอร์โทรศัพท์ (10 หลัก)",
        max_chars=10,
        placeholder="08X1234567",
    )

    col_confirm, col_cancel = st.columns(2)

    with col_confirm:
        if st.button("ยืนยัน", type="primary", use_container_width=True):
            # ตรวจสอบว่าเป็นตัวเลขและมีความยาว 10 หลัก
            if (
                phone_input
                and len(phone_input) == 10
                and phone_input.isdigit()
            ):
                st.session_state.phone_number = phone_input
                st.session_state.step = "receipt"
                st.toast("สมัครสมาชิกสำเร็จ! 🎉", icon="✅")
                st.rerun()
            else:
                st.error("❌ มีข้อผิดพลาด: กรุณาใส่เบอร์โทรศัพท์ให้ครบ 10 หลัก (เฉพาะตัวเลข)")

    with col_cancel:
        if st.button("ข้าม / ไม่สมัคร", use_container_width=True):
            st.session_state.phone_number = None
            st.session_state.step = "receipt"
            st.rerun()


st.title("☕ cafe super shop🍰☕")
st.subheader("📋 รายการเมนู")

# 1. แสดงรายการเมนู
for item in menu:
    i_id, qty = item["id"], st.session_state.cart.get(item["id"], 0)
    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])

    col1.write(f"**{item['name']}** ({item['price']} บาท)")
    if col2.button("➕", key=f"+{i_id}", use_container_width=True):
        st.session_state.cart[i_id] = qty + 1
        st.rerun()

    col3.markdown(
        f"<div style='text-align: center; font-weight: bold;'>{qty}</div>",
        unsafe_allow_html=True,
    )

    if (
        col4.button("➖", key=f"-{i_id}", use_container_width=True)
        and i_id in st.session_state.cart
    ):
        st.session_state.cart[i_id] -= 1
        if st.session_state.cart[i_id] <= 0:
            del st.session_state.cart[i_id]
        st.rerun()

st.divider()

# 2. คำนวณสรุปรายการที่เลือก
selected_items = [
    {
        **item,
        "qty": st.session_state.cart[item["id"]],
        "subtotal": item["price"] * st.session_state.cart[item["id"]],
    }
    for item in menu
    if st.session_state.cart.get(item["id"], 0) > 0
]
total_price = sum(item["subtotal"] for item in selected_items)

# 3. แสดงสรุปรายการและปุ่มยืนยัน
if selected_items:
    st.markdown("### 🛒 รายการที่เลือก")
    for item in selected_items:
        st.write(f"• {item['name']} x {item['qty']} = {item['subtotal']} บาท")

    st.markdown(f"## Total : **{total_price}** บาท")

    if st.button("✅ ยืนยันเมนู", type="primary", use_container_width=True):
        st.session_state.step = "member_ask"
        st.rerun()
else:
    st.info("กรุณาเลือกรายการอาหาร")

# ควบคุมการแสดง Dialog ตามสถานะ Step
if st.session_state.step == "member_ask":
    show_member_dialog(selected_items, total_price)
elif st.session_state.step == "receipt":
    show_receipt(selected_items, total_price)
    

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

# 1. ระบบบันทึกข้อมูล Session State
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "step" not in st.session_state:
    st.session_state.step = "cart"
if "current_phone" not in st.session_state:
    st.session_state.current_phone = None
if "owner_logged_in" not in st.session_state:
    st.session_state.owner_logged_in = False

# บันทึกข้อมูลตะกร้าชั่วคราวขณะออกบิล
if "checkout_items" not in st.session_state:
    st.session_state.checkout_items = []
if "checkout_total" not in st.session_state:
    st.session_state.checkout_total = 0

# ฐานข้อมูลจำลองสำหรับเก็บข้อมูลสมาชิก { "เบอร์โทร": ยอดสะสม }
if "members_db" not in st.session_state:
    st.session_state.members_db = {}


# ฟังก์ชันหน้าต่างบิลใบเสร็จ
@st.dialog("🧾 บิลใบเสร็จรับเงิน")
def show_receipt():
    phone = st.session_state.current_phone
    selected_items = st.session_state.checkout_items
    total_price = st.session_state.checkout_total

    # แสดงเฉพาะกรณีที่เป็นสมาชิก
    if phone and phone in st.session_state.members_db:
        accumulated_total = st.session_state.members_db[phone]
        st.success(f" เบอร์สมาชิก: **{phone}**")
        st.info(
            f" ยอดซื้อครั้งนี้: **{total_price}** บาท |  ยอดสั่งซื้อสะสมทั้งหมด: **{accumulated_total}** บาท"
        )
        st.divider()

    for item in selected_items:
        st.write(
            f"• **{item['name']}** x {item['qty']} = {item['subtotal']} บาท"
        )

    if total_price >= 350:
        st.info("🎉 **โปรโมชันพิเศษ:** ซื้อครบ 350 บาท รับฟรี! เครื่องดื่มราคา 65 บาท 1 แก้ว")

    st.divider()
    st.markdown(f"### ยอดรวมสุทธิ: **{total_price}** บาท")
    st.caption("ขอบคุณที่อุดหนุนค่ะ! 🙏")

    if st.button("ปิดหน้าต่าง / สั่งซื้อใหม่", use_container_width=True):
        st.session_state.cart = {}
        st.session_state.checkout_items = []
        st.session_state.checkout_total = 0
        st.session_state.step = "cart"
        st.session_state.current_phone = None
        st.rerun()


# ฟังก์ชัน Popup สมัคร/เข้าสู่ระบบสมาชิก
@st.dialog("👤 ระบบสมาชิก")
def show_member_dialog():
    total_price = st.session_state.checkout_total

    st.write("กรอกเบอร์โทรศัพท์เพื่อสะสมยอดซื้อ")
    st.caption("📌 **เงื่อนไข:** ซื้อครบ 350 บาท แถมน้ำราคา 65 บาท 1 แก้ว")

    phone_input = st.text_input(
        "กรุณากรอกเบอร์โทรศัพท์ (10 หลัก)",
        max_chars=10,
        placeholder="08X1234567",
    )

    col_confirm, col_cancel = st.columns(2)

    with col_confirm:
        if st.button("ยืนยัน", type="primary", use_container_width=True):
            if (
                phone_input
                and len(phone_input) == 10
                and phone_input.isdigit()
            ):
                st.session_state.current_phone = phone_input

                # บันทึกหรืออัปเดตยอดสั่งซื้อสะสมลงใน Database จำลอง
                if phone_input not in st.session_state.members_db:
                    st.session_state.members_db[phone_input] = total_price
                    st.toast("สมัครสมาชิกสำเร็จ! 🎉", icon="✅")
                else:
                    st.session_state.members_db[phone_input] += total_price
                    st.toast("สะสมยอดซื้อเรียบร้อย! 📈", icon="👍")

                st.session_state.step = "receipt"
                st.rerun()
            else:
                st.error("❌ กรุณาใส่เบอร์โทรศัพท์ให้ครบ 10 หลัก (เฉพาะตัวเลข)")

    with col_cancel:
        if st.button("ไม่สมัครสมาชิก", use_container_width=True):
            # ตั้งค่าให้เบอร์โทรเป็น None เพื่อออกบิลลูกค้าธรรมดา
            st.session_state.current_phone = None
            st.session_state.step = "receipt"
            st.rerun()


# หน้าจอหลัก UI
st.title("☕ cafe super shop🍰☕")
st.subheader("📋 รายการเมนู")

# แสดงรายการเมนู
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

# คำนวณสรุปรายการที่เลือก
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

if selected_items:
    st.markdown("### 🛒 รายการที่เลือก")
    for item in selected_items:
        st.write(f"• {item['name']} x {item['qty']} = {item['subtotal']} บาท")

    st.markdown(f"## Total : **{total_price}** บาท")

    if st.button("✅ ยืนยันเมนู", type="primary", use_container_width=True):
        # บันทึกข้อมูลเข้า Session State ก่อนเปลี่ยนหน้า Popup
        st.session_state.checkout_items = selected_items
        st.session_state.checkout_total = total_price
        st.session_state.step = "member_ask"
        st.rerun()
else:
    st.info("กรุณาเลือกรายการอาหาร")

# แสดงผล Popup ตามสถานะ
if st.session_state.step == "member_ask":
    show_member_dialog()
elif st.session_state.step == "receipt":
    show_receipt()

# -------------------------------------------------------------
# 🔐 ส่วนแสดงตารางข้อมูลสมาชิก (มีปุ่มยืนยันรหัส)
# -------------------------------------------------------------
st.write("---")
with st.expander("🔐 สำหรับเจ้าของร้าน (ตรวจสอบข้อมูลสมาชิก)"):
    if not st.session_state.owner_logged_in:
        password_input = st.text_input("กรุณากรอกรหัสผ่าน", type="password", key="owner_pass_input")
        if st.button("🔑 ยืนยันรหัส", use_container_width=True):
            if password_input == "1047":
                st.session_state.owner_logged_in = True
                st.rerun()
            else:
                st.error("❌ รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
    else:
        st.success("🔓 เข้าสู่ระบบเจ้าของร้านสำเร็จ")
        if st.session_state.members_db:
            st.markdown("### 📊 รายชื่อสมาชิกและยอดสั่งซื้อสะสม")
            for phone, total in st.session_state.members_db.items():
                st.write(f"📱 เบอร์: `{phone}` | 💵 ยอดสะสมทั้งหมด: **{total}** บาท")
        else:
            st.info("ยังไม่มีข้อมูลสมาชิกในระบบ")
        
        if st.button("🔒 ออกจากระบบเจ้าของร้าน", use_container_width=True):
            st.session_state.owner_logged_in = False
            st.rerun()
                

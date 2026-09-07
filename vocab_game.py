import time
import streamlit as st

st.title("⏱️ เกมเติมศัพท์จับเวลา")

# 1. กำหนดค่าเริ่มต้นใน session_state
if "start" not in st.session_state:
    st.session_state.start = None
if "is_ended" not in st.session_state:
    st.session_state.is_ended = False


# 📌 ฟังก์ชันเริ่มเกมใหม่ (รีเซ็ตค่าคำตอบทั้ง 4 ข้อ)
def reset_game():
    st.session_state.ans1 = ""
    st.session_state.ans2 = ""
    st.session_state.ans3 = ""
    st.session_state.ans4 = ""
    st.session_state.start = time.time()  # บันทึกเวลาเริ่มต้น
    st.session_state.is_ended = False  # รีเซ็ตสถานะเกม


# ----------------------------------------------------
# 📌 ฟังก์ชันแสดง Dialog สรุปผล
# ----------------------------------------------------
@st.dialog("📊 สรุปผลการเล่นเกม")
def show_result_dialog():
    st.balloons()
    score = 0

    # ดึงค่าและแปลงเป็นตัวพิมพ์เล็ก
    u_ans1 = st.session_state.get("ans1", "").strip().lower()
    u_ans2 = st.session_state.get("ans2", "").strip().lower()
    u_ans3 = st.session_state.get("ans3", "").strip().lower()
    u_ans4 = st.session_state.get("ans4", "").strip().lower()

    # ตรวจข้อ 1
    if u_ans1 == "apple":
        st.success("✅ ข้อ 1: ถูกต้อง")
        score += 1
    else:
        st.error(f"❌ ข้อ 1: ยังไม่ถูกต้อง (คุณตอบ '{u_ans1}')")

    # ตรวจข้อ 2
    if u_ans2 == "fish":
        st.success("✅ ข้อ 2: ถูกต้อง")
        score += 1
    else:
        st.error(f"❌ ข้อ 2: ยังไม่ถูกต้อง (คุณตอบ '{u_ans2}')")

    # ตรวจข้อ 3 (เพิ่มใหม่)
    if u_ans3 == "banana":
        st.success("✅ ข้อ 3: ถูกต้อง")
        score += 1
    else:
        st.error(f"❌ ข้อ 3: ยังไม่ถูกต้อง (คุณตอบ '{u_ans3}')")

    # ตรวจข้อ 4 (เพิ่มใหม่)
    if u_ans4 == "monkey":
        st.success("✅ ข้อ 4: ถูกต้อง")
        score += 1
    else:
        st.error(f"❌ ข้อ 4: ยังไม่ถูกต้อง (คุณตอบ '{u_ans4}')")

    st.info(f"🏆 ได้คะแนนรวม: {score} / 4 คะแนน")

    # เงื่อนไขชนะ (ต้องได้เต็ม 4 คะแนน)
    if score == 4:
        st.success("🎉 You win!")
    else:
        st.error("💀 You lose!")


# ----------------------------------------------------
# Main UI Logic
# ----------------------------------------------------
st.button("🎮 เริ่มเล่นเกม", on_click=reset_game)

# คำนวณเวลาที่เหลือ
time_left = 0
if st.session_state.start and not st.session_state.is_ended:
    elapsed = time.time() - st.session_state.start
    time_left = max(0, int(30 - elapsed))

    if time_left == 0:
        st.session_state.is_ended = True
    else:
        st.error(f"⏳ เหลือเวลา: {time_left} วินาที")

st.divider()

# ช่องกรอกคำตอบ (ข้อ 1-4)
st.text_input(
    "ข้อ 1: An `a _ _ l e` a day keeps the doctor away. 🍎",
    key="ans1",
    disabled=st.session_state.is_ended or st.session_state.start is None,
)

st.text_input(
    "ข้อ 2: Cats love to eat `f _ s h`. 🐟",
    key="ans2",
    disabled=st.session_state.is_ended or st.session_state.start is None,
)

# คำศัพท์ที่เพิ่มใหม่
st.text_input(
    "ข้อ 3: Monkeys love to eat `b _ n _ n a`. 🍌",
    key="ans3",
    disabled=st.session_state.is_ended or st.session_state.start is None,
)

st.text_input(
    "ข้อ 4: A `m _ n k e y` is swinging on the tree. 🐒",
    key="ans4",
    disabled=st.session_state.is_ended or st.session_state.start is None,
)

# ปุ่มส่งคำตอบ
if st.session_state.start and not st.session_state.is_ended:
    if st.button("📥 ส่งคำตอบ"):
        st.session_state.is_ended = True
        st.rerun()

# แสดง Dialog สรุปผลลัพธ์
if st.session_state.is_ended and st.session_state.start is None:
    pass
elif st.session_state.is_ended:
    show_result_dialog()

st.divider()
st.write("นางสาวรวิปรียา พรมมา เลขที่ 4 ม.4/14")

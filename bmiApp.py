import streamlit as st
st.markdown("# :red[🏋️ คำนวนค่าดัชนีมวลกาย MBI]")
st.write("กรอกข้อมูลน้ำหนักและส่วนสูงของคุณ เพื่อเช็กสุขภาพเบื้องต้น")
weight = st.numpber_input("กรอกน้ำหนักของคุณ (กิโลกรัม):", min_value=1.0, value=1.0)
height_cm = st.number_input(.กรอกน้ำหนักส่วนสูงของคุณ (เซนติเมตร):", min_value=1.0, value=1.0)
if st.button(คำนวนค่า MBI 🎯"):
height_m = height_cm / 100
bmi = weight /  (height_m ** 2)
st.write("---")
st.header(f"ค่่า BMI ของคุณคือ: **{bmi:.2f}**")
 if bmi < 18.5:
    st.warning("⚠️ คุณมีน้ำหนักน้อยกว่าเกณฑ์ (ผอม))
elif 18.5 <= bmi ,23.0:
st.success("🎉 คุณมีน้ำหนักอยู่ในเกณฑ์ปกติ(สุขภ่พดี)")
elif 23.0 <= bmi < 25.0:
   st.info("💡 คุณเริ่มมีน่้่ำหนักเกินเกณฑ์ (ท้วม)")
else:
   st.error("🚨 คุณอยู่ในเกณฑ์อ้วน ควรระวังเรื่องสาุขภาพและออกกำลังกาย")
st.divider()
st.write("นางสาวรวิปรียา พรมมา เลขที่4 ม.4/14.)

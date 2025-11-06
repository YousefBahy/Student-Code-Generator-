import streamlit as st
from PIL import Image
import os
import string

# ===================== إعدادات الواجهة =====================
st.set_page_config(page_title="نظام توليد أكواد اللجان", page_icon="🧾", layout="centered")

# تطبيق النمط الغامق
st.markdown("""
    <style>
        body {background-color: #0E1117; color: white;}
        .main {background-color: #0E1117;}
        .stTextInput, .stNumberInput, .stButton>button {
            background-color: #262730 !important;
            color: white !important;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #4C4F69 !important;
        }
        .card {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0px 0px 10px rgba(255,255,255,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ===================== الشعار والعنوان =====================
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("alex_logo.png"):
        st.image("alex_logo.png", width=100)
with col2:
    st.markdown("<h2 style='text-align:right; color:#1DB954;'>نظام توليد أكواد اللجان</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:right; color:gray;'>إعداد: يوسف باهي – المعيد بقسم إدارة الأعمال، كلية الأعمال، جامعة الإسكندرية</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #555;'>", unsafe_allow_html=True)

# ===================== إدخال بيانات اللجان =====================
st.markdown("### 👇 أدخل بيانات اللجان:")

committees = []
num_committees = st.number_input("عدد اللجان:", min_value=1, max_value=50, step=1)

for i in range(num_committees):
    with st.expander(f"🧮 اللجنة رقم {i+1}"):
        name = st.text_input(f"اسم اللجنة {i+1}:", key=f"name_{i}")
        count = st.number_input(f"عدد الطلاب في لجنة {i+1}:", min_value=0, step=1, key=f"count_{i}")
        committees.append({"name": name, "count": count})


# ===================== دالة توليد الرموز الأبجدية =====================
def get_letter_code(index):
    letters = string.ascii_uppercase
    if index < 26:
        return letters[index]
    else:
        first = (index // 26) - 1
        second = index % 26
        return letters[first] + letters[second]


# ===================== الزر والتوليد =====================
if st.button("🔢 توليد الأكواد"):
    all_codes_summary = {}
    global_counter = 0

    for committee in committees:
        committee_name = committee['name']
        num_students = int(committee['count'])
        committee_codes = []

        for i in range(1, num_students + 1):
            global_counter += 1
            # تحديد مجموعة الحروف (A, B, ..., Z, AA, AB, ...)
            letter_index = (global_counter - 1) // 100
            current_letter = get_letter_code(letter_index)
            serial_number = (global_counter - 1) % 100 + 1
            student_code = f"{serial_number}{current_letter}"
            committee_codes.append(student_code)

        # تحليل النطاقات
        ranges = []
        if committee_codes:
            current_start = committee_codes[0]
            current_letter = current_start.lstrip('0123456789')
            for i in range(1, len(committee_codes)):
                next_code = committee_codes[i]
                next_letter = next_code.lstrip('0123456789')
                if next_letter != current_letter:
                    ranges.append(f"{current_start} to {committee_codes[i-1]}")
                    current_start = next_code
                    current_letter = next_letter
            ranges.append(f"{current_start} to {committee_codes[-1]}")

        all_codes_summary[committee_name] = {"count": num_students, "ranges": ranges}

    # ===================== عرض النتائج =====================
    st.markdown("## ✅ ملخص الأكواد")
    total = 0
    for name, data in all_codes_summary.items():
        total += data["count"]
        st.markdown(f"<div class='card'><h4>📋 {name}</h4><p>عدد الطلاب: {data['count']}</p><p>نطاقات الأكواد:</p>", unsafe_allow_html=True)
        for r in data['ranges']:
            st.markdown(f"- {r}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.success(f"الإجمالي الكلي لجميع اللجان: {total} طالب")
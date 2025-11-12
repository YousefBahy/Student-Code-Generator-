import streamlit as st
from PIL import Image
import os
import string
import re

# ===================== إعدادات الصفحة =====================
st.set_page_config(page_title="نظام توليد أكواد اللجان", page_icon="🧾", layout="centered")

# ===================== تنسيق النمط الغامق والاتجاه =====================
st.markdown("""
    <style>
        body {background-color: #0E1117; color: white; direction: rtl; text-align: right;}
        .main {background-color: #0E1117; direction: rtl; text-align: right;}
        h1, h2, h3, h4, p, label, div {direction: rtl; text-align: right;}
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
            direction: rtl;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

# ===================== الشعار والعنوان =====================
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("alex_logo.png"):
        st.image("alex_logo.png", width=100)
with col2:
    st.markdown("<h2 style='color:#1DB954;'>نظام توليد أكواد اللجان</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray;'>إعداد: يوسف باهي – المعيد بقسم إدارة الأعمال، كلية الأعمال، جامعة الإسكندرية</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #555;'>", unsafe_allow_html=True)

# ===================== اختيار اللغة =====================
lang = st.radio("اختر نوع الحروف:", ["إنجليزية (A, B, C...)", "عربية (أ، ب، ت...)"], horizontal=True)

# ===================== إدخال الكود السابق =====================
st.markdown("### 🧾 أدخل آخر كود تم الوصول إليه (اختياري):")
last_code_input = st.text_input("مثال: 57C أو A57 أو ١٠٠ز أو ز١٠٠").strip()

# ===================== إعدادات الحروف =====================
ARABIC_LETTERS = ["ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي"]

def convert_arabic_digits_to_english(text):
    """تحويل الأرقام العربية إلى إنجليزية"""
    return text.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))

def normalize_arabic_letters(text):
    """توحيد الأشكال المختلفة للألف"""
    return text.replace("إ", "ا").replace("أ", "ا").replace("آ", "ا")

def get_letter_code(index, lang):
    """توليد تسلسل الحروف: A-Z, AA... أو أ، ب، ت..."""
    if lang == "إنجليزية (A, B, C...)":
        letters = string.ascii_uppercase
    else:
        letters = ARABIC_LETTERS
    result = ""
    while True:
        result = letters[index % len(letters)] + result
        index = index // len(letters) - 1
        if index < 0:
            break
    return result

def parse_last_code(code, lang):
    """تحليل الكود الأخير"""
    if not code:
        return 0
    code = normalize_arabic_letters(convert_arabic_digits_to_english(code)).replace(" ", "").upper()

    match = re.match(r"([A-Zا-ي]+)(\d+)$", code)
    if not match:
        match = re.match(r"(\d+)([A-Zا-ي]+)$", code)
    if not match:
        return 0

    letters, number = (match.group(1), int(match.group(2))) if match.group(1).isalpha() else (match.group(2), int(match.group(1)))
    letter_index = 0

    if lang == "إنجليزية (A, B, C...)":
        letters = letters.upper()
        for c in letters:
            letter_index = letter_index * 26 + (ord(c) - ord('A') + 1)
    else:
        letters = normalize_arabic_letters(letters)
        for c in letters:
            letter_index = letter_index * len(ARABIC_LETTERS) + (ARABIC_LETTERS.index(c) + 1)

    letter_index -= 1
    return letter_index * 100 + number

# حساب بداية الترقيم
global_counter = parse_last_code(last_code_input, lang)

# ===================== إدخال بيانات اللجان =====================
st.markdown("### 👇 أدخل بيانات اللجان:")

committees = []
num_committees = st.number_input("عدد اللجان:", min_value=1, max_value=50, step=1)
for i in range(num_committees):
    with st.expander(f"📋 اللجنة رقم {i+1}"):
        name = st.text_input(f"اسم اللجنة {i+1}:", key=f"name_{i}")
        count = st.number_input(f"عدد الطلاب في لجنة {i+1}:", min_value=0, step=1, key=f"count_{i}")
        if not name.strip():
            name = f"لجنة {i+1}"
        committees.append({"name": name, "count": count})

# ===================== التوليد =====================
if st.button("🔢 توليد الأكواد"):
    all_codes_summary = {}
    for committee in committees:
        committee_name = committee["name"]
        num_students = int(committee["count"])
        committee_codes = []

        for _ in range(num_students):
            global_counter += 1
            letter_index = (global_counter - 1) // 100
            current_letter = get_letter_code(letter_index, lang)
            serial_number = (global_counter - 1) % 100 + 1
            student_code = f"{serial_number}{current_letter}" if lang == "إنجليزية (A, B, C...)" else f"{current_letter}{serial_number}"
            committee_codes.append(student_code)

        ranges = []
        if committee_codes:
            current_start = committee_codes[0]
            current_letter = ''.join([c for c in current_start if c.isalpha()])
            for i in range(1, len(committee_codes)):
                next_code = committee_codes[i]
                next_letter = ''.join([c for c in next_code if c.isalpha()])
                if next_letter != current_letter:
                    separator = "to" if lang == "إنجليزية (A, B, C...)" else "إلى"
                    ranges.append(f"{current_start} {separator} {committee_codes[i-1]}")
                    current_start = next_code
                    current_letter = next_letter
            separator = "to" if lang == "إنجليزية (A, B, C...)" else "إلى"
            ranges.append(f"{current_start} {separator} {committee_codes[-1]}")

        all_codes_summary[committee_name] = {"count": num_students, "ranges": ranges}

    # ===================== عرض النتائج =====================
    st.markdown("## ✅ ملخص الأكواد")
    total = 0
    for name, data in all_codes_summary.items():
        total += data["count"]
        st.markdown(
            f"<div class='card'><h4>📋 {name}</h4><p>عدد الطلاب: {data['count']}</p><p>نطاقات الأكواد:</p>",
            unsafe_allow_html=True)
        for r in data['ranges']:
            st.markdown(f"- {r}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.success(f"الإجمالي الكلي لجميع اللجان: {total} طالب")
    st.info(f"📍 تم البدء من بعد الكود: {last_code_input or 'لم يُدخل كود سابق'}")
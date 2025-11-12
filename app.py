import streamlit as st
from PIL import Image
import os
import string
import re

# ===================== إعدادات الواجهة =====================
st.set_page_config(page_title="نظام توليد أكواد اللجان", page_icon="🧾", layout="centered")

# تطبيق النمط الغامق
st.markdown("""
    <style>
        body {background-color: #0E1117; color: white;}
        .main {background-color: #0E1117;}
        .stTextInput, .stNumberInput, .stSelectbox, .stButton>button {
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

# ===================== اختيار نوع الحروف =====================
st.markdown("### ⚙️ اختر نوع الحروف:")
letter_type = st.selectbox("نوع الحروف المستخدمة:", ["إنجليزية", "عربية"])

# ===================== إدخال بيانات اللجان =====================
st.markdown("### 👇 أدخل بيانات اللجان:")

last_code_input = st.text_input("أدخل آخر كود تم الوصول إليه (اختياري):", placeholder="مثال: 57C أو A57 أو ١٠٠Z")

# ---------- تحويل الأرقام العربية إلى الإنجليزية ----------
def convert_arabic_digits_to_english(text):
    arabic_to_english = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    return text.translate(arabic_to_english)

# ---------- الحروف ----------
AR_LETTERS = ["أ","ب","ج","د","هـ","و","ز","ح","ط","ي","ك","ل","م","ن","س","ع","ف","ص","ق","ر","ش","ت","ث","خ","ذ","ض"]
EN_LETTERS = list(string.ascii_uppercase)

# ---------- توليد تسلسل الحروف ----------
def get_letter_code(index, arabic=False):
    letters = AR_LETTERS if arabic else EN_LETTERS
    base = len(letters)
    result = ""
    while True:
        result = letters[index % base] + result
        index = index // base - 1
        if index < 0:
            break
    return result

# ---------- تحليل الكود الأخير ----------
def parse_last_code(code):
    if not code:
        return 0
    code = convert_arabic_digits_to_english(code)
    code = code.strip().replace(" ", "").upper()

    match = re.match(r"^([A-Z\u0621-\u064A]+)(\d+)$", code)
    if not match:
        match = re.match(r"^(\d+)([A-Z\u0621-\u064A]+)$", code)
    if not match:
        return 0

    part1, part2 = match.group(1), match.group(2)
    if part1[0].isalpha():
        letters, number = part1, int(part2)
    else:
        number, letters = int(part1), part2

    letter_index = 0
    if all('A' <= c <= 'Z' for c in letters):
        for c in letters:
            letter_index = letter_index * 26 + (ord(c) - ord('A') + 1)
    else:
        for c in letters:
            if c in AR_LETTERS:
                letter_index = letter_index * len(AR_LETTERS) + (AR_LETTERS.index(c) + 1)
            else:
                letter_index = letter_index * len(AR_LETTERS)
    letter_index -= 1
    return letter_index * 100 + number

# ---------- تحديد البداية ----------
start_counter = parse_last_code(last_code_input)

# ---------- إدخال اللجان ----------
committees = []
num_committees = st.number_input("عدد اللجان:", min_value=1, max_value=50, step=1)

for i in range(num_committees):
    with st.expander(f"🧮 اللجنة رقم {i+1}"):
        name = st.text_input(f"اسم اللجنة {i+1}:", key=f"name_{i}")
        count = st.number_input(f"عدد الطلاب في لجنة {i+1}:", min_value=0, step=1, key=f"count_{i}")
        if not name.strip():
            name = f"لجنة {i+1}"
        committees.append({"name": name, "count": count})

# ===================== توليد الأكواد =====================
if st.button("🔢 توليد الأكواد"):
    counter = start_counter
    arabic_mode = (letter_type == "عربية")
    connector = "إلى" if arabic_mode else "to"
    all_codes_summary = {}

    for committee in committees:
        committee_name = committee['name']
        num_students = int(committee['count'])
        committee_codes = []

        for _ in range(num_students):
            counter += 1
            letter_index = (counter - 1) // 100
            current_letter = get_letter_code(letter_index, arabic=arabic_mode)
            serial_number = (counter - 1) % 100 + 1
            student_code = f"{serial_number}{current_letter}"
            committee_codes.append(student_code)

        # إنشاء النطاقات
        ranges = []
        if committee_codes:
            def extract_letters(s):
                return ''.join([ch for ch in s if ch.isalpha() or ch in AR_LETTERS])
            current_start = committee_codes[0]
            current_letter = extract_letters(current_start)
            for i in range(1, len(committee_codes)):
                next_code = committee_codes[i]
                next_letter = extract_letters(next_code)
                if next_letter != current_letter:
                    ranges.append(f"{current_start} {connector} {committee_codes[i-1]}")
                    current_start = next_code
                    current_letter = next_letter
            ranges.append(f"{current_start} {connector} {committee_codes[-1]}")

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
    st.info(f"📍 تم البدء من بعد الكود: {last_code_input or 'لم يُدخل كود سابق'}")
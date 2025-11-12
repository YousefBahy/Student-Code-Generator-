import streamlit as st
import string
import re

# ===================== إعداد الصفحة =====================
st.set_page_config(page_title="نظام توليد أكواد اللجان", page_icon="🧾", layout="centered")

# ===================== تنسيق واجهة غامقة RTL =====================
st.markdown("""
    <style>
        body, .main, .block-container {
            direction: rtl;
            text-align: right;
            background-color: #0E1117;
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, label {
            direction: rtl;
            text-align: right;
        }
        .stTextInput, .stNumberInput, .stButton>button, .stSelectbox {
            background-color: #262730 !important;
            color: white !important;
            border-radius: 8px !important;
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

# ===================== العنوان الرئيسي =====================
st.markdown("<h2 style='color:#1DB954;'>🧾 نظام توليد أكواد اللجان</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:gray;'>إعداد: يوسف باهي – المعيد بقسم إدارة الأعمال، كلية الأعمال، جامعة الإسكندرية</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #555;'>", unsafe_allow_html=True)

# ===================== دوال مساعدة =====================
def to_english_digits(s):
    """تحويل الأرقام العربية إلى إنجليزية"""
    return s.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))

AR_LETTERS = ["ا", "ب", "ج", "د", "هـ", "و", "ز", "ح", "ط", "ي", "ك", "ل", "م", "ن", "س", "ع", "ف", "ص", "ق", "ر", "ش", "ت", "ث", "خ", "ذ", "ض"]
EN_LETTERS = list(string.ascii_uppercase)

def get_letter_code(index, arabic=False):
    """توليد تسلسل الحروف"""
    letters = AR_LETTERS if arabic else EN_LETTERS
    base = len(letters)
    result = ""
    while True:
        result = letters[index % base] + result
        index = index // base - 1
        if index < 0:
            break
    return result

def parse_code(code, arabic=False):
    """تحليل آخر كود مكتوب"""
    if not code:
        return 0
    code = to_english_digits(code.strip().replace(" ", "").upper())
    code = code.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")

    match = re.match(r"^([A-Z\u0621-\u064A]+)(\d+)$", code)
    if not match:
        match = re.match(r"^(\d+)([A-Z\u0621-\u064A]+)$", code)
    if not match:
        return 0

    p1, p2 = match.groups()
    if p1[0].isalpha():
        letters, number = p1, int(p2)
    else:
        number, letters = int(p1), p2

    letters = [ch.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا") for ch in letters]
    lst = AR_LETTERS if arabic else EN_LETTERS
    base = len(lst)
    letter_index = 0
    for c in letters:
        letter_index = letter_index * base + (lst.index(c) + 1)
    return (letter_index - 1) * 100 + number

# ===================== إدخال البيانات =====================
letter_type = st.selectbox("نوع الحروف:", ["عربية", "إنجليزية"])
arabic_mode = (letter_type == "عربية")

last_code = st.text_input("أدخل آخر كود تم الوصول إليه:", placeholder="مثال: ٥٠ا أو A50")
num_committees = st.number_input("عدد اللجان:", 1, 50, 2)

committees = []
for i in range(num_committees):
    name = st.text_input(f"اسم اللجنة {i+1}:", f"لجنة {i+1}")
    count = st.number_input(f"عدد الطلاب في لجنة {i+1}:", 1, 300, 10, key=f"count_{i}")
    committees.append((name, count))

# ===================== توليد الأكواد =====================
if st.button("🔢 توليد الأكواد"):
    start_counter = parse_code(last_code, arabic_mode)
    connector = "إلى" if arabic_mode else "to"
    total = 0

    for name, count in committees:
        st.markdown(f"### 📋 {name}")
        total += count
        start_counter += 1
        start_num = start_counter
        for _ in range(count - 1):
            start_counter += 1
        end_num = start_counter

        start_letter = get_letter_code((start_num - 1)//100, arabic_mode)
        end_letter = get_letter_code((end_num - 1)//100, arabic_mode)
        start_serial = (start_num - 1) % 100 + 1
        end_serial = (end_num - 1) % 100 + 1

        if arabic_mode:
            result = f"<div dir='rtl' style='font-size:18px;'> {start_letter}{start_serial} {connector} {end_letter}{end_serial} </div>"
        else:
            result = f"{start_serial}{start_letter} {connector} {end_serial}{end_letter}"

        st.markdown(result, unsafe_allow_html=True)

    st.success(f"✅ تم توليد الأكواد بنجاح — المجموع الكلي: {total} طالب")
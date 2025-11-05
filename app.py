import streamlit as st 
from PIL import Image 
import os

==============================

إعدادات الصفحة والثيم

==============================

st.set_page_config(page_title="مولد أكواد اللجان - جامعة الإسكندرية", page_icon=None, layout="wide", initial_sidebar_state="collapsed")

مظهر غامق مخصص عبر CSS

dark_css = """

<style>
:root { color-scheme: dark; }
html, body, [class*="css"]  {
    background-color: #0f1720 !important;
    color: #e6eef8 !important;
}
.stApp { padding: 1rem 1.5rem; }
.header-row { display: flex; align-items: center; gap: 1rem; }
.app-title { font-size: 26px; font-weight:700; }
.app-subtitle { font-size: 13px; color: #9fb0c7; margin-top: -6px; }
.card { background: #0b1220; border: 1px solid #13202b; padding: 14px; border-radius: 12px; box-shadow: 0 4px 12px rgba(2,6,23,0.6); }
.card h3 { margin: 0 0 6px 0; }
.card small { color: #9fb0c7; }
.divider { height:1px; background:#10212b; margin:12px 0 18px 0; }
.footer { color: #9fb0c7; font-size:13px; }
.logo-img { max-width:140px; height:auto; }
.ranges pre { background: transparent; color: #d7eefc; border: none; padding:0; }
</style>""" st.markdown(dark_css, unsafe_allow_html=True)

==============================

دالة توليد الأكواد (معدلة للعمل مع الواجهة)

==============================

def generate_continuous_codes_detailed(committees_data): all_codes_summary = {} code_letter_start = ord('A') global_sheet_counter = 0

for committee in committees_data:
    committee_name = committee['name']
    num_students = committee['students_count']
    committee_codes = []

    for i in range(1, num_students + 1):
        global_sheet_counter += 1
        letter_index = (global_sheet_counter - 1) // 100
        current_letter_code = chr(code_letter_start + letter_index)
        serial_number_in_group = (global_sheet_counter - 1) % 100 + 1
        student_code = f"{serial_number_in_group}{current_letter_code}"
        committee_codes.append(student_code)

    ranges = []
    if not committee_codes:
        pass
    elif len(committee_codes) == 1:
        ranges.append(f"{committee_codes[0]}")
    else:
        current_range_start = committee_codes[0]
        current_letter = current_range_start[-1]

        for i in range(1, len(committee_codes)):
            next_code = committee_codes[i]
            next_letter = next_code[-1]
            if next_letter != current_letter:
                ranges.append(f"{current_range_start} To {committee_codes[i-1]}")
                current_range_start = next_code
                current_letter = next_letter

        ranges.append(f"{current_range_start} To {committee_codes[-1]}")

    all_codes_summary[committee_name] = {
        'count': num_students,
        'ranges': ranges,
        'codes': committee_codes
    }

return all_codes_summary

==============================

واجهة المستخدم بالعربية

==============================

محاولة تحميل شعار الجامعة إن وجد

LOGO_FILENAME = "alex_logo.png"  # ضع هنا ملف الشعار بنفس اسم الملف في المستودع logo = None if os.path.exists(LOGO_FILENAME): try: logo = Image.open(LOGO_FILENAME) except Exception: logo = None

رأس الصفحة: الشعار على اليسار والعنوان على اليمين (بالشكل العربي)

with st.container(): cols = st.columns([1, 6]) with cols[0]: if logo: st.image(logo, use_column_width=False, width=110, caption="") else: st.markdown("<div class='card' style='text-align:center; padding:10px;'>شعار الجامعة غير مرفوع</div>", unsafe_allow_html=True) with cols[1]: st.markdown("<div class='header-row' dir='rtl'>", unsafe_allow_html=True) st.markdown(f"<div style='text-align:right;'><div class='app-title'>نظام إنشاء أكواد أوراق إجابات الطلاب</div><div class='app-subtitle'>واجهة بسيطة لإنشاء أكواد متسلسلة ونطاقاتها</div></div>", unsafe_allow_html=True) st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

المدخلات: عدد اللجان وبيانات كل لجنة

st.markdown("<div dir='rtl'>", unsafe_allow_html=True) num_committees = st.number_input("كم عدد اللجان؟", min_value=1, step=1, value=1) committees_data = []

for i in range(int(num_committees)): st.markdown(f"<div class='card' dir='rtl' style='margin-bottom:12px;'>", unsafe_allow_html=True) st.markdown(f"<h3 style='text-align:right;'>اللجنة رقم {i+1}</h3>", unsafe_allow_html=True) name = st.text_input(f"اسم اللجنة {i+1}", key=f"name_{i}") count = st.number_input(f"عدد الطلاب في اللجنة {i+1}", min_value=0, step=1, key=f"count_{i}") committees_data.append({'name': name.strip(), 'students_count': int(count)}) st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

زر إنشاء الأكواد

if st.button("إنشاء الأكواد", type='primary'): if any(c['name'] == "" for c in committees_data): st.warning("⚠️ يرجى إدخال اسم لكل لجنة قبل المتابعة.") else: with st.spinner("جاري إنشاء الأكواد وتحليل النطاقات..."): result = generate_continuous_codes_detailed(committees_data)

st.success("✅ تم إنشاء الأكواد بنجاح!")

    # عرض النتائج: كل لجنة داخل بطاقة
    total_sheets = 0
    for committee_name, data in result.items():
        total_sheets += data['count']
        st.markdown("<div class='card' dir='rtl' style='margin-bottom:12px;'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:right;'>{committee_name} <small style='color:#9fb0c7;'>({data['count']} طالب)</small></h3>", unsafe_allow_html=True)

        # عرض نطاقات
        st.markdown("<div class='ranges' style='text-align:right;'>", unsafe_allow_html=True)
        if not data['ranges']:
            st.markdown("<small>لا توجد بيانات لعرضها.</small>", unsafe_allow_html=True)
        else:
            for r in data['ranges']:
                st.code(r)
        st.markdown("</div>", unsafe_allow_html=True)

        # زر لعرض كل الأكواد مفصّلة (اختياري)
        with st.expander("عرض كل الأكواد المفصلة لهذه اللجنة"):
            codes = data.get('codes', [])
            if codes:
                # عرض في صفوف منظمة
                rows = []
                for i in range(0, len(codes), 20):
                    rows.append(codes[i:i+20])
                for row in rows:
                    st.write("  ".join(row))
            else:
                st.write("لا توجد أكواد")

        st.markdown("</div>", unsafe_allow_html=True)

    st.info(f"الإجمالي الكلي لجميع اللجان: {total_sheets} ورقة")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

تذييل الصفحة: بيانات الإعداد

st.markdown("<div class='footer' dir='rtl' style='margin-top:18px;'>", unsafe_allow_html=True) st.markdown("<strong>إعداد:</strong> يوسف باهي – المعيد بقسم إدارة الأعمال، كلية الأعمال، جامعة الإسكندرية", unsafe_allow_html=True) st.markdown("</div>", unsafe_allow_html=True)

ملاحظة عن الشعار

st.markdown("<div style='color:#89a6c3; margin-top:12px;' dir='rtl'>ملاحظة: لإظهار شعار الجامعة، ضع ملف الصورة باسم <code>alex_logo.png</code> في نفس مجلد التطبيق.</div>", unsafe_allow_html=True)


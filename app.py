import streamlit as st

def generate_continuous_codes_detailed(committees_data):
    """
    توليد أكواد متسلسلة مستمرة لكل لجنة وعرض النطاقات بالتفصيل.
    """
    all_codes_summary = {}
    code_letter_start = ord('A')  # القيمة ASCII لحرف 'A'
    global_sheet_counter = 0

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
            'ranges': ranges
        }

    return all_codes_summary


# ==============================
# واجهة Streamlit
# ==============================

st.set_page_config(page_title="مولد أكواد اللجان", page_icon="🧾", layout="centered")

st.title("🧾 نظام إنشاء أكواد أوراق إجابات الطلاب")
st.markdown("مرحبًا بك في نظام إنشاء **أكواد متسلسلة مستمرة** مع عرض نطاقات التكويد بالتفصيل.")

st.divider()

num_committees = st.number_input("كم عدد اللجان التي تريد إدخالها؟", min_value=1, step=1)
committees_data = []

for i in range(int(num_committees)):
    st.subheader(f"📋 بيانات اللجنة رقم {i+1}")
    name = st.text_input(f"اسم اللجنة {i+1}", key=f"name_{i}")
    count = st.number_input(f"عدد الطلاب في اللجنة {i+1}", min_value=0, step=1, key=f"count_{i}")
    committees_data.append({'name': name, 'students_count': count})

st.divider()

if st.button("🚀 إنشاء الأكواد"):
    if any(c['name'].strip() == "" for c in committees_data):
        st.warning("⚠️ يرجى إدخال اسم لكل لجنة قبل المتابعة.")
    else:
        with st.spinner("جاري إنشاء الأكواد وتحليل النطاقات..."):
            result = generate_continuous_codes_detailed(committees_data)

        st.success("✅ تم إنشاء الأكواد بنجاح!")
        st.write("### 📊 ملخص نطاقات التكويد:")

        total_sheets = 0
        for committee_name, data in result.items():
            total_sheets += data['count']
            st.markdown(f"**اللجنة:** {committee_name}")
            st.markdown(f"- عدد الطلاب: **{data['count']}**")
            st.markdown(f"- نطاقات الأكواد:")
            for r in data['ranges']:
                st.code(r)
            st.divider()

        st.info(f"الإجمالي الكلي لجميع اللجان: **{total_sheets} ورقة**")
        st.caption("💡 النطاقات توضّح بداية ونهاية كل مجموعة من 100 ورقة (A, B, C, ...).")
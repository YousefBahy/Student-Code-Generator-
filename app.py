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
        .stTextInput, .stNumberInput, .stButton>button, .stSelectbox {
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

#
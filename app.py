import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO
from PIL import Image

# إعدادات الصفحة لتكون مناسبة للطباعة
st.set_page_config(page_title="نظام التقارير - الروضة 44", layout="centered")

# --- الترويسة الرسمية ---
col1, col2 = st.columns([1, 2])
with col2:
    st.image("https://upload.wikimedia.org/wikipedia/ar/archive/2/22/20220320140228%21Ministry_of_Education_%28Saudi_Arabia%29_Logo.png", width=100)
with col1:
    st.write("**وزارة التعليم**")
    st.write("**إدارة التعليم بمنطقة الباحة**")
    st.write("**الروضة الرابعة والأربعون بكرا الجفدرة**")

st.markdown("<h2 style='text-align: center;'>تقرير توثيق فعالية</h2>", unsafe_allow_html=True)

# --- مدخلات البيانات ---
with st.expander("تعبئة بيانات التقرير", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        title = st.text_input("عنوان الفعالية")
        executors = st.text_input("المنفذون", value="جميع منسوبات الروضة")
        date = st.text_input("تاريخ التنفيذ")
    with c2:
        field = st.text_input("المجال")
        beneficiaries = st.text_input("المستفيدون والعدد")
        location = st.text_input("مكان التنفيذ", value="مقر الروضة")

    user_notes = st.text_area("اكتبي وصفاً مختصراً لما تم تنفيذه (سيقوم الذكاء الاصطناعي بتجميله):")
    link_to_barcode = st.text_input("رابط الشواهد (لتحويله لباركود)")
    
    # خانة رفع الصور
    uploaded_images = st.file_uploader("ارفعي صور الفعالية (حتى 4 صور)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if st.button("إصدار التقرير النهائي"):
    if title and user_notes:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"أعد صياغة النص التالي بأسلوب رسمي لتقرير مدرسي (وزارة التعليم): {user_notes}. اجعلها فقرة وصفية ثم أهداف."
        
        with st.spinner('جاري تنسيق التقرير...'):
            response = model.generate_content(prompt)
            
            # --- شكل التقرير النهائي (A4 Style) ---
            st.markdown("---")
            st.markdown(f"<h3 style='text-align: center; color: white; background-color: #1e3d59; padding: 10px;'>{title}</h3>", unsafe_allow_html=True)
            
            # جدول البيانات
            st.write(f"**المجال:** {field} | **المستفيدون:** {beneficiaries}")
            st.write(f"**المنفذون:** {executors} | **التاريخ:** {date} | **المكان:** {location}")
            
            st.markdown("#### وصف العمل والأهداف:")
            st.write(response.text)
            
            # عرض الصور المرفوعة (4 صور كحد أقصى)
            if uploaded_images:
                st.markdown("#### الشواهد الصور")
                cols = st.columns(2) # عرض صورتين في كل سطر
                for idx, img_file in enumerate(uploaded_images[:4]):
                    with cols[idx % 2]:
                        img = Image.open(img_file)
                        st.image(img, use_container_width=True)
            
            # الباركود والتوقيع
            col_b1, col_b2 = st.columns([1, 2])
            with col_b1:
                if link_to_barcode:
                    qr = qrcode.make(link_to_barcode)
                    buf = BytesIO()
                    qr.save(buf)
                    st.image(buf, width=100, caption="باركود الشواهد")
            with col_b2:
                st.write("\n\n**مديرة الروضة:**")
                st.write("أميرة سعد الغامدي")
                
            st.info("نصيحة: يمكنك طباعة هذه الصفحة وتحويلها لـ PDF عبر متصفحك (Ctrl + P).")
    else:
        st.error("يرجى تعبئة العنوان ووصف العمل.")

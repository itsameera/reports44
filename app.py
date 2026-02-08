import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# إعدادات الصفحة
st.set_page_config(page_title="نظام التقارير المدرسية", layout="wide")

# --- الجزء الأول: الترويسة الرسمية ---
col1, col2 = st.columns([1, 2])
with col2:
    st.image("https://upload.wikimedia.org/wikipedia/ar/archive/2/22/20220320140228%21Ministry_of_Education_%28Saudi_Arabia%29_Logo.png", width=120)
with col1:
    st.write("وزارة التعليم")
    st.write("إدارة التعليم بمنطقة الباحة")
    st.write("الروضة الرابعة والأربعون بكرا الجفدرة")

st.markdown("---")
st.header("نموذج إعداد تقرير فعالية")

# --- الجزء الثاني: خانات التعبئة ---
with st.expander("بيانات التقرير الأساسية", expanded=True):
    title = st.text_input("عنوان الفعالية/التقرير")
    executors = st.text_input("المنفذون", value="جميع منسوبات الروضة")
    participants = st.text_input("المشاركون", value="أولياء الأمور والأطفال")
    date = st.text_input("تاريخ التنفيذ", value="1447هـ")
    location = st.text_input("مكان التنفيذ", value="مقر الروضة")

link_to_barcode = st.text_input("ضع رابط الشواهد (ليتحول إلى باركود)")

# --- الجزء الثالث: تشغيل الذكاء الاصطناعي ---
if st.button("توليد التقرير النهائي"):
    if title:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # أمر الذكاء الاصطناعي (البرومبت المحسن)
        prompt = f"""
        اكتب محتوى تقرير مدرسي احترافي لفعالية بعنوان ({title}).
        المطلوب صياغة فقرتين:
        1. خطوات التنفيذ/الوصف: (اكتبها بشكل نقاط منظمة واحترافية).
        2. الأهداف: (اكتب 4 أهداف سامية بأسلوب تربوي).
        اجعل الأسلوب رسمياً جداً ومناسباً لوزارة التعليم السعودية.
        """
        
        with st.spinner('جاري صياغة التقرير...'):
            response = model.generate_content(prompt)
            
            # عرض النتيجة بشكل يشبه الصورة التي أرفقتيها
            st.success("تم إعداد التقرير بنجاح!")
            
            # تصميم مخرجات التقرير
            st.markdown(f"### {title}")
            
            c1, c2, c3 = st.columns(3)
            c1.info(f"**المنفذون:**\n{executors}")
            c2.info(f"**التاريخ:**\n{date}")
            c3.info(f"**المكان:**\n{location}")
            
            st.markdown("#### وصف الفعالية والأهداف")
            st.write(response.text)
            
            # توليد الباركود إذا وجد رابط
            if link_to_barcode:
                st.markdown("#### باركود الشواهد")
                qr = qrcode.make(link_to_barcode)
                buf = BytesIO()
                qr.save(buf)
                st.image(buf, caption="امسح الباركود لمشاهدة الشواهد", width=150)
            
            st.markdown("---")
            st.write("**مديرة الروضة:** أميرة سعد الغامدي")
    else:
        st.error("لطفاً أدخل عنوان التقرير")

# --- الجزء الرابع: المتطلبات ---
# تأكدي من إضافة qrcode و pillow لملف requirements.txt

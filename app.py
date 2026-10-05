import google.generativeai as genai
import streamlit as st
import tempfile
import os
import time

st.set_page_config(page_title="Movie to Script AI", page_icon="🎬")
st.title("🎬 Movie to Script AI")
st.write("ဗီဒီယိုတင်ပြီး ဇာတ်လမ်းအကျဉ်းကို အလိုအလျောက် ရေးခိုင်းပါ။")

# ကိုယ်ပိုင် AQ ကီး အစစ်ဖြင့် ချိတ်ဆက်ခြင်း
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

uploaded_file = st.file_uploader("ဇာတ်လမ်း ဗီဒီယို တင်ရန် (MP4, AVI, MOV)", type=['mp4', 'avi', 'mov', 'mkv'])

if st.button("🚀 Generate Narrative Script"):
    if not uploaded_file:
        st.warning("⚠️ ကျေးဇူးပြု၍ ဗီဒီယို အရင်တင်ပါ")
    else:
        try:
            with st.spinner("AI သို့ ဗီဒီယို အပ်လုဒ်လုပ်နေပါသည်... (ခဏစောင့်ပါ)"):
                # ဗီဒီယိုကို ယာယီ သိမ်းဆည်းခြင်း
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                    temp_video.write(uploaded_file.read())
                    video_path = temp_video.name

                # API Key အစစ်ဖြင့် File API ကို သုံး၍ ဗီဒီယို တင်ခြင်း
                video_file = genai.upload_file(path=video_path)
                
                # AI မှ ဗီဒီယို Process လုပ်သည်ကို စောင့်ဆိုင်းခြင်း
                while video_file.state.name == "PROCESSING":
                    time.sleep(3)
                    video_file = genai.get_file(video_file.name)
                    
                if video_file.state.name == "FAILED":
                    st.error("❌ ဗီဒီယို လက်မခံပါ။")
                else:
                    st.success("✅ ဗီဒီယို အပ်လုဒ်လုပ်ပြီးပါပြီ။ ဇာတ်လမ်း စဉ်းစားနေပါပြီ...")
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = "ဒီဗီဒီယိုကို သေချာကြည့်ပြီး ဇာတ်လမ်း အပြည့်အစုံကို မြန်မာလို ပြန်ပြောပြပေးပါ။"
                    response = model.generate_content([video_file, prompt])
                    
                    st.success("✅ အောင်မြင်ပါသည်!")
                    st.write(response.text)
                    
                # ယာယီဖိုင်ကို ရှင်းလင်းခြင်း
                os.remove(video_path)
        except Exception as e:
            st.error(f"Error တက်သွားပါသည် - {e}")

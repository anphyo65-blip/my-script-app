import streamlit as st
import google.generativeai as genai
import os
import time
import tempfile

st.set_page_config(page_title="Movie to Script AI", page_icon="🎬")

st.title("🎬 Movie to Script AI")
st.write("ဗီဒီယိုတင်ပြီး ဇာတ်လမ်းစခရစ်ကို အလိုအလျောက် ရေးခိုင်းပါမည်။")

st.sidebar.header("🔑 API Setup")
api_key = st.sidebar.text_input("Gemini API Key ကို ထည့်ပါ:", type="password")

uploaded_file = st.file_uploader("ဇာတ်လမ်း ဗီဒီယို တင်ရန် (MP4, AVI, MOV)", type=['mp4', 'avi', 'mov', 'mkv'])

if st.button("🚀 Generate Narrative Script"):
    if not api_key:
        st.warning("⚠️ ကျေးဇူးပြု၍ ဘေးဘက်တွင် API Key အရင်ထည့်ပါ။")
    elif not uploaded_file:
        st.warning("⚠️ ကျေးဇူးပြု၍ ဗီဒီယို အရင်တင်ပါ။")
    else:
        try:
            with st.spinner("AI သို့ ချိတ်ဆက်နေပါသည်... (ခဏစောင့်ပါ)"):
                genai.configure(api_key=api_key)
                
                # ဗီဒီယိုဖိုင်ကို ယာယီသိမ်းဆည်းခြင်း
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                    temp_video.write(uploaded_file.read())
                    video_path = temp_video.name

                # AI ဆီသို့ ဗီဒီယို လှမ်းပို့ခြင်း
                st.info("ဗီဒီယိုကို AI ထံသို့ ပို့ဆောင်နေပါသည်... (ဗီဒီယိုအရွယ်အစားပေါ်မူတည်၍ အချိန်အနည်းငယ် ကြာနိုင်ပါသည်)")
                video_file = genai.upload_file(path=video_path)

                # AI မှ ဗီဒီယိုကို ကြည့်ရှုစစ်ဆေးခြင်း
                st.info("AI မှ ဗီဒီယိုကို ကြည့်ရှုစစ်ဆေးနေပါသည်...")
                while video_file.state.name == "PROCESSING":
                    time.sleep(3)
                    video_file = genai.get_file(video_file.name)

                if video_file.state.name == "FAILED":
                    st.error("ဗီဒီယို စစ်ဆေးခြင်း မအောင်မြင်ပါ။")
                else:
                    st.info("စခရစ် စတင် ရေးသားနေပါပြီ...")
                    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
                    
                    # AI ကို ခိုင်းစေမည့် စာသား
                    prompt = "ဒီဗီဒီယိုကို သေချာကြည့်ပြီး ဇာတ်လမ်းပြန်ပြောပြတဲ့ (Recap) စခရစ်တစ်ခုကို မြန်မာလို အသေးစိတ် ရေးပေးပါ။"
                    
                    response = model.generate_content([video_file, prompt])
                    
                    st.success("အောင်မြင်စွာ ရေးသားပြီးပါပြီ!")
                    st.write("---")
                    st.write(response.text)
                    
                # ယာယီဖိုင်ကို ပြန်ဖျက်ခြင်း
                os.remove(video_path)
        except Exception as e:
            st.error(f"Error တက်သွားပါသည် - {e}")

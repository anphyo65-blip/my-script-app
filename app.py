import json
from google.oauth2 import service_account
import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Movie to Script AI", page_icon="🎬")

st.title("🎬 Movie to Script AI")
st.write("ဗီဒီယိုတင်ပြီး ဇာတ်လမ်းအကျဉ်းကို အလိုအလျောက် ရေးခိုင်းပါ။")

st.sidebar.header("🔑 API Setup")
st.sidebar.success("✅ စနစ်မှ API ချိတ်ဆက်ထားပြီးပါပြီ။")

uploaded_file = st.file_uploader("ဇာတ်လမ်း ဗီဒီယို တင်ရန် (MP4, AVI, MOV)", type=['mp4', 'avi', 'mov', 'mkv'])

if st.button("🚀 Generate Narrative Script"):
    if not uploaded_file:
        st.warning("⚠️ ကျေးဇူးပြု၍ ဗီဒီယို အရင်တင်ပါ")
    else:
        try:
            with st.spinner("AI သို့ ချိတ်ဆက်နေပါသည်... (ခဏစောင့်ပါ)"):
                
                # ၁။ Service Account ဖြင့် ချိတ်ဆက်ခြင်း
                creds_dict = json.loads(st.secrets["gcp_json"])
                credentials = service_account.Credentials.from_service_account_info(creds_dict)
                genai.configure(credentials=credentials)
                
                # ၂။ ဗီဒီယိုကို ဖတ်ယူခြင်း
                video_bytes = uploaded_file.read()
                
                # ၃။ 404 Error မတက်အောင် Google ထံမှ Model နာမည်အမှန်ကို အလိုအလျောက် ဆွဲယူခြင်း
                target_model = "gemini-1.5-flash" # ပုံမှန် Default
                for m in genai.list_models():
                    if "generateContent" in m.supported_generation_methods and "gemini-1.5" in m.name:
                        target_model = m.name
                        break
                
                model = genai.GenerativeModel(target_model)
                
                # ၄။ AI ထံသို့ တိုက်ရိုက်ပို့ဆောင်ခြင်း
                prompt = "ဒီဗီဒီယိုကို သေချာကြည့်ပြီး ဇာတ်လမ်း အပြည့်အစုံကို မြန်မာလို ပြန်ပြောပြပေးပါ။" 
                
                response = model.generate_content([
                    {"mime_type": uploaded_file.type, "data": video_bytes},
                    prompt
                ])
                
                st.success("✅ အောင်မြင်ပါသည်!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error တက်သွားပါသည် - {e}")

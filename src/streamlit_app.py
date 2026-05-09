# src/streamlit_app.py

import streamlit as st

from rag import ask_question, translate_image


# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="Mini Manuscript RAG",
    page_icon="📜",
    layout="centered"
)

# ======================================
# CUSTOM CSS FOR INTERACTIVE BACKGROUND
# ======================================
st.markdown(
    """
    <style>
    /* Dark Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #141e30);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Dark Glassmorphism Effect for Main Container */
    .block-container {
        background: rgba(15, 23, 42, 0.65);
        border-radius: 20px;
        padding: 3rem !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhance Input Fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📜 Mini Manuscript Conversational RAG ✨")

tab1, tab2 = st.tabs(["💬 Chat with Manuscript", "🖼️ Translate Image"])

with tab1:
    # ======================================
    # USER INPUT
    # ======================================

    query = st.text_input(
        "Ask a question about the manuscript 🕵️‍♂️"
    )

    # ======================================
    # SUBMIT BUTTON
    # ======================================

    if st.button("🚀 Submit Question"):

        if query.strip() == "":

            st.warning("⚠️ Please enter a question.")

        else:

            answer, sources, tokens = ask_question(query)

            st.subheader("💡 Answer")

            st.write(answer)

            st.subheader("📚 Sources")

            unique_sources = sorted(set(sources))

            for source in unique_sources:
                st.write(f"- 📄 {source}")
                
            st.info(f"🪙 Tokens Used: {tokens}")


with tab2:
    st.subheader("🖼️ Upload Manuscript Image for Translation")
    
    uploaded_file = st.file_uploader("Choose an image... 📂", type=["jpg", "jpeg", "png"])
    
    target_language = st.selectbox(
        "🌍 Select Language for Translation",
        ("English", "Hindi")
    )
    
    if st.button("✨ Translate Image"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption='📸 Uploaded Manuscript Image.', use_container_width=True)
            
            with st.spinner('🔮 Analyzing and translating...'):
                image_bytes = uploaded_file.getvalue()
                
                answer, tokens = translate_image(image_bytes, target_language)
                
                st.balloons()  # Interactive sticker/balloon effect on success!
                
                st.subheader("📝 Translation Result")
                st.write(answer)
                
                st.info(f"🪙 Tokens Used: {tokens}")
        else:
            st.warning("⚠️ Please upload an image first.")
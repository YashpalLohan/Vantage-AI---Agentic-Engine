import streamlit as st
import requests

st.set_page_config(
    page_title="GitHub Code Mentor", 
    page_icon="🐙",
    layout="centered"
)

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .reportview-container {
        background: #f8f9fa;
    }
    .review-card {
        padding: 2rem;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 2rem;
    }
    .language-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        background-color: #e7f3ff;
        color: #007bff;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 4px;
    }
    h1 {
        color: #1a1a1a;
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🐙 GitHub Code Mentor")
st.markdown("##### Transform your repository into a professional portfolio with AI-powered feedback.")

with st.container():
    st.markdown('<div class="review-card">', unsafe_allow_html=True)
    username = st.text_input("GitHub Username", placeholder="e.g., torvalds")
    analyze_btn = st.button("Analyze Portfolio")
    st.markdown('</div>', unsafe_allow_html=True)

if analyze_btn:
    if username:
        with st.spinner(f"🚀 AI Mentor is reviewing {username}..."):
            try:
                # Local endpoint for now
                response = requests.post(f"http://127.0.0.1:8000/review?username={username}")
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete!")
                    
                    # Portfolio Data Section
                    col_avatar, col1, col2 = st.columns([1, 1, 2])
                    
                    with col_avatar:
                        avatar_url = data["extracted_data"].get("avatar_url")
                        if avatar_url:
                            st.image(avatar_url, width=100, use_column_width=False)
                        else:
                            st.markdown("👤")

                    with col1:
                        st.subheader("📊 Stats")
                        st.metric("Public Repos", data["extracted_data"].get("public_repos_count", 0))
                        
                    with col2:
                        st.subheader("💻 Languages")
                        langs = data["extracted_data"].get("primary_languages", [])
                        if langs:
                            for lang in langs:
                                st.markdown(f'<span class="language-pill">{lang}</span>', unsafe_allow_html=True)
                        else:
                            st.write("No specific languages detected.")

                    st.markdown("---")
                    
                    # Feedback Section
                    st.subheader("💡 Mentor Feedback")
                    st.markdown(f'<div class="review-card">{data["mentor_feedback"]}</div>', unsafe_allow_html=True)
                    
                    st.subheader("📁 Recent Projects")
                    repos = data["extracted_data"].get("recent_repos", [])
                    st.write(", ".join(repos) if repos else "No recent repositories found.")

                else:
                    st.error(f"Backend Error: {response.status_code}")
            except Exception as e:
                st.error(f"Could not connect to the backend: {str(e)}")
    else:
        st.warning("Please enter a username first.")

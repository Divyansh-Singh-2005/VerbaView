import streamlit as st
import requests
import json
import re

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="VerbaView Studio", page_icon="🎨")

# CONSTANTS
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2" 

# --- BACKEND FUNCTIONS ---
def talk_to_verbaview(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1
    }
    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None

def get_html_prompt(user_instruction, current_code=None):
    role = """
    You are VerbaView, an expert Frontend AI.
    RULES:
    1. Return ONLY valid HTML code.
    2. MAIN STYLING: Use Tailwind CSS via CDN: <script src="https://cdn.tailwindcss.com"></script>
    3. CUSTOM CSS: If specific animations or complex styles are needed, put them in a <style> block in the <head>.
    4. ICONS: Use FontAwesome: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />
    5. SINGLE FILE: Put all CSS/JS inside the HTML.
    """
    if current_code:
        return f"{role}\nEXISTING CODE:\n{current_code}\nUSER UPDATE: {user_instruction}\nTASK: Update code. Return ONLY HTML."
    else:
        return f"{role}\nUSER REQUEST: {user_instruction}\nGENERATE HTML:"

def get_react_conversion_prompt(html_code):
    return f"""
    You are a Code Transpiler. Convert the following HTML into a Modern React Functional Component.
    INPUT HTML:
    {html_code}
    RULES:
    1. Return ONLY the Javascript/JSX code.
    2. Change 'class' to 'className'.
    3. Convert <style> blocks into a 'const styles' object or styled-components.
    4. Close all self-closing tags.
    5. Use 'export default function VerbaComponent()' structure.
    REACT CODE:
    """

def extract_css(html_code):
    match = re.search(r'<style>(.*?)</style>', html_code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "/* No custom CSS found. Using Tailwind utility classes. */"

def sanitize_code(raw_text):
    if not raw_text: return ""
    return raw_text.replace("```html", "").replace("```jsx", "").replace("```css", "").replace("```", "").strip()

def ensure_tailwind(html_code):
    if "cdn.tailwindcss.com" not in html_code:
        head_end = html_code.find("</head>")
        if head_end != -1:
            return html_code[:head_end] + '<script src="https://cdn.tailwindcss.com"></script>' + html_code[head_end:]
    return html_code

# --- FRONTEND UI ---

# Initialize Session State
if "html_code" not in st.session_state:
    st.session_state.html_code = ""
if "react_code" not in st.session_state:
    st.session_state.react_code = ""

# --- SIDEBAR (The Control Center) ---
with st.sidebar:
    st.title("🎨 VerbaView")
    st.markdown("---")
    
    # 1. Navigation (The "Tabs" are now here on the left)
    st.subheader("📍 View Mode")
    view_mode = st.radio(
        "Select Output:",
        options=["👁️ Live Preview", "📄 HTML Source", "🎨 CSS (Custom)", "⚛️ React (JSX)"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # 2. Controls
    if st.button("🗑️ Clear Workspace", use_container_width=True):
        st.session_state.html_code = ""
        st.session_state.react_code = ""
        st.rerun()
    
    st.markdown("---")
    st.caption(f"Model: {MODEL_NAME}")

# --- MAIN AREA ---
st.subheader("Describe your Interface")

col_input, col_btn = st.columns([4, 1])
with col_input:
    prompt = st.text_input("Instruction:", placeholder="e.g. A login card with a floating animation using custom CSS")
with col_btn:
    st.write("") 
    st.write("")
    generate_btn = st.button("✨ Generate", type="primary", use_container_width=True)

# Generator Logic
if generate_btn and prompt:
    with st.spinner("🧠 Engineering Interface..."):
        full_prompt = get_html_prompt(prompt, st.session_state.html_code)
        raw_response = talk_to_verbaview(full_prompt)
        if raw_response:
            clean_html = sanitize_code(raw_response)
            final_html = ensure_tailwind(clean_html)
            st.session_state.html_code = final_html
            st.session_state.react_code = "" 
            st.success("Design Generated!")

# Display Logic (Based on Sidebar Selection)
if st.session_state.html_code:
    st.markdown("---")
    
    if view_mode == "👁️ Live Preview":
        st.header("Live Preview")
        # Full width, no tabs cutting it off
        st.components.v1.html(st.session_state.html_code, height=800, scrolling=True)

    elif view_mode == "📄 HTML Source":
        st.header("Source Code (HTML)")
        st.code(st.session_state.html_code, language="html")
        st.download_button("📥 Download HTML", st.session_state.html_code, "verbaview.html", "text/html")

    elif view_mode == "🎨 CSS (Custom)":
        st.header("Custom CSS Styles")
        css_content = extract_css(st.session_state.html_code)
        st.code(css_content, language="css")
        st.info("ℹ️ This shows styles from the <style> block. Tailwind classes are inline.")

    elif view_mode == "⚛️ React (JSX)":
        st.header("React Component")
        
        if st.session_state.react_code == "":
            st.info("Convert the current design into a React Component.")
            if st.button("⚡ Convert to React Code"):
                with st.spinner("Transpiling to JSX..."):
                    react_prompt = get_react_conversion_prompt(st.session_state.html_code)
                    raw_react = talk_to_verbaview(react_prompt)
                    st.session_state.react_code = sanitize_code(raw_react)
                    st.rerun()
        
        if st.session_state.react_code:
            st.code(st.session_state.react_code, language="javascript")
            st.download_button("📥 Download JSX", st.session_state.react_code, "VerbaComponent.jsx", "text/javascript")

else:
    # Empty State Hint
    st.info("👈 Enter a prompt above and click Generate to start.")
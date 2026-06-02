"""
AI YouTube Toolkit - Streamlit Web UI
Run with: streamlit run app.py
"""

import json
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI YouTube Toolkit",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .stTextArea textarea { font-size: 0.9rem; }
    .tag-pill {
        display: inline-block;
        background: #e9ecef;
        border-radius: 20px;
        padding: 3px 12px;
        margin: 3px 2px;
        font-size: 0.82rem;
        color: #495057;
    }
    .char-count { font-size: 0.78rem; color: #6c757d; text-align: right; }
    .section-label {
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)


def demo_metadata(topic, style):
    hooks = {
        "educational": "In this video, I break down",
        "tutorial": "Step by step, I show you how to build",
        "vlog": "Follow along as I work through",
    }
    hook = hooks.get(style, "In this video, I cover")
    return {
        "title": f"How I Built {topic[:42].strip()} (Step-by-Step)",
        "description": (
            f"{hook} {topic} from zero to a working project.\n\n"
            "Timestamps:\n0:00 - Intro\n1:30 - What We're Building\n"
            "5:00 - Setup\n12:00 - Core Logic\n25:00 - Demo\n\n"
            "Subscribe for more AI and automation content!"
        ),
        "tags": [
            topic.lower()[:25], "python", "ai", "automation",
            "tutorial", "openai", "developer tools", "youtube creator",
            "tech", "build with ai", "beginner friendly",
        ],
        "_demo": True,
    }


def generate_metadata(topic, style):
    api_key = os.getenv("OPENAI_API_KEY") or st.session_state.get("api_key", "")
    if not api_key or not api_key.startswith("sk-"):
        return demo_metadata(topic, style)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""You are a YouTube SEO expert for tech/AI creators.
Generate metadata for: {topic} (style: {style})
Return JSON: {{"title": "<70 chars", "description": "3 paragraphs + timestamps + CTA", "tags": ["up to 15 tags"]}}"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        result["_demo"] = False
        return result
    except Exception as e:
        result = demo_metadata(topic, style)
        result["_error"] = str(e)
        return result


if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("## 🎬 AI YouTube Toolkit")
st.markdown("Generate SEO-optimized **titles, descriptions & tags** in seconds.")
st.divider()

with st.sidebar:
    st.markdown("### Settings")
    api_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Leave blank for demo mode.",
        value=st.session_state.get("api_key", ""),
    )
    if api_input:
        st.session_state["api_key"] = api_input
    st.markdown("---")
    st.markdown("No key? Demo mode shows the same output format using templates.")
    st.markdown("---")
    st.markdown("Built by [osiris379](https://github.com/osiris379)")

with st.form("generator_form"):
    topic = st.text_input(
        "Video Topic",
        placeholder="e.g. How to build an AI chatbot with Python",
        max_chars=200,
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        style = st.selectbox(
            "Content Style",
            options=["educational", "tutorial", "vlog"],
            format_func=lambda x: {
                "educational": "Educational",
                "tutorial": "Tutorial",
                "vlog": "Vlog",
            }[x],
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Generate", use_container_width=True, type="primary")

if submitted:
    if not topic.strip():
        st.warning("Please enter a video topic first!")
    else:
        with st.spinner("Generating your YouTube metadata..."):
            result = generate_metadata(topic.strip(), style)
            st.session_state.result = result
            st.session_state.history.insert(0, {"topic": topic.strip(), "style": style, "result": result})
            if len(st.session_state.history) > 5:
                st.session_state.history = st.session_state.history[:5]

if st.session_state.result:
    r = st.session_state.result
    if r.get("_demo"):
        st.info("Demo mode active. Add an OpenAI API key in the sidebar for AI-generated output.")
    if r.get("_error"):
        st.warning(f"API error: {r['_error']} - showing demo output.")
    st.markdown("---")
    st.markdown("### Your Metadata")
    title_val = r.get("title", "")
    st.markdown('<p class="section-label">Title</p>', unsafe_allow_html=True)
    st.code(title_val, language=None)
    char_color = "green" if len(title_val) <= 70 else "red"
    st.markdown(f'<p class="char-count"><span style="color:{char_color}">{len(title_val)} / 70 chars</span></p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    desc_val = r.get("description", "")
    st.markdown('<p class="section-label">Description</p>', unsafe_allow_html=True)
    st.text_area("", value=desc_val, height=220, label_visibility="collapsed", key="desc_output")
    st.markdown("<br>", unsafe_allow_html=True)
    tags = r.get("tags", [])
    tags_str = ", ".join(tags)
    st.markdown('<p class="section-label">Tags</p>', unsafe_allow_html=True)
    pills = " ".join(f'<span class="tag-pill">{t}</span>' for t in tags)
    st.markdown(f'<div style="margin-bottom:0.5rem">{pills}</div>', unsafe_allow_html=True)
    st.caption(f"{len(tags)} tags - copy-paste ready:")
    st.code(tags_str, language=None)
    st.markdown("<br>", unsafe_allow_html=True)
    export_text = f"TITLE\n{title_val}\n\nDESCRIPTION\n{desc_val}\n\nTAGS\n{tags_str}\n"
    st.download_button(
        label="Download as .txt",
        data=export_text,
        file_name=f"yt_metadata_{topic[:30].replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

if len(st.session_state.history) > 1:
    st.markdown("---")
    with st.expander(f"Recent generations ({len(st.session_state.history)})"):
        for i, item in enumerate(st.session_state.history[1:], 1):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{item['topic'][:60]}**")
                st.caption(f"{item['style']} - {item['result'].get('title', '')[:50]}")
            with col_b:
                if st.button("Load", key=f"load_{i}", use_container_width=True):
                    st.session_state.result = item["result"]
                    st.rerun()

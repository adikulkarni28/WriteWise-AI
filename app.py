
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI

load_dotenv()

st.set_page_config(
    page_title="WriteWise AI",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #6488ed;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    text-align: center;
    color: #9098a8;
    margin-bottom: 30px;
}

div.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    min-height: 45px;
}

div.stDownloadButton > button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

if "last_error" not in st.session_state:
    st.session_state.last_error = ""

if "generation_status" not in st.session_state:
    st.session_state.generation_status = ""

st.markdown(
    '<div class="main-title">WriteWise AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Intelligent AI-Powered Writing Assistant</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("Settings")

    provider = st.selectbox(
        "Choose AI Provider",
        ["Google Gemini", "OpenAI"]
    )

    if provider == "Google Gemini":
        model = st.selectbox(
            "Choose Gemini Model",
            [
                "gemini-3.6-flash",
                "gemini-3.5-flash",
                "gemini-3.1-flash-lite",
                "gemini-2.5-flash-lite"
            ]
        )
    else:
        model = st.selectbox(
            "Choose OpenAI Model",
            [
                "gpt-4.1-mini",
                "gpt-4.1"
            ]
        )

    st.divider()

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    output_format = st.selectbox(
        "Output Format",
        ["Markdown", "Plain Text"]
    )

    st.divider()
    st.caption("WriteWise AI")
    st.caption("AI-powered writing assistant")

st.subheader("Create Your Content")

col1, col2 = st.columns(2)

with col1:
    task_type = st.selectbox(
        "What do you want to create?",
        [
            "Blog Writing",
            "Email Drafting",
            "Code Explanation",
            "Social Media Post",
            "Essay Writing",
            "Resume Content",
            "Project Documentation",
            "Summary",
            "Custom Writing"
        ]
    )

with col2:
    tone = st.selectbox(
        "Writing Tone",
        [
            "Professional",
            "Simple",
            "Friendly",
            "Formal",
            "Creative",
            "Academic",
            "Persuasive",
            "Conversational"
        ]
    )

col3, col4 = st.columns(2)

with col3:
    length = st.selectbox(
        "Content Length",
        ["Short", "Medium", "Long"]
    )

with col4:
    audience = st.selectbox(
        "Target Audience",
        [
            "General Audience",
            "Students",
            "Professionals",
            "Developers",
            "Business Owners",
            "Teachers"
        ]
    )

user_prompt = st.text_area(
    "Enter your topic or instructions",
    placeholder="Example: Write a detailed blog about Siberian Huskies, their temperament and care.",
    height=150
)

extra_instructions = st.text_area(
    "Additional Instructions (Optional)",
    placeholder="Example: Include real-world examples and use simple English.",
    height=90
)

word_targets = {
    "Short": "150 to 250 words",
    "Medium": "400 to 600 words",
    "Long": "800 to 1200 words"
}

token_limits = {
    "Short": 1500,
    "Medium": 3000,
    "Long": 6000
}


def create_prompt():
    if output_format == "Markdown":
        format_instruction = (
            "Use Markdown headings, paragraphs and lists where appropriate."
        )
    else:
        format_instruction = (
            "Write in plain text without Markdown symbols."
        )

    return f"""
You are WriteWise AI, a helpful and skilled writing assistant.

Task: {task_type}

User request:
{user_prompt}

Tone: {tone}
Target audience: {audience}
Length: {length}
Suggested word count: {word_targets[length]}

Additional instructions:
{extra_instructions.strip() if extra_instructions.strip() else "None"}

Writing guidelines:
Write natural, clear and useful content.
Follow the user's instructions carefully.
Use the selected tone and target audience.
Avoid unnecessary repetition.
Use examples when they improve understanding.
Do not invent statistics, sources or factual claims.
Finish the content with a proper ending.
Do not stop in the middle of a sentence.
For code explanations, prioritize correctness over word count.

Formatting:
{format_instruction}

Return only the requested content.
"""


def extract_gemini_text(response):
    try:
        if response.text:
            return response.text.strip()
    except (ValueError, AttributeError):
        pass

    parts = []

    for candidate in response.candidates or []:
        content = candidate.content

        if content and content.parts:
            for part in content.parts:
                if getattr(part, "text", None):
                    if not getattr(part, "thought", False):
                        parts.append(part.text)

    return "\n".join(parts).strip()


def generate_with_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from the .env file."
        )

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=120000)
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=token_limits[length]
        )
    )

    if not response:
        raise RuntimeError("Gemini returned no response.")

    generated_text = extract_gemini_text(response)

    if not generated_text:
        raise RuntimeError(
            "Gemini returned an empty response. "
            "Try another model or retry later."
        )

    finish_reason = None

    if response.candidates:
        finish_reason = response.candidates[0].finish_reason

    reason_name = str(finish_reason).split(".")[-1]

    if reason_name == "MAX_TOKENS":
        return generated_text, (
            "Gemini reached its output token limit. "
            "The generated content may be incomplete."
        )

    if reason_name not in ("STOP", "None", "FINISH_REASON_UNSPECIFIED"):
        return generated_text, (
            f"Gemini stopped generation with status: {reason_name}. "
            "Please review the output."
        )

    return generated_text, ""


def generate_with_openai(prompt):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing from the .env file."
        )

    client = OpenAI(
        api_key=api_key,
        timeout=120.0
    )

    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=temperature,
        max_output_tokens=token_limits[length]
    )

    generated_text = response.output_text

    if not generated_text or not generated_text.strip():
        raise RuntimeError(
            "OpenAI returned an empty response."
        )

    warning = ""

    if response.status == "incomplete":
        warning = (
            "OpenAI stopped before completing the content. "
            "The output may be incomplete."
        )

    return generated_text.strip(), warning


st.divider()

if st.button(
    "✨ Generate Content",
    type="primary",
    use_container_width=True
):
    if not user_prompt.strip():
        st.warning("Please enter a topic or instructions.")

    else:
        st.session_state.generated_text = ""
        st.session_state.last_error = ""
        st.session_state.generation_status = ""

        with st.spinner("Generating your content..."):
            try:
                prompt = create_prompt()

                if provider == "Google Gemini":
                    result, warning = generate_with_gemini(prompt)
                else:
                    result, warning = generate_with_openai(prompt)

                st.session_state.generated_text = result
                st.session_state.generation_status = warning

            except Exception as error:
                st.session_state.last_error = str(error)

if st.session_state.last_error:
    st.error("Unable to generate content.")
    st.code(st.session_state.last_error)

    st.info(
        "Check your API key, model access and quota. "
        "If the AI provider is temporarily unavailable, "
        "try again later."
    )

if st.session_state.generated_text:
    st.subheader("Generated Content")

    if st.session_state.generation_status:
        st.warning(st.session_state.generation_status)
    else:
        st.success("Content generated successfully!")

    if output_format == "Markdown":
        st.markdown(st.session_state.generated_text)
    else:
        st.text(st.session_state.generated_text)

    st.divider()

    download_col, clear_col = st.columns(2)

    with download_col:
        file_extension = (
            "md" if output_format == "Markdown" else "txt"
        )

        mime_type = (
            "text/markdown"
            if output_format == "Markdown"
            else "text/plain"
        )

        st.download_button(
            label="Download Content",
            data=st.session_state.generated_text,
            file_name=f"writewise_content.{file_extension}",
            mime=mime_type,
            use_container_width=True
        )

    with clear_col:
        if st.button(
            "Clear Result",
            use_container_width=True
        ):
            st.session_state.generated_text = ""
            st.session_state.last_error = ""
            st.session_state.generation_status = ""
            st.rerun()

st.divider()

st.markdown(
    "<center>Made with ❤️ using Python, Streamlit and Generative AI</center>",
    unsafe_allow_html=True
)

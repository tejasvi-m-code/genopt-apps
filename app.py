import streamlit as st
import requests

FAB_API_ENDPOINT = "https://xmy6yovg6aaq4db7brijnsww6q0phnvv.lambda-url.us-east-1.on.aws/agent/test-01/execute"
FAB_HEADERS = {
    'content-type': 'application/json',
    'x-user-id': 'tejasvi-poc',
    'x-authentication': 'api-key D8762AA1BA98FB28EEE6EA45:2a33da34fa1e9a863aed86153e77a2a7'
}

LANGUAGES = [
    "Python", "JavaScript", "ESQL", "SAP ABAB", "Salesforce Apex",
    "Java", "C#", "Go", "Ruby", "TypeScript"
]

MODELS = [
    "FAB-GPT-Pro",
    "FAB-Codex",
    "FAB-Azure",
    "FAB-GoogleAI"
]

st.set_page_config(page_title="FAB Code Assistant", layout="wide")
st.title("FAB Code Generation & Optimization Assistant")

st.sidebar.header("Settings")
model_choice = st.sidebar.radio("Choose AI Model:", MODELS)
language_choice = st.sidebar.selectbox("Select Programming Language:", LANGUAGES)

uploaded_code = None
uploaded_file = st.file_uploader("Upload code file", type=["py", "js", "txt", "java", "cs"])
if uploaded_file:
    uploaded_code = uploaded_file.read().decode("utf-8")

st.subheader("Code Generation via Prompt")
user_prompt = st.text_area("Enter your prompt:", height=150)

if st.button("Generate Code"):
    if user_prompt:
        with st.spinner("Generating code from FAB Agent..."):
            try:
                response = requests.post(
                    FAB_API_ENDPOINT,
                    headers=FAB_HEADERS,
                    json={"input": {"query": user_prompt}}
                )
                response.raise_for_status()
                code_output = response.json().get("output", "No code returned.")
                st.code(code_output, language=language_choice.lower())

                st.download_button(
                    label="Download Generated Code",
                    data=code_output,
                    file_name=f"generated_code.{language_choice.lower()}",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt to generate code.")

st.subheader("Optimize Uploaded Code")
if st.button("Optimize Code"):
    if uploaded_code:
        optimize_prompt = (
            f"Optimize this {language_choice} code for the fastest possible execution while maintaining identical output. "
            f"Focus on performance improvements, algorithmic optimizations, and language-specific best practices. "
            f"Respond only with code; do not explain your work.\n\n{uploaded_code}"
        )
        with st.spinner("Optimizing code via FAB Agent..."):
            try:
                response = requests.post(
                    FAB_API_ENDPOINT,
                    headers=FAB_HEADERS,
                    json={"input": {"query": optimize_prompt}}
                )
                response.raise_for_status()
                optimized_code = response.json().get("output", "No optimized code returned.")
                st.code(optimized_code, language=language_choice.lower())

                st.download_button(
                    label="Download Optimized Code",
                    data=optimized_code,
                    file_name=f"optimized_code.{language_choice.lower()}",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload a code file to optimize.")

st.subheader("Code Conversion (from existing upload)")
conversion_target = st.selectbox("Convert code to: (Target Language)", LANGUAGES)

if st.button("Convert Code"):
    if uploaded_code:
        conversion_prompt = (
            f"Convert the following {language_choice} code into {conversion_target}. "
            f"Only respond with equivalent, runnable code. Do not explain your work.\n\n{uploaded_code}"
        )
        with st.spinner("Converting code via FAB Agent..."):
            try:
                response = requests.post(
                    FAB_API_ENDPOINT,
                    headers=FAB_HEADERS,
                    json={"input": {"query": conversion_prompt}}
                )
                response.raise_for_status()
                converted_code = response.json().get("output", "No converted code returned.")
                st.code(converted_code, language=conversion_target.lower())

                st.download_button(
                    label="Download Converted Code",
                    data=converted_code,
                    file_name=f"converted_code.{conversion_target.lower()}",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload a code file to convert.")

st.subheader("Code Conversion via File Upload")
convert_uploaded_file = st.file_uploader("Upload a file to convert code", key="convert_file", type=["py", "js", "txt", "java", "cs"])

source_lang = st.selectbox("Original Language", LANGUAGES, key="source_lang")
target_lang = st.selectbox("Target Language", LANGUAGES, key="target_lang")

if st.button("Run Code Conversion"):
    if convert_uploaded_file:
        try:
            file_content = convert_uploaded_file.read().decode("utf-8")
            conversion_prompt = (
                f"Convert the following {source_lang} code into {target_lang}. "
                f"Only respond with equivalent, runnable code. Do not explain your work.\n\n{file_content}"
            )

            with st.spinner("Converting uploaded code via FAB Agent..."):
                response = requests.post(
                    FAB_API_ENDPOINT,
                    headers=FAB_HEADERS,
                    json={"input": {"query": conversion_prompt}}
                )
                response.raise_for_status()
                converted_code = response.json().get("output", "No converted code returned.")
                st.code(converted_code, language=target_lang.lower())

                st.download_button(
                    label="Download Converted Code",
                    data=converted_code,
                    file_name=f"converted_code.{target_lang.lower()}",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload a code file to convert.")

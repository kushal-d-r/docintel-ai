import streamlit as st
import requests

st.set_page_config(page_title="DocIntel AI")

st.title("📄 DocIntel AI")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["jpg", "jpeg", "png", "pdf"]
)

if uploaded_file is not None:

    st.success("File selected")

    if uploaded_file.type.startswith("image"):
        st.image(uploaded_file)

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            uploaded_file.type
        )
    }

    if st.button("Upload"):

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        st.json(response.json())
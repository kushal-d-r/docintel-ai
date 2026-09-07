import streamlit as st
import requests

st.set_page_config(
    page_title="DocIntel AI",
    page_icon="📄",
    layout="wide"
)

# ==========================================================
# Session State
# ==========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "question" not in st.session_state:
    st.session_state.question = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""


# ==========================================================
# API Functions
# ==========================================================

def upload_document(uploaded_file):

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            uploaded_file.type
        )
    }

    response = requests.post(
        "http://127.0.0.1:8000/upload",
        files=files
    )

    if response.status_code == 200:
        st.session_state.result = response.json()
        st.session_state.answer = ""
    else:
        st.error("Upload Failed")
        st.text(response.text)


def ask_question(question, fields):

    payload = {
        "question": question,
        "fields": fields
    }

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json=payload
    )

    if response.status_code == 200:
        return response.json()["answer"]

    return "Unable to answer."



def search_documents(query):

    response = requests.get(
        "http://127.0.0.1:8000/search",
        params={"query": query}
    )

    if response.status_code == 200:
        return response.json()["results"]

    return []


# ==========================================================
# Header
# ==========================================================

st.title("📄 DocIntel AI")
st.caption("AI Powered Document Intelligence System")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["jpg", "jpeg", "png", "pdf"]
)

# ==========================================================
# Upload Section
# ==========================================================

if uploaded_file is not None:

    st.success("✅ File Selected")

    if uploaded_file.type.startswith("image"):
        st.image(
            uploaded_file,
            caption="Uploaded Document",
            use_container_width=True
        )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("📤 Upload Document", use_container_width=True):
            upload_document(uploaded_file)

    with col2:
        if st.button("🗑 Clear Result", use_container_width=True):
            st.session_state.result = None
            st.session_state.answer = ""
            st.rerun()
            
            
            
# ==========================================================
# Semantic Search
# ==========================================================

st.divider()

st.header("🔍 Semantic Document Search")

search_query = st.text_input(
    "Search Documents",
    placeholder="Example: Roshan, PAN, Passport, Karnataka"
)

if st.button("🔎 Search Documents", use_container_width=True):

    if search_query.strip() == "":

        st.warning("Enter a search query.")

    else:

        results = search_documents(search_query)

        if len(results) == 0:

            st.warning("No matching documents found.")

        else:

            st.success(f"{len(results)} document(s) found")

            for i, result in enumerate(results):

                with st.expander(
                    f"📄 Result {i+1} | Score: {result['score']:.4f}"
                ):

                    st.write("**Filename**")
                    st.info(result["filename"])

                    st.write("**Similarity Score**")
                    st.info(round(result["score"], 4))

                    st.write("**Extracted Fields**")
                    st.json(result["fields"])            
            



# ==========================================================
# Results
# ==========================================================

if st.session_state.result is not None:

    result = st.session_state.result
    fields = result["fields"]
    
    st.subheader("📷 Highlighted OCR")

    st.image(
        result["highlighted_image"],
        use_container_width=True
    )

    st.success("✅ OCR Completed Successfully")

    # ------------------------------------------------------
    # OCR Text
    # ------------------------------------------------------

    st.subheader("📄 OCR Text")

    st.text_area(
        "",
        result["ocr_text"],
        height=180
    )

    # ------------------------------------------------------
    # Structured JSON
    # ------------------------------------------------------

    st.subheader("📋 Structured JSON")

    st.json(fields)

    # ------------------------------------------------------
    # Extracted Information
    # ------------------------------------------------------

    st.subheader("📌 Extracted Information")

    for key, value in fields.items():
        st.write(f"**{key}**: {value}")

    # ------------------------------------------------------
    # OCR Words
    # ------------------------------------------------------

    if "words" in result:

        st.subheader("🔤 OCR Words")

        st.write(result["words"])

    # ------------------------------------------------------
    # Bounding Boxes
    # ------------------------------------------------------

    if "boxes" in result:

        st.subheader("📦 Bounding Boxes")

        st.write(result["boxes"])

    # ------------------------------------------------------
    # Question Answering
    # ------------------------------------------------------

    st.divider()

    st.subheader("💬 Ask Questions")

    st.session_state.question = st.text_input(
        "Enter your question",
        value=st.session_state.question,
        placeholder="Example: What is DOB?"
    )

    st.markdown("### Quick Questions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("👤 Name"):
            st.session_state.question = "What is Name?"
            st.rerun()

    with col2:
        if st.button("🎂 DOB"):
            st.session_state.question = "What is DOB?"
            st.rerun()

    with col3:
        if st.button("🚻 Gender"):
            st.session_state.question = "What is Gender?"
            st.rerun()

    with col4:
        if st.button("🪪 Aadhaar"):
            st.session_state.question = "What is Aadhaar Number?"
            st.rerun()

    if st.button("🤖 Ask AI", use_container_width=True):

        if st.session_state.question.strip() == "":

            st.warning("Please enter a question.")

        else:

            st.session_state.answer = ask_question(
                st.session_state.question,
                fields
            )

    if st.session_state.answer != "":

        st.subheader("✅ Answer")

        st.success(st.session_state.answer)
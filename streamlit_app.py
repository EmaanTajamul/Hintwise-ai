
import streamlit as st
import requests

# ---------------- CONFIG ----------------

API_URL = "https://rude-walls-remain.loca.lt/generate-hint"

st.set_page_config(
    page_title="HintWise AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- STYLING ----------------

st.markdown("""
<style>
.stApp {
    background: #111827;
    color: #F3F4F6;
}

.block-container {
    max-width: 950px;
    padding-top: 3rem;
}

.hero {
    text-align: center;
    padding: 35px 10px;
}

.hero h1 {
    font-size: 46px;
    color: #F9FAFB;
    margin-bottom: 10px;
}

.hero p {
    color: #9CA3AF;
    font-size: 17px;
}

.stTextArea textarea {
    background: #1F2937;
    color: #F9FAFB;
    border: 1px solid #374151;
    border-radius: 12px;
}

.stButton button {
    background: #0D9488;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton button:hover {
    background: #0F766E;
    color: white;
}

.hint-card {
    background: #1F2937;
    border: 1px solid #374151;
    border-left: 4px solid #0D9488;
    padding: 20px;
    border-radius: 12px;
    margin: 12px 0;
}

.hint-title {
    color: #5EEAD4;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 8px;
}

.hint-text {
    color: #F9FAFB;
    font-size: 16px;
    line-height: 1.6;
}

.footer {
    text-align: center;
    color: #6B7280;
    padding: 35px 0 10px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- EXAMPLES ----------------

EXAMPLES = {
    "Addition": "Ali has 5 apples. He buys 3 more apples. How many apples does he have now?",
    "Multiplication": "A box holds 6 pencils. How many pencils are in 7 boxes?",
    "Subtraction": "Sara had 20 stickers and gave 8 to her friend. How many stickers are left?",
    "Division": "24 chocolates are shared equally among 6 children. How many chocolates does each child get?"
}

# ---------------- SESSION STATE ----------------

if "question" not in st.session_state:
    st.session_state.question = ""

if "hints" not in st.session_state:
    st.session_state.hints = []

if "error" not in st.session_state:
    st.session_state.error = ""

# ---------------- API FUNCTION ----------------

def generate_hints(question):

    response = requests.post(
        API_URL,
        json={"question": question},
        timeout=180,
        headers={"bypass-tunnel-reminder": "true"},
    )

    response.raise_for_status()
    data = response.json()

    # Support both possible backend response formats
    hints = data.get("hints")

    if not hints:
        single_hint = data.get("hint")
        if single_hint:
            hints = [single_hint]

    if isinstance(hints, str):
        hints = [hints]

    if not isinstance(hints, list) or not hints:
        raise ValueError("The API did not return a valid hint.")

    return [str(hint) for hint in hints if str(hint).strip()]


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🧠 HintWise AI</h1>
    <p>Think smarter. Solve independently.</p>
    <p>Get guided hints instead of direct answers.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- EXAMPLE QUESTIONS ----------------

st.subheader("Try an example")

columns = st.columns(4)

for index, (name, example) in enumerate(EXAMPLES.items()):
    with columns[index]:
        if st.button(name, use_container_width=True):
            st.session_state.question = example
            st.session_state.hints = []
            st.session_state.error = ""

# ---------------- INPUT ----------------

st.subheader("Enter your math problem")

question = st.text_area(
    "Your question",
    key="question",
    height=130,
    placeholder="Example: Ahmed has 10 candies and gives 4 to his friend. How many are left?",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])

with col1:
    generate_clicked = st.button(
        "Generate Hint",
        use_container_width=True
    )

with col2:
    clear_clicked = st.button(
        "Clear",
        use_container_width=True
    )

if clear_clicked:
    st.session_state.question = ""
    st.session_state.hints = []
    st.session_state.error = ""
    st.rerun()

# ---------------- GENERATE HINTS ----------------

if generate_clicked:

    if not question.strip():
        st.warning("Please enter a math problem first.")

    else:
        st.session_state.hints = []
        st.session_state.error = ""

        with st.spinner("Your AI tutor is thinking..."):

            try:
                st.session_state.hints = generate_hints(question.strip())

            except requests.exceptions.ConnectionError:
                st.session_state.error = (
                    "Could not connect to the AI backend. "
                    "Please make sure your FastAPI server is running."
                )

            except requests.exceptions.Timeout:
                st.session_state.error = (
                    "The model is taking too long. Please try again."
                )

            except requests.exceptions.RequestException as error:
                st.session_state.error = f"API error: {error}"

            except (ValueError, KeyError) as error:
                st.session_state.error = str(error)

            except Exception as error:
                st.session_state.error = f"Something went wrong: {error}"

# ---------------- RESULTS ----------------

if st.session_state.error:
    st.error(st.session_state.error)

if st.session_state.hints:

    st.divider()
    st.subheader("Your Guided Hints")

    titles = [
        "Understand the Problem",
        "Choose a Strategy",
        "Take the First Step"
    ]

    for index, hint in enumerate(st.session_state.hints):

        title = (
            titles[index]
            if index < len(titles)
            else f"Additional Hint {index + 1}"
        )

        st.markdown(
            f"""
            <div class="hint-card">
                <div class="hint-title">
                    STEP {index + 1} · {title}
                </div>
                <div class="hint-text">{hint}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success("Keep thinking and solve the problem yourself!")

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    HintWise AI · Fine-tuned Math Learning Assistant
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import random
import plotly.express as px

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #f5f7ff;
}

h1, h2, h3 {
    color: #4B4BFF;
}

.stButton>button {
    background-color: #4B4BFF;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

.stNumberInput>div>div>input {
    border-radius: 10px;
}

.quote-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 22px;
    color:black;        
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

.login-box {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN PAGE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 AI Study Planner Login")

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.markdown('</div>', unsafe_allow_html=True)

else:

    # ---------------- LOAD DATA ----------------
    df = pd.read_csv("study_data.csv")

    # ---------------- SIDEBAR ----------------
    st.sidebar.title("📚 AI Study Planner")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Add Subject", "Charts", "Motivation"]
    )

    st.sidebar.write("---")
    st.sidebar.info("Stay Focused 🚀")

    # ---------------- DASHBOARD ----------------
    if menu == "Dashboard":

        st.title("📚 AI Study Planner")
        st.write("### Plan Smarter, Study Better 🚀")

        col1, col2 = st.columns(2)

        with col1:
            st.write("## 📖 Study Table")
            st.dataframe(df, use_container_width=True)

        with col2:

            completed = df[df["Status"] == "Completed"].shape[0]
            total = df.shape[0]

            progress = completed / total

            st.write("## 📈 Progress")
            st.progress(progress)

            st.metric(
                label="Completed Subjects",
                value=f"{completed}/{total}"
            )

        # AI Suggestion
        st.write("---")
        st.write("## 🤖 AI Suggestion")

        pending_subjects = df[df["Status"] == "Pending"]

        if not pending_subjects.empty:

            hardest = pending_subjects.sort_values(
                by="Hours",
                ascending=False
            ).iloc[0]

            st.info(
                f"Focus more on {hardest['Subject']} today. "
                f"It requires {hardest['Hours']} study hours."
            )

    # ---------------- ADD SUBJECT ----------------
    elif menu == "Add Subject":

        st.title("➕ Add New Subject")

        subject = st.text_input("Subject Name")

        hours = st.number_input(
            "Study Hours",
            min_value=1,
            max_value=12
        )

        status = st.selectbox(
            "Status",
            ["Pending", "Completed"]
        )

        if st.button("Add Subject"):

            new_data = pd.DataFrame({
                "Subject": [subject],
                "Hours": [hours],
                "Status": [status]
            })

            df = pd.concat([df, new_data], ignore_index=True)

            df.to_csv("study_data.csv", index=False)

            st.success("Subject Added Successfully!")

    # ---------------- CHARTS ----------------
    elif menu == "Charts":

        st.title("📊 Study Analytics")

        # Pie Chart
        pie_chart = px.pie(
            df,
            names="Subject",
            values="Hours",
            title="Study Hours Distribution"
        )

        st.plotly_chart(pie_chart, use_container_width=True)

        # Bar Chart
        bar_chart = px.bar(
            df,
            x="Subject",
            y="Hours",
            color="Status",
            title="Subject Wise Study Hours"
        )

        st.plotly_chart(bar_chart, use_container_width=True)

    # ---------------- MOTIVATION ----------------
    elif menu == "Motivation":

        st.title("🌟 Daily Motivation")

        quotes = [
            "Success starts with consistency.",
            "Small progress is still progress.",
            "Discipline beats motivation.",
            "Study now, shine later.",
            "Dream big and dare to fail.",
            "Push yourself because no one else will."
        ]

        quote = random.choice(quotes)

        st.markdown(
            f"""
            <div class="quote-box">
                ✨ {quote}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.balloons()
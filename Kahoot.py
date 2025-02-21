import openbadges_bakery
import streamlit as st
import random
import json
from openbadges_bakery import bake, unbake

# ---- Simulate Kahoot Quiz Data (since no official API) ---- #
quizzes = {
    "Quiz 1": {"questions": ["Q1: Capital of India?", "Q2: 2+2=?"], "answers": [["Delhi", "Mumbai", "Chennai", "Kolkata"], ["3", "4", "5", "6"]], "correct": [0, 1]},
    "Quiz 2": {"questions": ["Q1: Largest ocean?", "Q2: Fastest land animal?"], "answers": [["Atlantic", "Indian", "Arctic", "Pacific"], ["Cheetah", "Lion", "Tiger", "Deer"]], "correct": [3, 0]}
}

# ---- Streamlit App ---- #
st.title("Samarth - Kahoot Quiz & Badge Integration")

# Sidebar for user role
role = st.sidebar.selectbox("Select Role", ["Teacher", "Student"])

# ---- Teacher Interface ---- #
if role == "Teacher":
    st.header("📊 Teacher Dashboard")

    quiz_name = st.selectbox("Select a Quiz", list(quizzes.keys()))

    if st.button("Start Quiz 🏁"):
        # Simulate Game PIN generation
        game_pin = random.randint(100000, 999999)
        st.success(f"Quiz Started! Share this Game PIN with your students: **{game_pin}**")

        # Store Game PIN and quiz in session state
        st.session_state["game_pin"] = game_pin
        st.session_state["current_quiz"] = quiz_name

# ---- Student Interface ---- #
elif role == "Student":
    st.header("🎯 Join Kahoot Quiz")

    username = st.text_input("Enter your Username")
    game_pin_input = st.text_input("Enter Game PIN")

    if st.button("Join Quiz ✅"):
        if game_pin_input == str(st.session_state.get("game_pin", "")):
            st.success(f"Welcome {username}! You've joined {st.session_state['current_quiz']}.")

            # Display Quiz
            quiz_data = quizzes[st.session_state["current_quiz"]]
            score = 0

            for i, question in enumerate(quiz_data["questions"]):
                st.write(question)
                answer = st.radio(f"Select your answer for Q{i+1}", quiz_data["answers"][i], key=f"q{i}")

                if st.button(f"Submit Answer Q{i+1}", key=f"submit{i}"):
                    if quiz_data["answers"][i].index(answer) == quiz_data["correct"][i]:
                        st.success("Correct! ✅")
                        score += 1
                    else:
                        st.error("Wrong Answer ❌")

            st.write(f"Your Final Score: {score}/{len(quiz_data['questions'])}")

            # Generate Badge if score is high
            if score >= len(quiz_data['questions']) / 2:
                badge_data = {
                    "@context": "https://w3id.org/openbadges/v2",
                    "type": "BadgeClass",
                    "id": f"https://samarth.edu.in/badges/{username}-quiz-master",
                    "name": "Quiz Master",
                    "description": "Awarded for outstanding performance in quizzes",
                    "image": "https://samarth.edu.in/badges/quiz-master.png",
                    "criteria": {"narrative": "Scored above average in quizzes"},
                    "issuer": {
                        "id": "https://samarth.edu.in",
                        "name": "Samarth University",
                        "url": "https://samarth.edu.in",
                        "email": "admin@samarth.edu.in"
                    }
                }

                # Save badge
                with open(f"{username}_badge.json", "w") as f:
                    json.dump(badge_data, f, indent=4)

                bake(f"{username}_badge.json", f"{username}_badge.png")
                st.image(f"{username}_badge.png", caption="🏅 Congratulations! You earned the Quiz Master badge!")
        else:
            st.error("Invalid Game PIN. Please try again.")
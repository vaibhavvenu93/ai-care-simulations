import streamlit as st

st.set_page_config(page_title="AI Care Simulation", page_icon="🧠")

st.title("🧠 AI Care Simulation")
st.write("Gamified prototype for neurodivergence care workforce training.")

st.divider()

scenarios = {
    "Level 1: Transition Refusal": {
        "difficulty": "Beginner",
        "scenario": "A child refuses to transition from playtime to class and starts crying."
    },
    "Level 2: Sensory Overload": {
        "difficulty": "Beginner",
        "scenario": "A learner becomes overwhelmed by loud noise during a group activity."
    },
    "Level 3: Task Avoidance": {
        "difficulty": "Intermediate",
        "scenario": "A child throws a toy when asked to complete a worksheet."
    },
    "Level 4: Parent Question": {
        "difficulty": "Intermediate",
        "scenario": "A parent asks why reinforcement is important in behavior support."
    },
    "Level 5: Low Engagement": {
        "difficulty": "Advanced",
        "scenario": "A student avoids eye contact and does not respond during a session."
    }
}

scenario_name = st.selectbox("Choose a simulation mission", list(scenarios.keys()))
selected = scenarios[scenario_name]

col1, col2 = st.columns(2)
with col1:
    st.metric("Mission Difficulty", selected["difficulty"])
with col2:
    st.metric("Possible XP", "100 XP")

st.subheader("Scenario")
st.write(selected["scenario"])

response = st.text_area("How would you respond?", height=160)

def check_words(text, words):
    lowered = text.lower()
    return any(word in lowered for word in words)

def evaluate_response(text):
    categories = {
        "Empathy": {
            "words": ["calm", "understand", "support", "comfort", "patient", "gentle"],
            "feedback": "You considered emotional regulation and empathy."
        },
        "Safety": {
            "words": ["safe", "space", "quiet", "reduce", "remove", "environment"],
            "feedback": "You considered safety or environmental adjustment."
        },
        "Observation": {
            "words": ["observe", "trigger", "behavior", "data", "antecedent", "notice"],
            "feedback": "You considered observation, triggers, or behavior patterns."
        },
        "Reinforcement": {
            "words": ["reinforce", "reward", "praise", "positive", "preferred", "motivate"],
            "feedback": "You included reinforcement or positive behavior support."
        },
        "Next Step": {
            "words": ["next", "then", "routine", "plan", "step", "transition"],
            "feedback": "You included a clear practical next step."
        }
    }

    scores = {}
    feedback = []

    for category, data in categories.items():
        if check_words(text, data["words"]):
            scores[category] = 2
            feedback.append("Good: " + data["feedback"])
        else:
            scores[category] = 0
            feedback.append("Improve: Add more about " + category.lower() + ".")

    total_score = sum(scores.values())
    xp = total_score * 10

    if total_score >= 8:
        badge = "🏅 Care Simulation Badge Unlocked"
        level = "Behavioral Apprentice"
    elif total_score >= 5:
        badge = "🌱 Progress Badge Earned"
        level = "Care Explorer"
    else:
        badge = "🔁 Try Again Mission"
        level = "Learner"

    return total_score, scores, feedback, xp, badge, level

if st.button("Evaluate Response"):
    if not response.strip():
        st.warning("Please write your response first.")
    else:
        total_score, scores, feedback, xp, badge, level = evaluate_response(response)

        st.divider()

        st.subheader("Competency Result")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{total_score}/10")
        with col2:
            st.metric("XP Earned", f"{xp} XP")
        with col3:
            st.metric("Current Level", level)

        st.progress(total_score / 10)

        st.success(badge)

        st.subheader("Competency Breakdown")
        for category, score in scores.items():
            st.write(f"**{category}:** {score}/2")
            st.progress(score / 2)

        st.subheader("Feedback")
        for item in feedback:
            st.write("- " + item)

        st.subheader("Strong Response Structure")
        st.write("""
1. Stay calm and ensure safety.  
2. Observe what triggered the behavior.  
3. Reduce emotional or sensory pressure.  
4. Use clear and simple communication.  
5. Reinforce the next positive behavior.  
6. Document observations for supervision.
""")

        st.info("Prototype note: this is currently rule-based scoring. Future versions can use AI evaluation, adaptive simulation paths, and ABAT/RBT readiness scoring.")

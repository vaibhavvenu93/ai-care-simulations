import streamlit as st

st.set_page_config(page_title="AI Care Simulation", page_icon="🧠")

st.title("🧠 AI Care Simulation")
st.write("Prototype for neurodivergence care workforce training.")

scenarios = {
    "Transition Refusal": "A child refuses to transition from playtime to class and starts crying.",
    
    "Sensory Overload": "A learner becomes overwhelmed by loud noise during a group activity.",

    "Task Avoidance": "A child throws a toy when asked to complete a worksheet.",

    "Parent Question": "A parent asks why reinforcement is important in behavior support.",

    "Low Engagement": "A student avoids eye contact and does not respond during a session."
}

scenario_name = st.selectbox(
    "Choose a scenario",
    list(scenarios.keys())
)

st.subheader("Scenario")
st.write(scenarios[scenario_name])

response = st.text_area(
    "How would you respond?",
    height=150
)

def evaluate_response(text):

    score = 0
    feedback = []

    empathy_words = [
        "calm",
        "understand",
        "support",
        "safe",
        "comfort",
        "patient"
    ]

    reinforcement_words = [
        "reinforce",
        "reward",
        "praise",
        "positive"
    ]

    safety_words = [
        "safe",
        "space",
        "quiet",
        "reduce"
    ]

    observation_words = [
        "observe",
        "trigger",
        "behavior",
        "data"
    ]

    next_step_words = [
        "next",
        "then",
        "routine",
        "plan"
    ]

    lowered = text.lower()

    if any(word in lowered for word in empathy_words):
        score += 2
        feedback.append("Good: empathy and emotional regulation considered.")

    if any(word in lowered for word in reinforcement_words):
        score += 2
        feedback.append("Good: reinforcement or positive behavior support included.")

    if any(word in lowered for word in safety_words):
        score += 2
        feedback.append("Good: safety or environmental adjustment considered.")

    if any(word in lowered for word in observation_words):
        score += 2
        feedback.append("Good: behavioral observation or trigger analysis included.")

    if any(word in lowered for word in next_step_words):
        score += 2
        feedback.append("Good: practical next step included.")

    if score == 0:
        feedback.append(
            "Try including empathy, safety, reinforcement, observation, and next steps."
        )

    return score, feedback

if st.button("Evaluate Response"):

    if not response.strip():
        st.warning("Please write your response first.")

    else:

        score, feedback = evaluate_response(response)

        st.subheader("Competency Score")
        st.metric("Score", f"{score}/10")

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

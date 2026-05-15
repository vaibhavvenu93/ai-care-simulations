
import streamlit as st
import google.generativeai as genai

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="AI Care Simulation",
    page_icon="🧠"
)

# ---------------------------
# GEMINI SETUP
# ---------------------------

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.0-flash")

# ---------------------------
# HEADER
# ---------------------------

st.title("🧠 AI Care Simulation")

st.write(
    "Gamified prototype for neurodivergence care workforce training."
)

st.divider()

# ---------------------------
# SCENARIOS
# ---------------------------

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

scenario_name = st.selectbox(
    "Choose a simulation mission",
    list(scenarios.keys())
)

selected = scenarios[scenario_name]

# ---------------------------
# TOP METRICS
# ---------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric("Mission Difficulty", selected["difficulty"])

with col2:
    st.metric("Possible XP", "100 XP")

# ---------------------------
# SCENARIO
# ---------------------------

st.subheader("Scenario")

st.write(selected["scenario"])

response = st.text_area(
    "How would you respond?",
    height=180
)

# ---------------------------
# AI EVALUATION
# ---------------------------

def evaluate_with_gemini(scenario, learner_response):

    prompt = f"""
You are an expert behavioral therapy supervisor evaluating an early-stage neurodivergence care learner.

Evaluate the learner response professionally.

SCENARIO:
{scenario}

LEARNER RESPONSE:
{learner_response}

Evaluate across:
1. Empathy
2. Safety
3. Observation
4. Reinforcement
5. Practical Next Step

Return:
- A score out of 10
- Strengths
- Weaknesses
- Coaching advice
- A suggested improved response

Be constructive and supportive.
"""

    ai_response = model.generate_content(prompt)

    return ai_response.text

# ---------------------------
# BUTTON
# ---------------------------

if st.button("Evaluate Response"):

    if not response.strip():

        st.warning("Please write your response first.")

    else:

      with st.spinner("AI supervisor evaluating response..."):

    try:
        evaluation = evaluate_with_gemini(
            selected["scenario"],
            response
        )

        st.divider()
        st.subheader("🧠 AI Evaluation")
        st.write(evaluation)
        st.success("Simulation Complete")

    except Exception:
        st.divider()
        st.subheader("🧠 AI Evaluation Temporarily Unavailable")
        st.warning("The AI evaluator hit a temporary quota or availability limit. Showing fallback competency guidance instead.")

        st.subheader("Fallback Competency Guidance")
        st.write("""
A strong response should include:

1. Empathy and emotional regulation  
2. Safety or environmental adjustment  
3. Observation of triggers and behavior patterns  
4. Reinforcement of positive behavior  
5. A clear next step  
6. Documentation for supervision
""")

        st.success("Fallback Simulation Complete")

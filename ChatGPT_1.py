import openai
import streamlit as st

# Set the OpenAI API key
openai.api_key = 'your-api-key-here'  # Replace with your API key

# Predefined interview questions
questions = [
    "Can you tell me about yourself?",
    "What is your greatest strength?",
    "Describe a challenging situation you faced at work and how you handled it.",
    "Where do you see yourself in 5 years?",
    "Why should we hire you?"
]

# Streamlit web interface for interview simulation
def interview_simulation():
    responses = []
    for i, question in enumerate(questions):
        st.write(f"Question {i+1}: {question}")
        user_input = st.text_input(f"Your answer to question {i+1}:", key=f"answer_{i}")
        if user_input:
            responses.append(user_input)
    return responses

# Function to evaluate each response
def evaluate_response(question, answer):
    prompt = f"Evaluate the following answer to the question '{question}':\n\nAnswer: {answer}\n\nConsider relevance, clarity, and depth."
    
    try:
        # OpenAI API call to evaluate the response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert interviewer providing feedback and evaluation for an interview."},
                {"role": "user", "content": prompt}
            ]
        )
        evaluation = response['choices'][0]['message']['content']
        return evaluation
    except Exception as e:
        # Handle any errors that occur
        st.write(f"Error: {e}")
        return "Unable to evaluate the response."

# Function to score responses based on evaluation
def score_response(evaluation):
    if "excellent" in evaluation.lower():
        return 10
    elif "good" in evaluation.lower():
        return 8
    elif "adequate" in evaluation.lower():
        return 6
    elif "poor" in evaluation.lower():
        return 4
    else:
        return 2

# Function to evaluate and score the entire interview
def evaluate_and_score(responses):
    total_score = 0
    for i, answer in enumerate(responses):
        evaluation = evaluate_response(questions[i], answer)
        score = score_response(evaluation)
        total_score += score
        st.write(f"Evaluation for Question {i+1}: {evaluation}")
        st.write(f"Score: {score}/10\n")
    
    # Calculate average score
    if len(questions) > 0:
        average_score = total_score / len(questions)
        st.write(f"Final Score: {average_score}/10")
    else:
        st.write("No questions were evaluated.")

    # Final feedback based on score
    if average_score >= 8:
        st.write("Excellent performance!")
    elif average_score >= 6:
        st.write("Good performance, but there's room for improvement.")
    else:
        st.write("Significant improvement needed.")

# Streamlit app setup
st.title('AI Job Interview Simulation')

# Start the interview process on button click
if st.button("Start Interview"):
    responses = interview_simulation()
    if len(responses) == len(questions):  # Ensure all questions are answered
        evaluate_and_score(responses)

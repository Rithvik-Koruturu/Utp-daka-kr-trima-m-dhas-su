from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables (like your Google API key)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is set; if not, display an error message
if not api_key:
    st.error("API key is not set. Please check your .env file.")
else:
    # Configure the generative AI model with the provided API key
    genai.configure(api_key=api_key)

    # Function to get a response for text input using the gemini-pro model
    def get_gemini_text_response(description, moods):
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])

        # Emotional context for the model
        emotional_prompt = f"User is feeling {' and '.join(moods)}. "
        prompt = f"{emotional_prompt}Incident Description: {description}"

        # Get response from the AI
        response = chat.send_message(prompt, stream=True)
        
        return response

    # Initialize Streamlit app
    st.set_page_config(page_title="NeuroNova - Emotional AI Assistant")
    st.header("NeuroNova - Emotional AI Assistant")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Mood Selection using checkboxes
    st.subheader("Select Your Moods")
    mood_options = ["😊 Happy", "😟 Sad", "😠 Angry", "😰 Anxious", "😐 Neutral"]
    selected_moods = st.multiselect("How are you feeling today?", mood_options)

    # Incident description input
    st.subheader("Incident Description")
    incident_description = st.text_area("Describe the incident or situation:")

    # Button to get a response
    if st.button("Get Response"):
        if incident_description and selected_moods:
            response = get_gemini_text_response(incident_description, selected_moods)
            response_text = []

            # Collect response text
            for chunk in response:
                try:
                    response_text.append(chunk.text)
                except AttributeError:
                    st.error("Received an unexpected response format from the AI.")
                    break
            
            if response_text:
                full_response = "\n".join(response_text)
                st.write(full_response)
                st.session_state['chat_history'].append(("You", incident_description))
                st.session_state['chat_history'].append(("Bot", full_response))
        else:
            st.error("Please fill in both the incident description and select at least one mood.")

    # Display chat history
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    # Additional sidebar functionalities
    st.sidebar.markdown("© 2024 Team NeuroNova")

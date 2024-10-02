from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# Load environment variables (like your Google API key)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is set; if not, display an error message
if not api_key:
    st.error("API key is not set. Please check your .env file.")
else:
    # Configure the generative AI model with the provided API key
    genai.configure(api_key=api_key)

    # Function to get the response from the generative AI model for images
    def get_image_analysis(image_data):
        model = genai.GenerativeModel('gemini-1.5-flash')
        try:
            response = model.generate_content([image_data, "Analyze the educational content in this image."])
            return response.text
        except Exception as e:
            st.error(f"Error in image analysis: {e}")
            return "Analysis failed."

    # Function to get a response for text input using the gemini-pro model
    def get_text_response(question, image_context=None):
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])

        if image_context:
            combined_prompt = f"Context: {image_context}\nQuestion: {question}"
            response = chat.send_message(combined_prompt, stream=True)
        else:
            response = chat.send_message(question, stream=True)

        return response

    # Initialize Streamlit app
    st.set_page_config(page_title="AI-Powered Learning Companion")

    st.header("AI-Powered Learning Companion")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Multi-image upload functionality
    uploaded_files = st.file_uploader("Upload educational images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    image_contexts = []
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)

            # Convert the image to a binary format for analysis
            image_data = BytesIO()
            image.save(image_data, format='PNG')  # Save as PNG or JPEG based on the file
            image_data.seek(0)  # Move to the beginning of the BytesIO buffer

            # Analyze the image and get context
            image_context = get_image_analysis(image_data)
            image_contexts.append(image_context)

        # Display the analysis results for each image
        st.subheader("Image Analysis Results:")
        for idx, context in enumerate(image_contexts):
            st.write(f"Analysis for Image {idx + 1}: {context}")

    # Unified input field for text queries
    user_input = st.text_input("Ask a question (related to the images or any educational topic):")

    # Button to get a response
    if st.button("Get Response"):
        if user_input:
            combined_image_context = "\n".join(image_contexts) if image_contexts else None
            response = get_text_response(user_input, combined_image_context)
            
            # Display response
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("You", user_input))
                st.session_state['chat_history'].append(("Bot", chunk.text))

    # Display chat history
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    # Future Opportunities Section
    st.markdown("### Future Opportunities:")
    st.markdown("- Enhanced multi-modal learning: Incorporating video, audio, and other forms of media.")
    st.markdown("- Adaptive learning: Personalized learning paths based on user performance.")
    st.markdown("- Gamification: Game-based mechanics to enhance engagement.")
    st.markdown("- Cross-platform integration: Mobile apps and educational platforms.")
    st.markdown("- Subject-specific expansions: Specialized AI capabilities for fields like medicine, law, or engineering.")

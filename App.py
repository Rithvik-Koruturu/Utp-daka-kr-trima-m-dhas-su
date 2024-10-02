import streamlit as st
from deep_translator import GoogleTranslator  # Import the translator
from PIL import Image

# Title of the application
st.title("Course Creation Copilot")

# Step 1: Course Structure Design
st.header("1. Design Course Structure")
course_title = st.text_input("Course Title:")
num_modules = st.number_input("Number of Modules:", min_value=1, value=1)

modules = []
for i in range(num_modules):
    module_name = st.text_input(f"Module {i + 1} Name:")
    modules.append(module_name)

# Step 2: Language Translation Copilot
st.header("2. Translate Course Content")
content_to_translate = st.text_area("Enter content to translate:")
selected_language = st.selectbox("Select Language:", ["hi", "ta", "bn", "kn"], format_func=lambda x: {
    "hi": "Hindi",
    "ta": "Tamil",
    "bn": "Bengali",
    "kn": "Kannada"
}[x])

if st.button("Translate"):
    # Translate content using deep_translator
    translated = GoogleTranslator(source='auto', target=selected_language).translate(content_to_translate)
    st.write("Translated Content:")
    st.write(translated)

# Step 3: Multimedia Enhancements
st.header("3. Add Multimedia Enhancements")

# Image Copilot
st.subheader("Image Copilot")
uploaded_image = st.file_uploader("Upload an image for your course (optional):", type=["jpg", "jpeg", "png"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Final Step: Save Course Structure
if st.button("Save Course Structure"):
    st.write("Course Title:", course_title)
    st.write("Modules:", modules)
    st.success("Course structure saved successfully!")

st.markdown("---")
st.markdown("### Future Enhancements:")
st.markdown("- Integrate a database to save and manage courses.")
st.markdown("- Add options for creating quizzes and assessments.")
st.markdown("- Provide analytics on course engagement and effectiveness.")

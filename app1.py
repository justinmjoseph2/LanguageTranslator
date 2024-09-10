import streamlit as st
from transformers import pipeline
from langdetect import detect, DetectorFactory

# To ensure consistent results from langdetect
DetectorFactory.seed = 0

# List of supported languages with their full names
LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'it': 'Italian',
    'nl': 'Dutch',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'hi': 'Hindi',
    'ml': 'Malayalam',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'uk': 'Ukrainian',
    'pl': 'Polish',
    'tr': 'Turkish',
    'vi': 'Vietnamese',
    'sv': 'Swedish',
    'fi': 'Finnish',
    'no': 'Norwegian',
    'da': 'Danish',
    'cs': 'Czech',
    'el': 'Greek',
    'he': 'Hebrew',
    'hu': 'Hungarian',
    'ro': 'Romanian',
    'sk': 'Slovak',
    'th': 'Thai',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ur': 'Urdu',
    'fa': 'Persian',
    'id': 'Indonesian',
    'ms': 'Malay',
    'tl': 'Tagalog',
    'sr': 'Serbian',
    'bg': 'Bulgarian'
}

# Reverse the LANGUAGES dictionary for easier lookup
LANG_CODES = {v: k for k, v in LANGUAGES.items()}

# Initialize translation pipeline
def load_translation_pipeline(src_lang, tgt_lang):
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    translation_pipeline = pipeline("translation", model=model_name)
    return translation_pipeline

# Streamlit app layout
st.title("Language Translator using Seq2Seq Model")

# User input for target language
tgt_lang_full = st.selectbox("Select Target Language", list(LANGUAGES.values()))
tgt_lang = LANG_CODES[tgt_lang_full]

# User input for text
text = st.text_area("Enter Text to Translate")

# Translate button
if st.button("Translate"):
    if text:
        with st.spinner("Detecting language..."):
            # Automatically detect the source language
            try:
                src_lang = detect(text)
                src_lang_full = LANGUAGES.get(src_lang, "Unknown")
                st.write(f"Detected source language: {src_lang_full}")

                # Load translation pipeline
                with st.spinner("Loading translation model..."):
                    translation_pipeline = load_translation_pipeline(src_lang, tgt_lang)

                # Perform translation
                translated_text = translation_pipeline(text)[0]['translation_text']

                # Display the result
                st.success("Translation Complete!")
                st.write("Translated Text:", translated_text)
            except Exception as e:
                st.error(f"Error detecting language or translating: {str(e)}")
    else:
        st.warning("Please enter some text to translate.")

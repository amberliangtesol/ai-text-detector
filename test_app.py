import streamlit as st

st.title("Test App")

text = st.text_area("Enter text", "Test text")

if st.button("Test"):
    st.write("Button clicked!")
    st.write(f"Text: {text}")
    st.success("Working!")
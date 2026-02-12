import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="My Smart AI Bot", page_icon="🤖")
st.title("🤖 My Smart AI Bot")

TOKEN = st.secrets["HF_TOKEN"]
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=TOKEN)

if st.button("Clear Chat 🗑️"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("assistant"):
        full_response = ""
        try:
          
            for message in client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                stream=True,
            ):
                token = message.choices[0].delta.content
                if token:
                    full_response += token
            st.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            full_response = "Sorry, Llama is taking a break. Try again in a minute!"
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
                
         




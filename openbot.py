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
            
            response = client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
            )
            
            if response.choices and response.choices[0].message.content:
                full_response = response.choices[0].message.content
                st.markdown(full_response)
            else:
                full_response = "I couldn't generate a response. Please try again!"
                st.warning(full_response)
                
        except Exception as e:
            full_response = "System is a bit busy. Please click 'Clear Chat' and try once more!"
            st.error(f"Error: {e}")
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

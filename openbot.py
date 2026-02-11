import streamlit as st
from huggingface_hub import InferenceClient


TOKEN = st.secrets["HF_TOKEN"]
client = InferenceClient(api_key=TOKEN)

st.title("🤖 My Smart AI Bot")
st.write("Ask me anything!")

user_input = st.text_input("Unnga kelvi enna?", placeholder="Example: What is titanium?")

if st.button("Get Answer"):
    if user_input:
        with st.spinner("AI is thinking..."):
            try:
                
                response = client.chat_completion(
                    model="meta-llama/Llama-3.2-1B-Instruct",
                    messages=[{"role": "user", "content": user_input}],
                    max_tokens=500
                )
                
                
                answer = response.choices[0].message.content
                st.success("Done!")
                st.markdown("### Answer:")
                st.write(answer)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question!")

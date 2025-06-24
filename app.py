#we use streamlit framework from python
import streamlit as st 
from ibm_watsonx_ai.foundation_models import Model #we need foundation model means llm

#we need to give some credentials of ibm
api_key="your ibm project api key"
project_id="your ibm project id"
base_url="your watson url"
#initialize model
model_id="ibm/granite-13b-instruct-v2"

#hello/welcome comment
st.title("CHAT BOT")
st.caption(f"Using model:{model_id}")
#user prompts need to be shown and response also
#so a chat history
#session state is checking if all things are present 
# like memory working etc is taken care by this session state

if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[]
#2 is stride or step for space
for i in range(0,len(st.session_state.chat_history),2):
    if i<len(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(st.session_state.chat_history[i]) 
            #st.chat msg is user prompt store in history
    if i+1<len(st.session_state.chat_history):
        with st.chat_message("Assistant"):
            st.chat_message("assistant").write(st.session_state.chat_history[i+1])
    
    
user_prompt=st.chat_input("Ask me anything ")
if user_prompt:
    with st.chat_message("user"):
       st.write(user_prompt)
    st.session_state.chat_history.append(user_prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                model=Model(
                    model_id=model_id,
                    credentials={
                        "apikey":api_key,
                        "url":base_url
                    },
                    project_id=project_id
                )
                response=model.generate_text(
                    prompt=f"user:{user_prompt}\n Assistant:",
                    params={
                        "max_mew_tokens":200,
                        "temperature":0.7,
                        "top_p":1.0,
                        "decode_method":"sample",
                        "stop_response":["<|endoftext|>","User"]
                    })
                bot_response=response['generated_text']if isinstance(response,dict) and 'generated_text' in response else str(response)
                st.write(bot_response)
                st.session_state.chat_history.append(bot_response)
            except Exception as e:
                st.error(f"An error occured:{e}")
                st.info("An error occured in processing your request please check your credentials again")
#virtual environment open commad prompt when you create a project you need to 
#do this create a virtual environment cause you create a requirements.txt 
#that contains all libraries needed even when you use different framework like fastapi or flask
#to create a virtual environment it will create a separate space in local storage
#to avoid having any interuption with libraries 
#if yesterday you used streamlit and pasdas 2.5 and today you used pandas 2.3 there is going to be a clash
#so to avoid this you create a virtual environment
#python -m venv .chat (.chat is virtual environment)
#you can see your folders now .chat
#now we need to activate the virtual environment .chat\Scripts\activate
#now file path in cmd is starts with .chat instead of c or d drive
#now install the requirements here
#D:\gen AI>chatbot\Scripts\activate          

#(chatbot) D:\gen AI>                                  
#there must be a requirements.txt file with libraries verions for big projects 
#if you send code to some friend and said to install these libraries he might install different versions and that version may not have the needed function
#its better to make virtual enviromnet and requirements.txt file




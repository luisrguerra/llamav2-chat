import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
import replicate

load_dotenv()

llama2_70b = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781"
llama2_13b = "a16z-infra/llama-2-13b-chat:2a7f981751ec7fdf87b5b91ad4db53683a98082e9ff7bfd12c8cd5ea85980a52"
#Falcon is expensive
falcon_40b_instruct="joehoover/falcon-40b-instruct:7eb0f4b1ff770ab4f68c3a309dd4984469749b7323a3d47fd2d5e09d58836d3c"
# Wizard coder not work well
wizardcoder_15b_v1_0 = "lucataco/wizardcoder-15b-v1.0:b8c554180169aa3ea1c8b95dd6af4c24dd9e59dce55148c8f3654752aa641c87"
vicuna_13b = "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b"

def generate_response(human_input):

	output = replicate.run(
		vicuna_13b,
		input={"prompt": human_input},)
	# The replicate/llama70b-v2-chat model can stream output as it's running. 
	# Collect all response parts into a list
	response_parts = []
	for item in output:
		response_parts.append(item)

	response = " ".join(response_parts)

	return response

st.title("Replicate Chatbot Demo")

if 'generated' not in st.session_state:
	st.session_state['generated'] = []

if 'past' not in st.session_state:
	st.session_state['past'] = []

def get_text():
	input_text = st.text_input(" ", key="input")
	return input_text

user_input = get_text()

if user_input:
	output = generate_response(user_input)
	st.session_state.past.append(user_input)
	st.session_state.generated.append(output)

if st.session_state['generated']:
	for i in range(len(st.session_state['generated'])):
		message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
		message(st.session_state["generated"][i], key=str(i))
#url variable is used to send the requests to the llm
llm = "llm_url"

#db variable is used to send requests to and from the database, specified for the user
db = "db_url"

#prompt variable is used to send prompt text to the llm
prompt = "text"

#attempts ping the llm, returns boolean on success/fail
def llm_connect(llm):
	return True

#connects the llm and the db entries for the user, returns boolean on success/fail
def db_llm_connect(db, llm):
	return True

#takes prompt for llm, sends to llm, returns string
def generate_text(prompt):
	return "response"
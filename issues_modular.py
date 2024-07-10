from github import Github, Auth
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.chat_models.bedrock import BedrockChat
from anthropic import AnthropicVertex
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.schema.runnable import RunnablePassthrough

gcp_region = 'us-east-1'
modelId = 'anthropic.claude-3-sonnet-20240229-v1:0'
google = AnthropicVertex(region=gcp_region, project_id="figma-code-fixer")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="cred.json"

template = '''
You are a GitHub Issues Creator. You will be provided the contents of a code file, and you will need to create a GitHub Issue in the format of 
Title: 
Description:
Labels:

The title of the issue must be short and direct to the point. 
The description of the issue must have:
1. all the relevant code that may cause issues
2. the severity of the issues
3. Cascading effects of the issue.
4. fixes of the issue.

All of this information must be described in a dictionary with the keys being the sections, and the values being the description of the sections.

Generate the title after creating the body of the issue.

Finally, based on the information and the title, generate three to four labels that are relevant to the code.

Formatting Instructions: {format_instructions}

If there are no prospective issues, and the code is in good working conditions, say so. Do not be overly critical, and only create issues that are relevant and impactful.
If the code follows all conventions, and has a good structure without bugs and issues, keep the body of the issue short or empty.

History: 
{history}


Formatting 
Current Conversation:

Code: {input}
Github Issue: 

'''


examples=[
    {
        "input": '''
def calculate_order_total(items):
    total_price = 0
    for item in items:
        total_price += item["price"]
    return total_price

# Example usage
order_items = [
    {"name": "Shirt", "price": 19.99},
    {"name": "Hat", "price": 12.50},
]

order_total = calculate_order_total(order_items)
print(f"Order total: ${order_total:.2f}")
''',
"output": '''
{"Title": "lack of coverage for discounts, edge cases, and negative price.

Description: The calculate_order_total function appears to be calculating the total price of items in an order. However, there might be an issue with how it handles potential discounts or negative prices.

Expected Behavior: The function should consider any discounts applied to the order and handle negative item prices appropriately (e.g., ignore them or throw an error).

Current Behavior:The code simply sums the price of each item without considering discounts or negative values. This could lead to inaccurate order totals.

Possible Solutions:
Add an optional argument to the function for a discount percentage.
Modify the loop to check for a "discount" key in the item dictionary and apply the discount if present.
Raise an exception if an item has a negative price.

Labels: bug, python
'''
    },
    {"input": '''
def github_push_and_pull(github_token, repo_url, git_branch, file_path, file_content, cc_id):
  # Authenticate with GitHub
  g = Github(github_token)

  repo = g.get_repo(repo_url)
  main_branch_sha = repo.get_branch('main').commit.sha

  # Check if the branch exists; create it if it doesn't
  try:
    repo.get_branch(git_branch)
  except GithubException:
    # Create a new branch based on 'main'
    repo.create_git_ref(ref=f"refs/heads/{git_branch}", sha=main_branch_sha)

  # Update/Create file logic
  try:
    # Update existing file
    existing_file = repo.get_contents(file_path, ref=git_branch)
    # ... (update logic)
  except GithubException:
    # Create new file
    # ... (create logic)

  # Pull Request Creation
  try:
    pull = repo.create_pull(
      title="Add/Update",
      body=f"File add/updated by Code Companion, id: {cc_id}",
      head=git_branch,
      base="main",
    )
    print("Pull Request created:", pull.html_url)
    return "1"
  except GithubException as e:
    # Handle pull request already exists
    if "A pull request already exists" in str(e):
      print("A pull request already exists for this branch. Please review the existing pull request.")
      return "2"
    else:
      return "3"


''',
     "output": '''

{Title: Lack of error handling in Except Block.     

Description: The github_push_and_pull function automates pushing and pulling code changes to a GitHub repository. However, there might be a potential logic error in how it handles existing files.

Current Behavior: The current code attempts to update an existing file within the try block. However, the update logic is not shown (... (update logic)).  If the update logic involves modifying the file content and then calling repo.update_file, there might be an issue.

Expected Behavior: The expected behavior is to update existing files or create new ones based on their presence in the repository.

Scenario:
The function attempts to update an existing file.
If the update fails due to insufficient permissions or other reasons, the except GithubException block is triggered.
Since the update failed, the code then attempts to create a new file in the else block because the except block doesn't explicitly handle the update failure.

Possible Consequence: This could lead to a situation where the function tries to create a duplicate file instead of handling the update failure gracefully.

Possible Solution:

Move the update logic for the existing file out of the try block.
If the update fails, handle the exception and potentially retry the update or provide a more informative error message.
Alternatively, consider refactoring the logic to check the update success before attempting to create a new file.
Labels: bug, python
    }
'''}, 
{"input": '''
import nltk

nltk.download('punkt')  # Download tokenizer if not already installed

def summarize_text(text, max_length=100):

  if max_length <= 0:
    raise ValueError("Maximum summary length must be greater than zero.")

  try:
    # Tokenize text into sentences
    sentences = nltk.sent_tokenize(text)

    # Calculate sentence scores based on position and word overlap
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
      score = 1.0 - abs(i - len(sentences) / 2)  # Positional weight
      for other_sentence in sentences:
        if i != sentences.index(other_sentence):
          overlap = len(set(sentence.split()) & set(other_sentence.split()))
          score += overlap  # Overlap weight
      sentence_scores[sentence] = score

    # Sort sentences by score, descending
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Create summary by selecting top-ranked sentences within limit
    summary = ""
    word_count = 0
    for sentence in ranked_sentences:
      if word_count + len(sentence.split()) <= max_length:
        summary += sentence + " "
        word_count += len(sentence.split())
      else:
        break

    return summary.strip()

  except Exception as e:
    print(f"Error during summarization: {e}")
    return "An error occurred while summarizing the text."
''',
"output":'''
This code accounts for all possible edges. It has excellent flow of control, data assignment, and order of operations. There are no apparent issues with this code.

'''}
]

class outputDict(BaseModel):
    Title: str = Field(description="Title of the Issue")
    Description: str = Field(description="Primary description of the Issue")
    Behavior: dict = Field(description="Dictionary of the Current Behavior and Expected Behavior")
    Solution: str = Field(description="Provided Solution for the issue")


parser = JsonOutputParser(pydantic_object=outputDict)
issues_prompt= PromptTemplate(
    input_variables = ["input", "history"],
    template=template,
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

def setup_memory():
    example_memory = ConversationBufferMemory(human_prefix="Code", ai_prefix="GitHub Issue", memory_key="conversation")
    for example in examples:
        example_memory.save_context({"Code:": example["input"]}, {"Github Issue":example["output"]})

    return example_memory


class outputDict(BaseModel):
    Title: str = Field(description="Title of the Issue")
    Description: str = Field(description="Primary description of the Issue")
    Behavior: dict = Field(description="Dictionary of the Current Behavior and Expected Behavior")
    Solution: str = Field(description="Provided Solution for the issue")
    


def create_brain():
    
    llm = ChatVertexAI(model_id=modelId, client=google, max_output_tokens = 2048)
    mem = setup_memory()
    
   #print(type(mem.load_memory_variables({})))
    
    #conv = ConversationChain(llm=llm, memory=mem, verbose=False, prompt = issues_prompt)
    conv = ( {"input": RunnablePassthrough(),"history": lambda _:mem.load_memory_variables({})["conversation"]}| issues_prompt | llm | parser)
    
    return conv

test = '''
def factorial(number):

  if number < 0:
    return "Factorial is not defined for negative numbers"
  factorial = 1
  for i in range(1, number + 1):
    factorial -= i
  return factorial
'''
a = create_brain()
print(a.invoke({"input": test}))






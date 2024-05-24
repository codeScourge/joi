from tools import AskBrave
import dotenv
import dspy
import os

dotenv.load_dotenv()


# --- loading models
model = dspy.OpenAI(model='gpt-3.5-turbo-1106', api_key=os.getenv("OPENAI_KEY"))
dspy.configure(lm=model)
    

# --- Module
class MyModule(dspy.Module):
    def __init__(self, tools:list):
        # by default, it would have the dspy.Retrieve tool set
        self.layer = dspy.ReAct("question -> answer", tools=tools)
        
    def forward(self, question):
        return self.layer(question=question).answer
    
    
if __name__ == "__main__":
    bot = MyModule(tools=[AskBrave()])
    
    answer = bot("Can you find out, what happend in Hamburg today?")
    print("\n\n########### AI GOT FOLLOWING DATA ###########\n\n")
    print(answer)
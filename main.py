
from dotenv import load_dotenv
import os

load_dotenv(".env")


from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage, AnyMessage
from workflow.agent import agent



def cprint(str):
    print("="*40)
    print(" "*17, str)
    print("="*40)
    

    

if __name__ == "__main__": 
    conversation = []
    userInput = ""
    output = ""

    while True:
        cprint("INPUT")
        userInput = input()
        print()
        try:
            conversation, output = agent(userInput, conversation)   
        except:
            print("agent failed")
            output=""
            conversation = [*conversation, HumanMessage(content=str(input))]
        cprint("OUTPUT")
        print(output)
        print()

        print("="*90)
        print(conversation)
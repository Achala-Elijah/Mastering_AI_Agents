from dotenv import load_dotenv
import os

load_dotenv("../.env")


from graph import createWorkflow
from state import State




#I want you to test me on matter inscience i want four short questions each with true or false.


graph = createWorkflow()

initialState = State(
    input="can u search what matter is for me?",
    output="",
    transcribedText="",
    isTranscribed=False,
    nextRoute=[],
    plannerMessages=[],
    explainerMessages=[],
    quizGeneratorMessages=[],
    summarizerMessages=[],
    plannerToolMessages=[],
    explainerToolMessages=[],
    conversationMessages=[],
)

result = graph.invoke(initialState, config={"configurable": {"max_iterations": 10}})

print(result)
print("="*15)
print(result["output"])
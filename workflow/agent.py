

from dotenv import load_dotenv
import os

load_dotenv("../.env")


from workflow.graph import createWorkflow
from workflow.state import State







def agent(input, conversationMessages):
    graph = createWorkflow()
    
    initialState = State(
    input=input,
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
    conversationMessages=conversationMessages,
    )
    
    result = graph.invoke(initialState, config={"configurable": {"max_iterations": 10}})
    
    return result, result["output"]
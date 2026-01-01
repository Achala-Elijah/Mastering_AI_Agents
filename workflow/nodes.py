from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage, AnyMessage
from langchain_groq import ChatGroq
import os
from workflow.state import *
from workflow.prompts import *
from workflow.tools import *




planner = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GAPI"))


plannerLlm = planner.with_structured_output(ManagerOuputFormat)
explainerLlm = llm.bind_tools(explainerTools)







def plannerNode(state: State):
    plannerMessages = state["plannerMessages"]
    conversationMessages = state["conversationMessages"]
    transcribedText = state["transcribedText"]
    isTranscribed = state["isTranscribed"]
    input = state["input"]
    
    
    if not plannerMessages:
        plannerMessages = [HumanMessage(content=str(input))]
    
    messages = [SystemMessage(content=str(plannerPrompt)), *conversationMessages, *plannerMessages]
    
    #check for error here
    response = plannerLlm.invoke(messages)
    
    nextRoute = response.nextRoute
    tool_calls = response.tool_calls
    tool_calls = [tc.dict() for tc in tool_calls]
    
    return {
        "nextRoute": nextRoute,
        "plannerMessages": [AIMessage(content=str(nextRoute), tool_calls=tool_calls)],
        "isTranscribed": False,
        **({"conversationMessages": [HumanMessage(content=str(input)), ToolMessage(content=transcribedText, tool_call_id="transcribe")]} if isTranscribed else {"conversationMessages": [HumanMessage(content=str(input))]})
    }
    
    



def plannerToolsNode(state:State):
    lastPlannerMessage = state["plannerMessages"][-1]
    
    tool_calls = lastPlannerMessage.tool_calls
    transcribedText = ""
    tools_messages = []
    
    registered_tools = {fn.__name__: fn for fn in tools}
    
    for tc in tool_calls:
        name = tc["name"]
        tool_funt = registered_tools.get(name)
        if tool_funt:
            result = tool_funt(**tc["args"])
            tools_messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
            if name == "transcribe":
                transcribedText = result
                
    return {
        "plannerToolMessages": tools_messages,
        "plannerMessages": tools_messages,
        **({"transcribedText": transcribedText, "isTranscribed": True} if transcribedText else {"isTranscribed": False}),
    }
    
    
    
    
    
def explainerNode(state: State):
    explainerMessages = state["plannerMessages"]
    conversationMessages = state["conversationMessages"]
    input = state["input"]
    
    if not explainerMessages:
        explainerMessages = [HumanMessage(content=str(input))]
        
    messages = [SystemMessage(content=str(explainerPrompt)), *conversationMessages]
    
    #check for error
    response = explainerLlm.invoke(messages)
    
    return {
        "output": response.content,
        "explainerMessages": [*explainerMessages, AIMessage(content=str(response.content), tool_calls=response.tool_calls)],
        "conversationMessages": [AIMessage(content=str(response.content))]
    }
    
    
    
    
def explainerToolsNode(state: State):
    explainerLastMessage = state["explainerMessages"][-1]
    
    tools = explainerTools
    tool_registry = {tool.name: tool for tool in tools}
    
    tool_messages = []
    
    # Execute each tool the agent requested
    for tool_call in explainerLastMessage.tool_calls:
        tool = tool_registry[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        
        # Send the result back to the agent
        tool_messages.append(ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        ))
    
    return {
        "explainerMessages": tool_messages,
        "explainerToolMessages": tool_messages,
        "conversationMessages": tool_messages
    }






def quizGeneratorNode(state: State):
    quizGeneratorMessages = state["quizGeneratorMessages"]
    conversationMessages = state["conversationMessages"]
    input = state["input"]
    
    if not quizGeneratorMessages:
        quizGeneratorMessages = [HumanMessage(content=str(input))]
        
    messages = [SystemMessage(content=str(quizGeneratorPrompt)), *conversationMessages]
    
    #check for error
    response = llm.invoke(messages)
    
    return {
        "output": response.content,
        "quizGeneratorMessages":[*quizGeneratorMessages, AIMessage(content=str(response.content))],
        "conversationMessages": [AIMessage(content=str(response.content))]
    }
    
    
    
    
    
def summarizerNode(state: State):
    summarizerMessages = state["summarizerMessages"]
    conversationMessages = state["conversationMessages"]
    input = state["input"]
    
    if not summarizerMessages:
        summarizerMessages = [HumanMessage(content=str(input))]
        
    messages = [SystemMessage(content=str(summarizerPrompt)), *conversationMessages]
    
    #check for error
    response = llm.invoke(messages)
    
    return {
        "output": response.content,
        "summarizerMessages":[*summarizerMessages, AIMessage(content=str(response.content))],
        "conversationMessages": [AIMessage(content=str(response.content))]
    }
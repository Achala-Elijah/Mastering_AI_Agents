from langgraph.graph import StateGraph, END
from workflow.state import State
from workflow.constants import *
from workflow.nodes import *


def plannerEdge(state:State):
    nextRoute = state["nextRoute"]
    return nextRoute[-1]




def explainerEdge(state:State):
    lastExplainerMessage = state["explainerMessages"][-1]
    
    if lastExplainerMessage.tool_calls:
        return "explainerTools"
    
    return "end"




def createWorkflow():
    workflow = StateGraph(State)
    
    #define nodes
    workflow.add_node(PLANNER_NODE, plannerNode)
    workflow.add_node(EXPLAINER_NODE, explainerNode)
    workflow.add_node(QUIZ_GENERATOR_NODE, quizGeneratorNode)
    workflow.add_node(SUMMARIZER_NODE, summarizerNode)
    workflow.add_node(PLANNER_TOOLS_NODE, plannerToolsNode)
    workflow.add_node(EXPLAINER_TOOLS_NODE, explainerToolsNode)
    
    #Define entry point
    workflow.set_entry_point(PLANNER_NODE)
    
    #Define edges
    workflow.add_edge(PLANNER_TOOLS_NODE, PLANNER_NODE)
    workflow.add_edge(EXPLAINER_TOOLS_NODE, EXPLAINER_NODE)
    workflow.add_edge(QUIZ_GENERATOR_NODE, END)
    workflow.add_edge(SUMMARIZER_NODE, END)
    
    workflow.add_conditional_edges(
        PLANNER_NODE,
        plannerEdge,
        {
            "explainer": EXPLAINER_NODE,
            "quizGenerator": QUIZ_GENERATOR_NODE,
            "summarizer": SUMMARIZER_NODE,
            "tools": PLANNER_TOOLS_NODE
        }
    )
    
    workflow.add_conditional_edges(
        EXPLAINER_NODE,
        explainerEdge,
        {
            "explainerTools": EXPLAINER_TOOLS_NODE,
            "end": END
        }
    )
    
    return workflow.compile()
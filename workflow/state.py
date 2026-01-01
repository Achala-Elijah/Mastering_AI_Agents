from typing_extensions import TypedDict, List, Dict
from typing import Annotated, Optional, Any, Literal
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, AnyMessage   
from operator import add
from pydantic import BaseModel, Field, conlist, field_validator



class State(TypedDict):
    transcribedText: str
    isTranscribed: bool
    input: str
    output: str
    nextRoute: Annotated[List[str], add]
    
    
    plannerMessages: Annotated[List[AnyMessage], add]
    explainerMessages: Annotated[List[AnyMessage], add]
    quizGeneratorMessages: Annotated[List[AnyMessage], add]
    summarizerMessages: Annotated[List[AnyMessage], add]
    plannerToolMessages: Annotated[List[AnyMessage], add]
    explainerToolMessages: Annotated[List[AnyMessage], add]
    
    conversationMessages: Annotated[List[AnyMessage], add]
    
    
    
    
    
class ToolCall(BaseModel):
    id: str
    name: str
    args: Dict[str, Any]
    
    
class ManagerOuputFormat(BaseModel):
    nextRoute: List[Literal["tools", "explainer", "quizGenerator", "summarizer"]] = Field(
        ..., description="A list containing exactly one next route."
    )
    
    tool_calls: Optional[List[ToolCall]] = Field(default_factory=list)
    
    @field_validator("nextRoute", mode="after")
    def must_have_one_item(cls, v):
        if len(v) != 1:
            raise ValueError("nextRoute must contain exactly one item")
        return v
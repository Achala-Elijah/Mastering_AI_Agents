import os
import assemblyai as aai
import yt_dlp
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import inspect



def downloadVideo(video_url: str) -> str:
    """
    Download a video or audio file given it URL.

    Args: 
        video_url (string): A link to the video or audio.

    Returns:
        String: Returns the path to the downloaded video on local machine if the download was successful; otherwise, an empty string("").

    Example:
       >>> downloadVideo("https://youtu.be/j2SQPQBINh4?si=2sGxa0jgoVmf3VUX")
       "The dowloaded video or audio (https://youtu.be/j2SQPQBINh4?si=2sGxa0jgoVmf3VUX) is in the directory ./downloads/video.mp4"
    """

    path = './downloads/video.%(ext)s'
    ydl_opts = {
        'outtmpl': path,  # Save as video.mp4 or .webm
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
        except Exception as e:
            return ""

    return f"The downloaded video or audio({video_url}) is in the directory {path}"
    
    
    
    


def transcribe(file_path: str) -> str:
    """
    Transcribe a video or audio file from a local path.

    Args:
        file_path(str): Path to the audio or video file on local machine.

    Returns:
        str: The transcribed text if successful; otherwise, empty str.

    Example:
        >>> transcribe("./downloads/video.mp4")
        "This is the transcribed text of the video."
    """

    aai.settings.api_key = os.getenv("ASSEMBLY_AI_KEY")
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.universal)
    transcript = aai.Transcriber(config=config).transcribe(file_path)

    if transcript.status == "error":
        return ""
    
    result = f"The transcribed audio or video ({file_path}) is: \n {transcript.text}"

    
    return result




def generate_tool_metadata(func):
    sig = inspect.signature(func)
    args_schema = {k: (v.annotation.__name__ if v.annotation != inspect._empty else "Any")
                   for k, v in sig.parameters.items()}

    metadata = {
        "id": func.__name__ + "_tool",
        "name": func.__name__,
        "description": func.__doc__.strip() if func.__doc__ else "",
        "args_schema": args_schema
    }
    return metadata






def build_tools_prompt(tools_metadata: list) -> str:
    lines = ["You have access to the following tools you can call:"]
    for t in tools_metadata:
        args_str = ", ".join(f"{k}: {v}" for k, v in t["args_schema"].items())
        lines.append(f"- {t['name']}({args_str}): {t['description']}")
        lines.append("\n")
    lines.append(
        "When you want to use a tool, return JSON in this format:\n"
        '{ "nextRoute": ["tools"], "tool_calls": [ { "name": "tool_name", "arguments": {...} } ] }'
    )

    return "\n".join(lines)






def toolsPrompt(tools: list) -> str:
    tools_metadata = [generate_tool_metadata(fn) for fn in tools]
    tools_prompt = build_tools_prompt(tools_metadata)
    
    return tools_prompt




tools = [transcribe, downloadVideo]
explainerTools = [
    TavilySearchResults(max_results=1, search_depth="advanced", tavily_api_key=os.getenv("TAVILY_API_KEY"))
]
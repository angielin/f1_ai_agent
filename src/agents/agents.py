import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from .agent_outputs import AgentResponse
from .tools.tools import tools
from .tracing.logger import setup_logging

load_dotenv()

logger = setup_logging(__name__)

SYSTEM_PROMPT = (
    "You are an F1 (Formula 1) assistant. Answer questions about drivers, "
    "teams, races, and stats. Use your tools to look up current or specific "
    "information rather than guessing, and say when you're not sure.\n\n"
    "Search sparingly: try at most two tool calls total for a question. If "
    "the first search doesn't return a clear answer, do not keep retrying "
    "with slightly reworded queries - answer with the best information you "
    "found and say what's uncertain, rather than searching again."
)

# Caps the number of agent/tool round-trips per question (LangGraph
# recursion_limit counts each node step, so this allows a handful of
# search-then-respond cycles before forcing a stop). Keeps runs fast and
# protects a tight API quota from runaway search-refinement loops.
MAX_AGENT_STEPS = 8


def build_agent_graph(model: str = "gemini-3.5-flash-lite"):
    '''
    Wires the Gemini LLM together with the tools from tools.py into a
    tool-calling agent graph (LangChain's current `create_agent` API - the
    older AgentExecutor/create_tool_calling_agent path was removed in
    langchain 1.x). Raises early if GOOGLE_API_KEY isn't set, rather than
    failing on the first question.
    '''
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Add it to a .env file at the repo "
            "root (see .env.example)."
        )

    llm = ChatGoogleGenerativeAI(model=model, temperature=0)
    return create_agent(llm, tools=tools, system_prompt=SYSTEM_PROMPT)


class F1Agent:
    '''
    Conversational wrapper around the agent graph. Keeps the full message
    history (including tool calls/results) in memory for the lifetime of
    the instance so follow-up questions ("what about his teammate?") have
    context.
    '''

    def __init__(self, model: str = "gemini-3.5-flash-lite"):
        self.graph = build_agent_graph(model)
        self.messages: list[BaseMessage] = []

    def ask(self, question: str) -> AgentResponse:
        logger.debug("User asked: %s", question)

        self.messages.append(HumanMessage(content=question))
        result = self.graph.invoke(
            {"messages": self.messages},
            config={"recursion_limit": MAX_AGENT_STEPS},
        )
        self.messages = result["messages"]

        answer = self.messages[-1].text
        tools_used = [
            m.name for m in self.messages if isinstance(m, ToolMessage)
        ]

        logger.debug("Agent answered: %s", answer)
        return AgentResponse(answer=answer, tools_used=tools_used)

'''
Use langchain to integrate with Google Search and Gemini
'''

from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

search_tool = DuckDuckGoSearchRun(
    name="web_search",
    description=(
        "Search the web for current F1 information: race results, standings, "
        "schedules, and news. Use this for anything recent or time-sensitive."
    ),
)

wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000),
    description=(
        "Look up background information on F1 drivers, teams, and history "
        "from Wikipedia. Use this for biographical or historical facts."
    ),
)

tools = [search_tool, wikipedia_tool]

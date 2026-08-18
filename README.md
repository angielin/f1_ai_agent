### Description

F1 AI Agent for driver information and stats using LangChain and Gemini. Talk
to it from the terminal and it'll look things up on the web and Wikipedia to
answer.

## Prerequisites

    - Python 3.11 (a newer Homebrew-installed Python is recommended - macOS's
      system Python is built against LibreSSL and fails to connect to the
      Gemini API)
    - Pipenv
    - A Gemini API key (free at https://aistudio.google.com/app/apikey)

## Getting started

    1. Clone the repository
    2. pip install pipenv
    3. pipenv install
    4. cp .env.example .env, then edit .env and paste in your real
       GOOGLE_API_KEY
    5. pipenv shell

## Running the agent

    pipenv run python cli.py

This starts an interactive chat in your terminal - ask about drivers, teams,
races, and stats, and type `exit` or `quit` to leave. Conversation history is
kept for the session, so follow-up questions work.

## Project layout

    - cli.py                        - interactive entry point
    - src/agents/agents.py          - agent wiring (Gemini + tools)
    - src/agents/agent_outputs.py   - structured response schema
    - src/agents/tools/tools.py     - DuckDuckGo search + Wikipedia tools
    - src/agents/tracing/           - logging setup (writes to
                                       src/agents/tracing/output.log)

## Notes

    - Free-tier Gemini keys have a daily request quota. If you hit a 429/
      "RESOURCE_EXHAUSTED" error, wait a bit or check your limits at
      https://ai.dev/rate-limit.
    - Never commit .env (it holds your real API key) - only .env.example
      should be tracked, with a placeholder value.

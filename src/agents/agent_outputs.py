from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    '''
    Shape of a single answer from the F1 agent. Kept lightweight for now -
    just the final answer plus which tools it leaned on, so the CLI (or any
    future caller) doesn't have to parse raw agent output.
    '''

    answer: str = Field(description="The agent's answer to the user's question")
    tools_used: list[str] = Field(
        default_factory=list,
        description="Names of tools invoked while producing the answer",
    )

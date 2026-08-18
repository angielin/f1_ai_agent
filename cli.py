from src.agents.agents import F1Agent


def main() -> None:
    print("F1 AI Agent — ask me about drivers, teams, races, and stats.")
    print("Type 'exit' or 'quit' to leave.\n")

    try:
        agent = F1Agent()
    except RuntimeError as e:
        print(f"[setup error] {e}")
        return

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            response = agent.ask(question)
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print(
                    "[error] Gemini API quota exceeded for now. Free-tier "
                    "keys are capped at a small number of requests per day "
                    "- wait a bit and try again, or check your limits at "
                    "https://ai.dev/rate-limit\n"
                )
            else:
                print(f"[error] {e}\n")
            continue

        print(f"Agent: {response.answer}\n")


if __name__ == "__main__":
    main()

# Chat interface logic
# src/chat.py

from rag import ask_question


def start_chat():

    print("\n==============================")
    print("Mini Manuscript RAG Chat")
    print("==============================")

    print("\nType 'exit' to quit.\n")

    while True:

        query = input("Ask Question: ")

        if query.lower() == "exit":
            print("\nGoodbye!\n")
            break

        answer, sources, tokens = ask_question(query)

        print("\nAnswer:\n")

        print(answer)

        print("\nSources:")

        unique_sources = sorted(set(sources))

        for source in unique_sources:
            print(f"- {source}")

        print(f"\n[Tokens Used: {tokens}]")

        print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":

    start_chat()
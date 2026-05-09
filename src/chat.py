# Chat interface logic
# src/chat.py

from rag import ask_question


def start_chat():

    print("\n==============================")
    print("Mini Manuscript RAG Chat")
    print("==============================")

    print("\nType 'exit' to quit.\n")

    while True:

        query = input("Ask: > ")

        if query.lower() == "exit":
            print("\nGoodbye!\n")
            break

        answer, sources, tokens = ask_question(query)

        print(f"Answer: {answer}")

        # Format sources as [page_x]
        formatted_sources = []
        for s in sources:
            # Extract page number if present, otherwise use the source string
            import re
            match = re.search(r'Page (\d+)', s)
            if match:
                formatted_sources.append(f"[page_{match.group(1)}]")
            else:
                formatted_sources.append(f"[{s}]")

        print(f"Sources: {', '.join(sorted(set(formatted_sources)))}")
        print(f"Tokens Used: {tokens}")
        print("-" * 20)


if __name__ == "__main__":

    start_chat()
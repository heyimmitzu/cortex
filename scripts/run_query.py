"""Entry point: ask a question against the knowledgebase (retrieve -> rerank -> answer)."""

import argparse

from cortex.query.answer import generate_answer
from cortex.query.rerank import rerank
from cortex.query.retrieve import retrieve


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="Question to ask the knowledgebase")
    args = parser.parse_args()

    candidates = retrieve(args.question)
    top_chunks = rerank(args.question, candidates)
    answer = generate_answer(args.question, top_chunks)
    print(answer)


if __name__ == "__main__":
    main()

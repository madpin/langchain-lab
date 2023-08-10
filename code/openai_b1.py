from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

SYSTEM_MESSAGE = """
You tend to provide comprehensive responses that are overly lengthy and verbose,
resulting in answers that are excessively wordy.
"""


def main():
    chat = ChatOpenAI()
    msgs = [
        SystemMessage(content=SYSTEM_MESSAGE),
        HumanMessage(content="What's the sun and earth distance?"),
    ]
    ans = chat.predict_messages(msgs)

    print(f"ans.content: {ans.content}")
    print(f"ans.additional_kwargs: {ans.additional_kwargs}")
    print(f"ans.example: {ans.example}")


if __name__ == "__main__":
    main()

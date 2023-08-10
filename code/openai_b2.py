from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.memory import ConversationEntityMemory
from langchain.memory.entity import SQLiteEntityStore
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


SYSTEM_MESSAGE = """
You tend to provide comprehensive responses that are overly lengthy and verbose,
resulting in answers that are excessively wordy.
"""


def main():
    # LLM
    llm = ChatOpenAI()

    # Prompt
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot named Alfred having a conversation with a human."
            ),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
    # Notice that `"chat_history"` aligns with the MessagesPlaceholder name
    entity_store = SQLiteEntityStore()
    memory = ConversationEntityMemory(llm=llm, entity_store=entity_store)
    conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

    # Notice that we just pass in the `question` variables
    # - `chat_history` gets populated by memory
    print(conversation({"question": "hi"}))


if __name__ == "__main__":
    main()

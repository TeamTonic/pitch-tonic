from typing import List, Sequence, Any
import pickle

import pytest
from pydantic.fields import PrivateAttr

from llama_index.core.base.llms.types import ChatResponse
from llama_index.core.llms import ChatMessage, MessageRole, MockLLM
from src.chat_summary_memory_buffer import (
    ChatSummaryMemoryBuffer,
)
from llama_index.core.utils import get_tokenizer

tokenizer = get_tokenizer()


def _get_role_alternating_order(i: int):
    if i % 2 == 0:
        return MessageRole.USER
    return MessageRole.ASSISTANT


USER_CHAT_MESSAGE = ChatMessage(role=MessageRole.USER, content="first message")
USER_CHAT_MESSAGE_TOKENS = len(tokenizer(str(USER_CHAT_MESSAGE.content)))
LONG_USER_CHAT_MESSAGE = ChatMessage(
    role=MessageRole.USER,
    content="".join(
        ["This is a message that is longer than the proposed token length"] * 10
    ),
)
LONG_RUNNING_CONVERSATION = [
    ChatMessage(role=_get_role_alternating_order(i), content=f"Message {i}")
    for i in range(5)
]
LONG_USER_CHAT_MESSAGE_TOKENS = len(tokenizer(str(LONG_USER_CHAT_MESSAGE.content)))


class MockSummarizerLLM(MockLLM):
    _i: int = PrivateAttr()
    _responses: List[ChatMessage] = PrivateAttr()
    _max_tokens: int = PrivateAttr()

    def __init__(self, responses: List[ChatMessage], max_tokens: int = 512) -> None:
        self._i = 0  # call counter, determines which response to return
        self._responses = responses  # list of responses to return
        self._max_tokens = max_tokens  # Max tokens for summary

        super().__init__()

    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        del messages  # unused

        # For this mockLLM, we assume tokens are separated by spaces
        max_tokens = self._max_tokens
        if self._max_tokens > len(self._responses[self._i].content):
            max_tokens = len(self._responses[self._i].content)
        response_tokens = " ".join(
            self._responses[self._i].content.split(" ")[0:max_tokens]
        )

        response = ChatResponse(
            message=ChatMessage(role=MessageRole.ASSISTANT, content=response_tokens),
        )
        self._i += 1
        return response

    def set_max_tokens(self, max_tokens):
        self._max_tokens = max_tokens


FIRST_SUMMARY_RESPONSE = "First, the user asked what an LLM was, and the assistant explained the basic ideas."
SECOND_SUMMARY_RESPONSE = (
    "The conversation started about LLMs. It then continued about LlamaIndex."
)


@pytest.fixture()
def summarizer_llm():
    return MockSummarizerLLM(
        responses=[
            ChatMessage(
                content=FIRST_SUMMARY_RESPONSE,
                role=MessageRole.ASSISTANT,
            ),
            ChatMessage(
                content=SECOND_SUMMARY_RESPONSE,
                role=MessageRole.ASSISTANT,
            ),
        ]
    )


def test_put_get(summarizer_llm) -> None:
    # Given one message with fewer tokens than token_limit_full_text
    memory = ChatSummaryMemoryBuffer.from_defaults(
        chat_history=[USER_CHAT_MESSAGE], summarizer_llm=summarizer_llm
    )

    # When I get the chat history from the memory
    history = memory.get()

    # Then the history should contain the full message
    assert len(history) == 1
    assert history[0].content == USER_CHAT_MESSAGE.content


def test_put_get_summarize_long_message(summarizer_llm) -> None:
    # Given one message with more tokens than token_limit_full_text
    memory = ChatSummaryMemoryBuffer.from_defaults(
        chat_history=[LONG_USER_CHAT_MESSAGE],
        token_limit_full_text=2,
        summarizer_llm=summarizer_llm,
    )

    # When I get the chat history from the memory
    history = memory.get()

    # Then the history should contain the summarized message
    assert len(history) == 1
    assert history[0].content == FIRST_SUMMARY_RESPONSE


def test_put_get_summarize_part_of_conversation(summarizer_llm) -> None:
    # Given a chat history where only 2 responses fit in the token_limit_full_text
    tokens_most_recent_messages = sum(
        [
            len(tokenizer(str(LONG_RUNNING_CONVERSATION[-i].content)))
            for i in range(1, 3)
        ]
    )
    memory = ChatSummaryMemoryBuffer.from_defaults(
        chat_history=LONG_RUNNING_CONVERSATION.copy(),
        token_limit_full_text=tokens_most_recent_messages,
        summarizer_llm=summarizer_llm,
    )

    # When I get the chat history from the memory
    history = memory.get()

    # Then the history should contain the full message for the latest two and
    # a summary for the older messages
    assert len(history) == 3
    assert history[0].content == FIRST_SUMMARY_RESPONSE
    assert history[0].role == MessageRole.SYSTEM
    assert history[1].content == "Message 3"
    assert history[2].content == "Message 4"

    # When I add a new message to the history
    memory.put(ChatMessage(role=MessageRole.USER, content="Message 5"))

    # Then the history should re-summarize
    history = memory.get()
    assert len(history) == 3
    assert history[0].content == SECOND_SUMMARY_RESPONSE
    assert history[0].role == MessageRole.SYSTEM
    assert history[1].content == "Message 4"
    assert history[2].content == "Message 5"


def test_get_when_initial_tokens_less_than_limit_returns_history() -> None:
    # Given some initial tokens much smaller than token_limit and message tokens
    initial_tokens = 5

    # Given a user message
    memory = ChatSummaryMemoryBuffer.from_defaults(
        token_limit_full_text=1000, chat_history=[USER_CHAT_MESSAGE]
    )

    # When I get the chat history from the memory
    history = memory.get(initial_tokens)

    # Then the history should contain the message
    assert len(history) == 1
    assert history[0] == USER_CHAT_MESSAGE


def test_get_when_initial_tokens_exceed_limit_raises_value_error() -> None:
    # Given some initial tokens exceeding token_limit
    initial_tokens = 50
    memory = ChatSummaryMemoryBuffer.from_defaults(
        chat_history=[USER_CHAT_MESSAGE],
        token_limit_full_text=initial_tokens - 1,
        count_initial_tokens=True,
    )

    # When I get the chat history from the memory
    with pytest.raises(ValueError) as error:
        memory.get(initial_tokens)

    # Then a value error should be raised
    assert str(error.value) == "Initial token count exceeds token limit"


def test_set() -> None:
    memory = ChatSummaryMemoryBuffer.from_defaults(chat_history=[USER_CHAT_MESSAGE])

    memory.put(USER_CHAT_MESSAGE)

    assert len(memory.get()) == 2

    memory.set([USER_CHAT_MESSAGE])
    assert len(memory.get()) == 1


def test_max_tokens_without_summarizer() -> None:
    memory = ChatSummaryMemoryBuffer.from_defaults(
        chat_history=[USER_CHAT_MESSAGE], token_limit_full_text=5
    )

    memory.put(USER_CHAT_MESSAGE)
    assert len(memory.get()) == 2

    # do we limit properly
    memory.put(USER_CHAT_MESSAGE)
    memory.put(USER_CHAT_MESSAGE)
    assert len(memory.get()) == 2

    # In ChatSummaryMemoryBuffer, we overwrite the actual chat history
    assert len(memory.get_all()) == 2

    # does get return in the correct order?
    memory.put(ChatMessage(role=MessageRole.USER, content="test message2"))
    assert memory.get()[-1].content == "test message2"
    assert len(memory.get()) == 2


def test_max_tokens_with_summarizer(summarizer_llm) -> None:
    max_tokens = 1
    summarizer_llm.set_max_tokens(max_tokens)
    memory = ChatSummaryMemoryBuffer.from_defaults(
        summarizer_llm=summarizer_llm,
        chat_history=[USER_CHAT_MESSAGE],
        token_limit_full_text=5,
    )

    # do we limit properly
    memory.put(USER_CHAT_MESSAGE)
    memory.put(USER_CHAT_MESSAGE)
    memory_results = memory.get()
    assert len(memory_results) == 3
    # Oldest message is summarized
    assert memory_results[0].content == " ".join(
        FIRST_SUMMARY_RESPONSE.split(" ")[0:max_tokens]
    )
    assert memory_results[0].role == MessageRole.SYSTEM

    # In ChatSummaryMemoryBuffer, we overwrite the actual chat history
    assert len(memory.get_all()) == 3

    # does get return in the correct order?
    memory.put(ChatMessage(role=MessageRole.USER, content="test message2"))
    memory_results = memory.get()
    assert memory_results[-1].content == "test message2"
    assert len(memory_results) == 3
    # Oldest message is summarized based on the latest information
    assert memory_results[0].content == " ".join(
        SECOND_SUMMARY_RESPONSE.split(" ")[0:max_tokens]
    )


def test_sting_save_load() -> None:
    memory = ChatSummaryMemoryBuffer.from_defaults(
        chat_history=[USER_CHAT_MESSAGE], token_limit_full_text=5
    )

    json_str = memory.to_string()

    with pytest.raises(NotImplementedError):
        ChatSummaryMemoryBuffer.from_string(json_str)


def test_dict_save_load() -> None:
    memory = ChatSummaryMemoryBuffer.from_defaults(
        chat_history=[USER_CHAT_MESSAGE], token_limit_full_text=5
    )

    json_dict = memory.to_dict()

    with pytest.raises(NotImplementedError):
        ChatSummaryMemoryBuffer.from_dict(json_dict)


def test_pickle() -> None:
    """Unpickleable tiktoken tokenizer should be circumvented when pickling."""
    memory = ChatSummaryMemoryBuffer.from_defaults()
    bytes_ = pickle.dumps(memory)
    assert isinstance(pickle.loads(bytes_), ChatSummaryMemoryBuffer)
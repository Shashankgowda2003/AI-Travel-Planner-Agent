import pytest
from langchain_classic.memory import ConversationBufferMemory


class TestConversationMemory:
    def test_memory_stores_messages(self):
        memory = ConversationBufferMemory()
        memory.chat_memory.add_user_message("Plan a trip to Goa")
        memory.chat_memory.add_ai_message("Here is your Goa trip plan...")
        assert len(memory.chat_memory.messages) == 2

    def test_memory_chat_history_format(self):
        memory = ConversationBufferMemory()
        memory.chat_memory.add_user_message("Plan a 3-day trip to Jaipur")
        memory.chat_memory.add_ai_message("Day 1: Amer Fort, City Palace...")
        messages = memory.chat_memory.messages
        assert messages[0].type == "human"
        assert messages[1].type == "ai"
        assert "Jaipur" in messages[0].content
        assert "Amer Fort" in messages[1].content

    def test_memory_passed_to_plan_function(self):
        memory = ConversationBufferMemory()
        memory.chat_memory.add_user_message("Cheaper hotels please")
        memory.chat_memory.add_ai_message("Updated with budget stays.")
        messages = memory.chat_memory.messages[-6:]
        assert len(messages) == 2
        assert messages[0].type == "human"

    def test_memory_last_6_messages_capped(self):
        memory = ConversationBufferMemory()
        for i in range(10):
            memory.chat_memory.add_user_message(f"Refine trip {i}")
            memory.chat_memory.add_ai_message(f"Refined plan {i}")
        last_messages = memory.chat_memory.messages[-6:]
        assert len(last_messages) == 6
        assert last_messages[-1].content == "Refined plan 9"

    def test_empty_memory_returns_empty_chat_history(self):
        memory = ConversationBufferMemory()
        if memory.chat_memory and memory.chat_memory.messages:
            chat_context = "\n".join(
                [f"{'User' if m.type == 'human' else 'Assistant'}: {m.content}"
                 for m in memory.chat_memory.messages[-6:]]
            )
        else:
            chat_context = ""
        assert chat_context == ""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class PromptFactory:
    """
        Prompt Factory Static class.

        @Methods:
            create(system_prompt: str) -> ChatPromptTemplate
    """
    @staticmethod
    def create(system_prompt: str, conversation_history: bool = False) -> ChatPromptTemplate:
        
        """
        Create a prompt from Langchain Prompt templates and returns back this PromptTemplate.

        Arguments:
            system_prompt (str): the current system instructions.
        """
        history_placeholder = MessagesPlaceholder(variable_name="history") if conversation_history else ("system", "")

        created_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt
                ),
                history_placeholder,
                MessagesPlaceholder("messages"),
                
            ]
        )

        return created_prompt
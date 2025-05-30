import cohere
from groq import Groq

from campus_security_api.config import EnvironmentVariables


class LLMService:
    _co = cohere.ClientV2(EnvironmentVariables.COHERE_API_KEY)
    _groq = Groq(api_key=EnvironmentVariables.GROQ_API_KEY)

    @classmethod
    def chat_with_ai(cls, system_prompt_content: str, system_info_content, chat_msg_queryset):

        system_prompt = {
            "role": "system",
            "content": system_prompt_content
        }

        system_info = {
            "role": "user",
            "name": "system_info",
            "content": system_info_content
        }

        messages = []

        for comment in chat_msg_queryset:
            messages.append({
                "role": "assistant" if comment.comment_by.id == 'system-ai' else "user",  # "user" or "assistant"
                "name": f"{comment.comment_by.username}",
                "content": f"[{comment.date_created}] {comment.comment}"
            })

        ai_prompt_messages = [system_prompt, system_info] + messages

        return cls._chat_with_groq(ai_prompt_messages)

    @classmethod
    def _chat_with_cohere(cls, messages: list[dict[str, str]]):

        response = cls._co.chat(
            model="command-r-plus",
            messages=messages
        )

        return response.message.content[0].text

    @classmethod
    def _chat_with_groq(cls, messages: list[dict[str, str]]):


        completion = cls._groq.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.1
            # response_format={"type": "json_object"}
        )

        return completion.choices[0].message.content

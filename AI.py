from gigachat import GigaChatAsyncClient
from gigachat.models import Chat, Messages, MessagesRole
from copy import deepcopy
from keys import key_api_ai


class AIHelper:
    def __init__(self,):
        self.client = GigaChatAsyncClient(credentials=key_api_ai, verify_ssl_certs=False)
        self.messages = Chat(
            messages=[
                Messages(role=MessagesRole.SYSTEM,
                         content=f"Тебе будут отправляться города и страны,"
                                 f"а ты должен отправлять список из 5 достопримечательностей с какм-нибудь"
                                 f"интересным фактом"
                                 f"Если сообщение не относится к этому, "
                                 f"то скажи, что не разговариваешь на другие темы.")
            ],
            temperature=0.7,
            max_tokens=100)

    async def get_text_message(self, request: str):
        chat2 = deepcopy(self.messages)
        chat2.messages.append(Messages(role=MessagesRole.USER, content=request))
        response = await self.client.achat(chat2)
        answer = response.choices[0].message.content
        return answer

    def __del__(self):
        self.client.aclose()
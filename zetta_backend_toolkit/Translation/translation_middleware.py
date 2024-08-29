from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from googletrans import Translator

class TranslationMiddleware(Middleware):
    def __init__(self, app: FastAPI, target_language: str = "en"):
        super().__init__(app)
        self.translator = Translator()
        self.target_language = target_language

    async def dispatch(self, request: Request, call_next):
        language = request.headers.get("Accept-Language", "en")
        if language != self.target_language:
            body = await request.body()
            if body:
                translated_text = self.translator.translate(body.decode("utf-8"), src=language, dest=self.target_language).text
                request._body = translated_text.encode("utf-8")
        response = await call_next(request)
        translated_response = response
        if response.body:
            translated_response_body = self.translator.translate(response.body.decode("utf-8"), src=self.target_language, dest=language).text
            translated_response.body = translated_response_body.encode("utf-8")
        return translated_response
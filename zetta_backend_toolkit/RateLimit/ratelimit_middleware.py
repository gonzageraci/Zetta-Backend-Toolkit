import logging
import time
import json
from typing import Callable
from fastapi import FastAPI, HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.DEBUG,  # Establecer el nivel de logging a DEBUG
                    format='%(levelname)s - %(asctime)s - %(message)s', # Formato del mensaje
                    handlers=[logging.StreamHandler()])  # Enviar los logs a la consola


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI, max_requests:int = 100, period:int = 60):
        super().__init__(app)
        self.max_requests = max_requests # Número máximo de peticiones permitidas
        self.period = period # Periodo de tiempo en segundos
        if not self.logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
        
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]):
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if current_time - timestamp < self.period]

        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests")

        self.requests[client_ip].append(current_time)
        response = await call_next(request)
        return response
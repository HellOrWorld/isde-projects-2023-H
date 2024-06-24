from typing import List
from fastapi import Request


class HistogramForm:
    def __init__(self, request: Request):
        self.request = request
        self.image_id: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.image_id = form.get("image_id")
from typing import List
from fastapi import Request

#Here is the declaration of the HistogramForm class. This class is quite similar to the ClassificationForm class,
# but it has only one field, image_id, and no model_id field because an image histogram is not dependent on any machine
# learning model.

class HistogramForm:
    def __init__(self, request: Request):
        self.request = request
        self.image_id: str = ""
        self.errors: List = []

    async def load_data(self):
        form = await self.request.form()
        self.image_id = form.get("image_id")

    def is_valid(self):
        if not self.image_id or not isinstance(self.image_id, str):
            self.errors.append("A valid image id is required")
        if not self.errors:
            return True
        return False

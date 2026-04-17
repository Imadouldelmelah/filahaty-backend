from pydantic import BaseModel

class AgronomyRequest(BaseModel):
    crop: str

class AgronomyResponse(BaseModel):
    # This can be expanded to be more specific, but for now we'll allow dynamic dictionary response
    # matching the engine's output.
    pass

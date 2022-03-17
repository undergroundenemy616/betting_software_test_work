from utils import CustomBaseModel


class BaseModel(CustomBaseModel):
    encoded_key: str
    body: dict
    duplicates_count: int = 0


class EncodedKeyResponseModel(CustomBaseModel):
    encoded_key: str


class DuplicatesResponseModel(CustomBaseModel):
    duplicates_percentage: int

from .schemas import HTTPError,HTTPSuccess
RESPONSE_404 = {
    "model": HTTPError,
    "description": "Data Not Found",
}
RESPONSE_OK={
    "model": HTTPSuccess,
    "description": "Successful Response",
}
from http import HTTPStatus

from starlette.responses import JSONResponse

NOT_FOUND_RESPONSE = JSONResponse(
    content={'type': 'error', 'message': 'object doesn\'t exist'},
    status_code=HTTPStatus.NOT_FOUND,
)

NO_CONTENT_RESPONSE = JSONResponse(
    content={'type': 'success', 'message': 'object deleted'},
    status_code=HTTPStatus.NO_CONTENT,
)

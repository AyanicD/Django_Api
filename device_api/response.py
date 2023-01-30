from rest_framework import response
import json


class Response(response.Response):
    """The various HTTP responses for use in returning proper HTTP codes."""

    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        super().__init__(data, status, template_name, headers, exception, content_type)


class Ok(Response):
    """200 OK
    Should be used to indicate nonspecific success. Must not be used to
    communicate errors in the response body.
    In most cases, 200 is the code the client hopes to see. It indicates that
    the REST API successfully carried out whatever action the client requested,
    and that no more specific code in the 2xx series is appropriate. Unlike
    the 204 status code, a 200 response should include a response body.
    """

    status_code = 200


class Created(Response):
    """201 Created
    Must be used to indicate successful resource creation.
    A REST API responds with the 201 status code whenever a collection creates,
    or a store adds, a new resource at the client's request. There may also be
    times when a new resource is created as a result of some controller action,
    in which case 201 would also be an appropriate response.
    """

    status_code = 201


class NoContent(Response):
    """204 No Content
    The HTTP 204 No Content success status response code indicates that a
    request has succeeded, but that the client doesn't need to navigate away
    from its current page.
    """

    status_code = 204


class BadRequest(Response):
    """400 Bad Request
    May be used to indicate nonspecific failure.
    400 is the generic client-side error status, used when no other 4xx error
    code is appropriate.
    """

    status_code = 400


class Unauthorized(Response):
    """401 Unauthorized
    Must be used when there is a problem with the client credentials.
    A 401 error response indicates that the client tried to operate on a
    protected resource without providing the proper authorization. It may have
    provided the wrong credentials or none at all.
    """

    status_code = 401


class Forbidden(Response):
    """403 Forbidden
    Should be used to forbid access regardless of authorization state.
    A 403 error response indicates that the client's request is formed
    correctly, but the REST API refuses to honor it. A 403 response is not a
    case of insufficient client credentials; that would be 401 ("Unauthorized").
    REST APIs use 403 to enforce application-level permissions. For example, a
    client may be authorized to interact with some, but not all of a REST API's
    resources. If the client attempts a resource interaction that is outside of
    its permitted scope, the REST API should respond with 403.
    """

    status_code = 403


class NotFound(Response):
    """404 Not Found
    Must be used when a client's URI cannot be mapped to a resource.
    The 404 error status code indicates that the REST API can't map the
    client's URI to a resource.
    """

    status_code = 404


class MethodNotAllowed(Response):
    """405 Method Not Allowed
    Must be used when the HTTP method is not supported.
    The API responds with a 405 error to indicate that the client tried to use
    an HTTP method that the resource does not allow. For instance, a read-only
    resource could support only GET and HEAD, while a controller resource might
    allow GET and POST, but not PUT or DELETE.
    A 405 response must include the Allow header, which lists the HTTP methods
    that the resource supports. For example:
        Allow: GET, POST
    """

    status_code = 405


class NotImplemented(Response):
    """501 Not Implemented
    The server either does not recognise the request method, or it lacks the
    ability to fulfill the request.
    """

    status_code = 501


def parse_response(api_response):
    """
    This method parse the third party API response

    Args:
        api_response (object): API response obj

    """
    if api_response.text is None:
        raise Exception(api_response.status_code, {})
    try:
        content = json.loads(api_response.text)
    except ValueError:
        content = {"statusCode": api_response.status_code, "message": api_response.text}
    finally:
        if api_response.status_code not in [200, 201, 204]:
            message = (
                content.get("message")
                if content.get("message")
                else content.get("errors")
            )
            raise Exception(api_response.status_code, message)
        else:
            return content, api_response.status_code

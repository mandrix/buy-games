from django.http import RawPostDataException
from django.http import HttpResponsePermanentRedirect
import django.conf as conf

from ipware import get_client_ip
from product.models import Log


class LoggingMiddleware:
    """
    Middleware used to create a log of the users actions and save it in the database.
    """

    @staticmethod
    def contains_unwanted_path(path: str):
        """
        Checks if an unwanted path is in the path provided as an argument.
        :param path: A path in an url
        :return: A boolean saying if one of the unwanted paths are in the path
        """
        unwanted_paths = [
            "/robots.txt",
            "/sitemap.xml",
            "/favicon.ico",
            "/assets/",
            "/static/",
            "/admin"
            ]

        for unwanted_path in unwanted_paths:
            if path.startswith(unwanted_path):
                return True

        other_unwanted = [".png", ".jpg", ".mp4", ".mp3", "year", "page", "tag"]

        for unwanted in other_unwanted:
            if unwanted in path:
                return True
        return False

    @staticmethod
    def get_status_text(response):
        """
        Used to get the status text of a request if it has it and it can be parsed into json
        :return: Status text of request
        """
        try:
            out = response.status_text
        except AttributeError:
            out = "No status text."
        return out

    @staticmethod
    def create_log(response, request, request_json):
        """
        Creates a new log entry with all the fields needed using the request and the response
        but only if it not a request to the admin page.
        :return: The object created
        """
        _path = request.get_full_path()
        if LoggingMiddleware.contains_unwanted_path(_path):
            return
        _status_code = response.status_code
        _status_text = LoggingMiddleware.get_status_text(response)
        _response = str(response.content.decode())
        _is_secure = request.is_secure()
        _ipv4_address = get_client_ip(request)[0]
        _log = {
            "status_code": _status_code,
            "status_text": _status_text,
            "response": _response,
            "request": request_json,
            "path": _path,
            "is_secure": _is_secure,
            "ipv4_address": _ipv4_address,
        }
        return _log

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request = str(request.POST)
        if not len(request.POST):
            try:
                _request = request.body.decode()
            except (RawPostDataException, UnicodeDecodeError):
                _request = "Data is not JSON encoded"
        response = self.get_response(request)
        # Log creation
        try:
            log = LoggingMiddleware.create_log(response=response, request=request, request_json=_request)
            if log:
                Log.objects.create(**log)
        except Exception as e:
            print(f"Se produjo una excepción: {str(e)}")

        return response


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().partition(":")[0]
        if host in ["www.readygamescr.com", "buy-games.herokuapp.com", "www.buy-games.herokuapp.com"]:
            return HttpResponsePermanentRedirect("https://readygamescr.com" + request.path)
        else:
            return self.get_response(request)

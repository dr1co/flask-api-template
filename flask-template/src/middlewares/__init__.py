"""Request/response hooks that run around every request.

Flask before_request/after_request callbacks and custom decorators (auth
checks, logging, request-id tagging, rate limiting). Register them on the
app or on a blueprint in src/app.py:create_app() or in the blueprint's
__init__.py.
"""

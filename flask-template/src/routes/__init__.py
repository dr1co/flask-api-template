"""Flask blueprints (route definitions).

Each subfolder is a blueprint: it only handles request/response and URL
rules. Delegate business logic to src/controllers, data access to src/db
or src/schemas, and register each blueprint in src/app.py:create_app().
"""

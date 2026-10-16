"""Application package.

src/app.py holds the create_app() factory; everything else is organized
by layer: routes (blueprints), controllers (business logic), db
(engine/session), schemas (data shape), classes (shared domain/utility
code), middlewares (request hooks), plus config.py and extensions.py for
general app configuration.
"""

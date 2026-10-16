"""Data shape: request/response (de)serialization and validation.

Marshmallow/Pydantic-style schemas (or plain dataclasses) describing the
shape of API payloads and, if an ORM is introduced, the table models.
Import from here in routes/controllers to validate input and serialize
output consistently.
"""

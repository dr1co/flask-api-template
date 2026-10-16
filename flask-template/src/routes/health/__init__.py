"""Health-check route.

Exposes GET /health for availability checks (load balancers, container
orchestrators, monitoring). Keep this route free of authentication and
database dependencies so it always reflects whether the process is up.
"""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
  return jsonify(status="ok")

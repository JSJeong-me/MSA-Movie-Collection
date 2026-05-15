import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVICE_DIRS = [
    "api-gateway",
    "auth-service",
    "collection-service",
    "movie-service",
    "notification-service",
    "review-service",
    "search-service",
    "user-service",
]


def load_service_module(service_dir: str, module: str):
    service_paths = [str(ROOT / d) for d in SERVICE_DIRS]

    # Remove existing service roots so only one `app` package root is active.
    sys.path[:] = [p for p in sys.path if p not in service_paths]
    sys.path.insert(0, str(ROOT / service_dir))

    # Drop prior service-local app modules.
    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            del sys.modules[name]

    return importlib.import_module(module)

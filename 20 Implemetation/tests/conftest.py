import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_service_module(service_dir: str, module: str):
    """Load module from one service while isolating shared `app` package name collisions."""
    service_path = str(ROOT / service_dir)
    if service_path not in sys.path:
        sys.path.insert(0, service_path)

    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            del sys.modules[name]

    return importlib.import_module(module)

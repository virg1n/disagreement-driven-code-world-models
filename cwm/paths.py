"""Repository-relative default locations. Override with environment variables."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# directory holding results_main/, results_v2/, results_32b/, results_control/
RESULTS = os.environ.get("CWM_RESULTS", os.path.join(ROOT, "results"))


def res(name):
    return os.path.join(RESULTS, name)

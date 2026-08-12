import sys
from pathlib import Path

from google.colab import drive


PROJECT_ROOT = Path("/content/drive/MyDrive/ForecastOpti")


def initialize_project():
    """Initialize the ForecastOpti Google Colab environment."""

    drive.mount("/content/drive")

    if not PROJECT_ROOT.exists():
        raise FileNotFoundError(
            f"ForecastOpti project root not found: {PROJECT_ROOT}"
        )

    project_root_str = str(PROJECT_ROOT)

    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

    return PROJECT_ROOT

"""Start ohne Konsolenfenster (pythonw). Wird auch vom Windows-Autostart verwendet."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sc_playtime.app import main  # noqa: E402

sys.exit(main())

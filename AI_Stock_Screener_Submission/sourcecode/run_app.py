import os
import sys
from streamlit.web import cli as stcli

if __name__ == "__main__":
    dashboard_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "dashboard.py"
    )

    sys.argv = [
        "streamlit",
        "run",
        dashboard_path,
        "--server.headless=true",
        "--global.developmentMode=false"
    ]

    sys.exit(stcli.main())
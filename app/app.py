"""Module within the `app` package that exposes a created Flask `app` instance.
This helps environments that look specifically for `app/app.py` or `app:app`.
"""

from . import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

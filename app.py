"""Entrypoint shim for platforms that expect a top-level `app` module.
This file exposes a top-level `app` variable (Flask instance) by calling
`create_app()` from the `app` package.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

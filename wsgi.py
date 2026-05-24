import os
from dotenv import load_dotenv

load_dotenv()

import app

application = app.app

if __name__ == "__main__":
    application.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
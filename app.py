import os

# App Initialization
from __init__ import create_app # from __init__ file
app = create_app(os.getenv("CONFIG_MODE")) 

# ----------------------------------------------- #

# Hello World!
@app.route('/')
def hello():
    return "Hello World!"

# Applications Routes
from accounts import urls
from items import urls

@app.route('/health')
def health():
    return {
        "status": "healthy"
    }, 200


# ----------------------------------------------- #

if __name__ == "__main__":
    # To Run the Server in Terminal => flask run -h localhost -p 5000
    # To Run the Server with Automatic Restart When Changes Occurred => FLASK_DEBUG=1 flask run -h localhost -p 5000

    app.run(host="0.0.0.0", port=5000, debug=True)
import os
from server import create_app


app = create_app()

if __name__ == '__main__':
    port = os.getenv('OUR_API_PORT', 14441)
    app.run(debug=True)
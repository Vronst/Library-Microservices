import os
from server import create_app # db


app = create_app()

if __name__ == '__main__':
    port: int = int(os.getenv('UI_PORT', 14440))
    app.run(debug=True, host='0.0.0.0', port=port)
    
import os
import sys
from server import create_app # db


app = create_app()

if __name__ == '__main__':
    if '-p' in sys.argv:
        populate_users_db()
        sys.argv.remove('-p')
    if '-Rp' in sys.argv:
        from server.utils import populate_users_db, reset_database
        reset_database()
        populate_users_db()
        sys.argv.remove('-Rp')
    if '-R' in sys.argv:
        from server.utils import reset_database
        reset_database()
        sys.argv.remove('-R')
   
    port: int = int(os.getenv('UI_PORT', 14440))
    app.run(debug=True, host='0.0.0.0', port=port)
    
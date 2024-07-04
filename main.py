from sales import app
from pathlib import Path
from sales.exts import db

if __name__ == '__main__':
    app.run(debug=True,  use_reloader=False)


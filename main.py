import sys
from app import app

if __name__ == "__main__":
    if "-d" in sys.argv:
        app.run(debug=True)
    else:
        app.run()

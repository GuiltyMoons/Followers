import sys
from followers import app

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        app.run(debug=False)
    else:
        app.run(debug=True)


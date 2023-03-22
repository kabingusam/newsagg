from newsagg import app
from newsagg.models import db
from newsagg.routes import *


print(app)
print(db)


if __name__ == '__main__':
    print("running")
    app.run(port=5000, debug=True)
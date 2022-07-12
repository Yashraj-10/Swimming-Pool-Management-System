from website import create_app,addAdmin
from website.models import User
app=create_app()

if __name__=='__main__':
   app.run(debug=True)
   
    
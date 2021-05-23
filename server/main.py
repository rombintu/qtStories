from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Stories
import socket    
import json
import os

port = 60001                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind(('localhost', port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.
file = os.getcwd() + '/stories.json'

def main():
    print('Server is started...')
    while True:
        conn, addr = s.accept()
        if conn:
            # engine = create_engine('postgresql://test:password@localhost:5432/project13')
            engine = create_engine('sqlite:///db.sqlite')
            Session = sessionmaker(bind=engine)
            session = Session()
            stories = session.query(Stories).all()
            arr_data = []
            with open(file, 'w') as f:
                for st in stories:
                    arr_data.append(
                        {"hero": st.hero, 
                        "story": st.story,
                        "end": st.end})
                f.write(json.dumps({"data": arr_data}, indent=4))

        f = open(file,'rb')
        l = f.read(1024)
        while (l):
            conn.send(l)
            l = f.read(1024)
        f.close()

        print(f'Done sending to {addr}')
        conn.close()
    

if __name__ == "__main__":
    main()
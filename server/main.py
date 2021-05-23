from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Stories
import socket                   # Import socket module
port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind(('localhost', port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

def export_to_json():
    with open('stories', 'w') as f:
        

def main():
    print('Server is started...')
    while True:
        # engine = create_engine('postgresql://test:password@localhost:5432/project13')
        engine = create_engine('sqlite:///db.sqlite')
        Session = sessionmaker(bind=engine)
        session = Session()
        # st = session.query(Stories).all()
        conn, addr = s.accept()
        data='mytext.txt'
        while data:
            conn.send(data.encode())
            print(f'Send data to {addr}')

        print('Done sending')
        session.close()
        conn.close()
    
    

if __name__ == "__main__":
    main()
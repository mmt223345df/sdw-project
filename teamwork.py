## import libraries
from app import create_app


app = create_app()


if __name__ == '__main__':
    # Start the application server with default parameters and enable debug mode.
    app.run(debug=True,host='127.0.0.1', port=5000)
    # app.run(host='0.0.0.0', port=5001)


from src import create_app
from src.config import ProdConfig

app = create_app(ProdConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7507)

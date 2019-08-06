from core import application


if __name__ == '__main__':
    app = application.create_app(__name__)
    app.run()

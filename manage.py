from flask_script import Manager
from app import create_app
from app.commands.commands import createManger

app = create_app()

manager = Manager(app)
manager.add_command("init", createManger)


if __name__ == '__main__':
    manager.run()

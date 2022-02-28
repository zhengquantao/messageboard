from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.commands.commands import createManger
from app.extensions import db

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("init", createManger)
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()

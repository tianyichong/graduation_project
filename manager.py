import os
from app import create_app, db
from app.models import User, Number
from flask import Flask
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 创建程序
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# 初始化
manager = Manager(app)
migrate = Migrate(app, db)


# 为 shell 定义上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Number=Number)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()


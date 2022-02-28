
# 入门指引

1. 安装依赖项:
  ```bash
  pip install -r requirements.txt
  ```


2. 数据库迁移命令
``` bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# 可能用到命令
python manage.py db history
python manage.py db downgrade

```

3. Run
``` bash
python manapy.py runserver

```

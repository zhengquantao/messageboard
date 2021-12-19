from flask_script import Manager

from app.models.models import UserInfo, db

createManger = Manager()


@createManger.option("-u",  dest="username")
@createManger.option("-m",  dest="mobile")
@createManger.option("-e",  dest="email")
def create_user_info(username, mobile, email):
    """创建用户"""
    user = UserInfo(username=username, mobile=mobile, email=email)
    # 添加
    db.session.add(user)
    try:
        # 提交到数据库
        db.session.commit()
        print("用户添加成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        print("用户添加失败")
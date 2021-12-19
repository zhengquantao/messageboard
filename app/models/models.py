from datetime import datetime

from app.extensions import db


class UserInfo(db.Model):

    __tablename__ = "user_info"
    __table_args__ = ({"comment": "用户信息表"},)

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    mobile = db.Column(db.String(11), nullable=False, comment="用户手机")
    username = db.Column(db.String(128), nullable=False, comment="用户名")
    email = db.Column(db.String(50), nullable=False, comment="邮箱")
    # weixin_id = db.Column(db.String(125), index=True, default="", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment="用户密码")
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="最后一次登录时间",)


class MessageBoard(db.Model):
    __tablename__ = "message_board"
    __table_args__ = ({"comment": "留言信息"},)

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    content = db.Column(db.Text, nullable=False, comment="用户留言信息")
    user_id = db.Column(db.BigInteger, db.ForeignKey("user_info.id"), nullable=False, comment="关联用户")
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment="留言时间")
    user = db.relationship("UserInfo", backref=db.backref("message"))


class WxInfo(db.Model):
    __tablename__ = "wx_info"
    __table_args__ = ({"comment": "微信用户信息"})
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    wx_code = db.Column(db.String(128),  nullable=False, comment="微信code")
    user_id = db.Column(db.BigInteger, db.ForeignKey("user_info.id"), nullable=False, comment="用户信息")
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment="创建时间")
    user = db.relationship("UserInfo", backref=db.backref("wx_info"))
from models import usuarios

def get_all_users():
    users = usuarios.query.all()
    return [usuarios.to_dict() for usuarios in users]

def get_user_by_id(id):
    user = usuarios.query.filter_by(id=id).first()
    if user:
        return user.to_dict()
    else:
        return None
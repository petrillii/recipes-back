from models import usuarios

def getAllUsers():
    users = usuarios.query.all()
    return [usuarios.to_dict() for usuarios in users]

def getUserById(id):
    user = usuarios.query.filter_by(id=id).first()
    if user:
        return user.to_dict()
    else:
        return None
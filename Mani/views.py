from app import db,app
from apps.user.models import User

@app.route('/init/')
def create_manager_if_exists():
    """
    This is just for create test manager
    """

    if User.query.filter_by(username='test').first():
        return "Manager Test is exist"
    else:
        u = User()
        u.username = 'test'
        u.set_password('test')
        u.role = 'manager'
        db.session.add(u)
        db.session.commit()

        return "Created Manager test with username and password 'test'"

from authentication.auth_service import AuthService


def register_routes(app, db):
    auth_service = AuthService(db)

    @app.route('/user/register', methods=['POST'])
    def register():
        return auth_service.register()

    @app.route('/user/login', methods=['POST'])
    def login():
        return auth_service.login()

    @app.route('/user/delete', methods=['DELETE'])
    def delete():
        return auth_service.delete_user()

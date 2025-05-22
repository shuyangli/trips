import firebase_admin


def get_firebase_app():
    try:
        firebase_app = firebase_admin.get_app()
    except ValueError:
        firebase_app = firebase_admin.initialize_app()
    return firebase_app

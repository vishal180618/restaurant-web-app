def connect_firebase():
    """
    Use a service account
    """
    import firebase_admin
    from firebase_admin import credentials
    cred = credentials.Certificate('/home/sysadmin/Projects/flask-tutorial/midyear-circle-337709-3749a3c5b159.json')
    firebase_admin.initialize_app(cred)


from models.user import User

if __name__ == "__main__":
    test_user = User(user_id=0, name='Testik', male=True, email='test@test.ru', password='password',
                     balance=100)

    print(test_user)
import unittest
from os import path

from flask_login import current_user, login_user, FlaskLoginClient
from bs4 import BeautifulSoup

from blog import create_app
from blog import db
import os

from blog.models import get_user_model, get_post_model, get_category_model, get_comment_model

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
app.testing = True

'''
회원가입, 로그인, 로그아웃 부분을 테스트
1. 2명의 유저를 데이터베이스에 넣어 본 후, 데이터베이스에 들어간 유저의 수가 총 2명이 맞는지를 확인한다.
2. auth/sign-up 에서 폼을 통해서 회원가입 요청을 보낸 후, 데이터베이스에 값이 잘 들어갔는지를 확인한다.
3. 로그인 전에는 네비게이션 바에 "login", "sign up" 이 보여야 하고, 로그인한 유저 이름과 "logout" 이 표시되면 안 된다.
'''


class TestAuth(unittest.TestCase):
    # 테스트를 위한 사전 준비
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        # 테스트를 위한 db 설정
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        if not path.exists("tests/" + "test_db"):  # DB 경로가 존재하지 않는다면,
            db.create_all(app=app)  # DB를 하나 만들어낸다.

    # 테스트가 끝나고 나서 수행할 것, 테스트를 위한 데이터베이스의 내용들을 모두 삭제한다.
    def tearDown(self):
        os.remove('test.db')
        self.ctx.pop()

    # 1. 2명의 유저를 데이터베이스에 넣어 본 후, 데이터베이스에 들어간 유저의 수가 총 2명이 맞는지를 확인한다.
    def test_signup_by_database(self):
        self.user_test_1 = get_user_model()(
            email="hello@example.com",
            username="testuserex1",
            password="12345",
            is_staff=True
        )
        db.session.add(self.user_test_1)
        db.session.commit()

        self.user_test_2 = get_user_model()(
            email="hello2@example.com",
            username="testuserex2",
            password="12345",
        )
        db.session.add(self.user_test_2)
        db.session.commit()

        # 데이터베이스에 있는 유저의 수가 총 2명인가?
        self.assertEqual(get_user_model().query.count(), 2)

    # 2. auth/sign-up 에서 폼을 통해서 회원가입 요청을 보낸 후, 데이터베이스에 값이 잘 들어갔는지를 확인한다.
    def test_signup_by_form(self):
        response = self.client.post('/auth/sign-up',
                                    data=dict(email="helloworld@naver.com", username="hello", password1="dkdldpvmvl",
                                              password2="dkdldpvmvl"))
        self.assertEqual(get_user_model().query.count(), 1)

    # 3. 로그인 전에는 네비게이션 바에 "login", "sig up" 이 보여야 하고, 로그인한 유저 이름과 "logout" 이 표시되면 안 된다.
    def test_before_login(self):
        # 로그인 전이므로, 네비게이션 바에는 "login", "sign up" 이 보여야 한다.
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        navbar_before_login = soup.nav  # nav 태그 선택

        self.assertIn("Login", navbar_before_login.text)  # navbar 안에 "Login" 이 들어있는지 테스트
        self.assertIn("Sign Up", navbar_before_login.text, )  # navbar 안에 "Sign Up" 이 들어있는지 테스트
        self.assertNotIn("Logout", navbar_before_login.text, )  # navbar 안에 "Logout" 이 없는지 테스트

        # 로그인을 하기 위해서는 회원가입이 선행되어야 하므로, 폼에서 회원가입을 진행해 준다.
        response = self.client.post('/auth/sign-up',
                                    data=dict(email="helloworld@naver.com", username="hello", password1="dkdldpvmvl",
                                              password2="dkdldpvmvl"))
        # 이후, auth/login 에서 로그인을 진행해 준다.
        with self.client:
            response = self.client.post('/auth/login',
                                        data=dict(email="helloworld@naver.com", username="hello",
                                                  password="dkdldpvmvl"),
                                        follow_redirects=True)
            soup = BeautifulSoup(response.data, 'html.parser')
            navbar_after_login = soup.nav

            # 로그인이 완료된 후, 네비게이션 바에는 로그인한 유저 이름과 "Logout" 이 표시되어야 한다.
            self.assertIn(current_user.username, navbar_after_login.text)
            self.assertIn("Logout", navbar_after_login.text)
            # 로그인이 완료된 후, 네비게이션 바에는 "Login" 과 "Sign Up" 이 표시되면 안 된다.
            self.assertNotIn("Login", navbar_after_login.text)
            self.assertNotIn("Sign up", navbar_after_login.text)


class TestPostwithCategory(unittest.TestCase):
    # 테스트를 위한 사전 준비
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        # 테스트를 위한 db 설정
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        if not path.exists("tests/" + "test_db"):  # DB 경로가 존재하지 않는다면,
            db.create_all(app=app)  # DB를 하나 만들어낸다.

    # 테스트가 끝나고 나서 수행할 것, 테스트를 위한 데이터베이스의 내용들을 모두 삭제한다.
    def tearDown(self):
        os.remove('test.db')
        self.ctx.pop()

    '''
    1. 임의의 카테고리를 넣어본 후, 데이터베이스에 카테고리가 잘 추가되어 있는지 확인한다.
    2. 카테고리를 넣은 후, /categories-list 에 접속했을 때, 넣었던 카테고리들이 잘 추가되어 있는지 확인한다. 
    3. 게시물을 작성할 때에, 로그인하지 않았고, 스태프 권한을 가지고 있지 않다면 접근이 불가능해야 한다.
        - 스태프 권한을 가지고 있지 않은 사용자 1명, 게시물 작성 페이지에 접근할 수 없어야 한다.
        - 스태프 권한을 가지고 있는 사용자 1명, 게시물 작성 페이지에 접근할 수 있어야 한다.
    4. 임의의 카테고리를 넣어본 후,
        웹 페이지에서 폼으로 게시물을 추가할 때에 option 태그에 값이 잘 추가되는지,
        게시물을 추가한 후 게시물은 잘 추가되어 있는지
        저자는 로그인한 사람으로 추가되어 있는지 확인한다.

    '''

    def test_add_category_and_post(self):
        # 이름 = "python" 인 카테고리를 하나 추가하고,
        self.python_category = get_category_model()(
            name="python"
        )
        db.session.add(self.python_category)
        db.session.commit()
        self.assertEqual(get_category_model().query.first().name, "python")  # 추가한 카테고리의 이름이 "python" 인지 확인한다.
        self.assertEqual(get_category_model().query.first().id, 1)  # id는 1로 잘 추가되어있는지 확인한다.
        # 이름 = "rust" 인 카테고리를 하나 추가하고,
        self.rust_category = get_category_model()(
            name="rust"
        )
        db.session.add(self.rust_category)
        db.session.commit()
        self.assertEqual(get_category_model().query.filter_by(id=2).first().name,
                         "rust")  # id가 2인 카테고리의 이름이 "rust" 인지 확인한다.
        # 이름 = "javascript" 인 카테고리를 하나 더 추가해 주자.
        self.rust_category = get_category_model()(
            name="javascript"
        )
        db.session.add(self.rust_category)
        db.session.commit()

        # 카테고리 리스트 페이지에 접속했을 때에, 추가했던 3개의 카테고리가 잘 추가되어 있는지?
        response = self.client.get('/categories-list')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn('python', soup.text)
        self.assertIn('rust', soup.text)
        self.assertIn('javascript', soup.text)

        # 로그인 전에는, 포스트 작성 페이지에 접근한다면 로그인 페이지로 이동해야 한다. 리디렉션을 나타내는 상태 코드는 302이다.
        response = self.client.get('/create-post', follow_redirects=False)
        self.assertEqual(302, response.status_code)

        # 스태프 권한을 가지고 있지 않는 작성자 생성
        response = self.client.post('/auth/sign-up',
                                    data=dict(email="helloworld@naver.com", username="hello", password1="dkdldpvmvl",
                                              password2="dkdldpvmvl"))
        # 스태프 권한을 가지고 있지 않은 작성자가 포스트 작성 페이지에 접근한다면, 권한 거부가 발생해야 한다.
        with self.client:
            response = self.client.post('/auth/login',
                                        data=dict(email="helloworld@naver.com", username="hello",
                                                  password="dkdldpvmvl"),
                                        follow_redirects=True)
            response = self.client.get('/create-post', follow_redirects=False)
            self.assertEqual(403,
                             response.status_code)  # 스태프 권한을 가지고 있지 않은 사람이 /create-post 에 접근한다면, 서버는 상태 코드로 403을 반환해야 한다.
            response = self.client.get('/auth/logout')  # 스태프 권한을 가지고 있지 않은 작성자에서 로그아웃

        # 스태프 권한을 가지고 있는 작성자 생성, 폼에서는 is_staff 를 정할 수 없으므로 직접 생성해야 한다.
        self.user_with_staff = get_user_model()(
            email="staff@example.com",
            username="staffuserex1",
            password="12345",
            is_staff=True
        )
        db.session.add(self.user_with_staff)
        db.session.commit()

        # 스태프 권한을 가지고 있는 유저로 로그인 후, 게시물을 잘 작성할 수 있는지 테스트
        from flask_login import FlaskLoginClient
        app.test_client_class = FlaskLoginClient
        with app.test_client(user=self.user_with_staff) as user_with_staff:
            # 로그인한 상태로, 게시물 작성 페이지에 갔을 때에 폼이 잘 떠야 한다.
            response = user_with_staff.get('/create-post', follow_redirects=True)
            self.assertEqual(response.status_code,
                             200)  # 스태프 권한을 가지고 있는 사용자가 서버에 get 요청을 보냈을 때에, 정상적으로 응답한다는 상태 코드인 200을 돌려주는가?

            # 미리 작성한 카테고리 3개가 셀렉트 박스의 옵션으로 잘 뜨고 있는가?
            soup = BeautifulSoup(response.data, 'html.parser')
            select_tags = soup.find(id='category')
            self.assertIn("python", select_tags.text)
            self.assertIn("rust", select_tags.text)
            self.assertIn("javascript", select_tags.text)

            response_post = user_with_staff.post('/create-post',
                                                 data=dict(title="안녕하세요, 첫 번째 게시물입니다.", content="만나서 반갑습니다!",
                                                           category="1"),
                                                 follow_redirects=True)

            self.assertEqual(1, get_post_model().query.count())  # 게시물을 폼에서 작성한 후, 데이터베이스에 남아 있는 게시물의 수가 1개가 맞는가?

        # 게시물은 잘 추가되어 있는지?
        response = self.client.get(f'/posts/1')
        soup = BeautifulSoup(response.data, 'html.parser')

        # 게시물의 페이지에서 우리가 폼에서 입력했던 제목이 잘 나타나는지?
        title_wrapper = soup.find(id='title-wrapper')
        self.assertIn("안녕하세요, 첫 번째 게시물입니다.", title_wrapper.text)

        # 게시물 페이지에서, 로그인했던 유저의 이름이 저자로 잘 표시되는지?
        author_wrapper = soup.find(id='author-wrapper')
        self.assertIn("staffuserex1", author_wrapper.text)

    def test_update_post(self):
        '''
        임의의 유저를 2명 생성한다. smith, james
        smith 으로 로그인 후, 폼에서 게시물을 하나 생성한다.
        smith로 로그인한 상태에서 smith가 작성한 게시물에 들어갔을 때에, "수정하기" 버튼이 보여야 한다.
        수정하기 버튼을 누르고 수정 페이지에 들어가면, 폼에 원래 내용이 채워져 있어야 한다.
        이후 폼에서 내용을 바꾸고 수정하기 버튼을 누르면, 수정이 잘 되어야 한다.
        smith 에서 로그아웃 후, james 로 로그인 후 smith가 작성한 게시물에 들어갔을 때에, "수정하기" 버튼이 보이지 않아야 한다.
        james 가 smith가 작성한 게시물을 수정하려 한다면(url로 접근하려 한다면), 거부되어야 한다.
        '''

        # 2명의 유저 생성하기
        self.smith = get_user_model()(
            email="smithf@example.com",
            username="smith",
            password="12345",
            is_staff=True,
        )
        db.session.add(self.smith)
        db.session.commit()
        self.james = get_user_model()(
            email="jamesf@example.com",
            username="james",
            password="12345",
            is_staff=True,
        )
        db.session.add(self.james)
        db.session.commit()

        # 2개의 카테고리 생성하기
        self.python_category = get_category_model()(
            name="python"  # id == 1
        )
        db.session.add(self.python_category)
        db.session.commit()
        self.javascript_category = get_category_model()(
            name="javascript"  # id == 2
        )
        db.session.add(self.javascript_category)
        db.session.commit()

        # smith로 로그인 후, 수정 처리가 잘 되는지 테스트
        from flask_login import FlaskLoginClient
        app.test_client_class = FlaskLoginClient
        # smith 로 게시물 작성, 이 게시물의 pk는 1이 될 것임
        with app.test_client(user=self.smith) as smith:
            smith.post('/create-post',
                       data=dict(title="안녕하세요,smith가 작성한 게시물입니다.",
                                 content="만나서 반갑습니다!",
                                 category="1"), follow_redirects=True)
            response = smith.get('/posts/1')  # smith가 본인이 작성한 게시물에 접속한다면,
            soup = BeautifulSoup(response.data, 'html.parser')
            edit_button = soup.find(id='edit-button')
            self.assertIn('Edit', edit_button.text)  # "Edit" 버튼이 보여야 함

            response = smith.get('/edit-post/1')  # smith 가 본인이 작성한 포스트에 수정하기 위해서 접속하면,
            self.assertEqual(200, response.status_code)  # 정상적으로 접속할 수 있어야 함, status_code==200이어야 함
            soup = BeautifulSoup(response.data, 'html.parser')

            title_input = soup.find('input')
            content_input = soup.find('textarea')

            # 접속한 수정 페이지에서, 원래 작성했을 때 사용했던 문구들이 그대로 출력되어야 함
            self.assertIn(title_input.text, "안녕하세요,smith가 작성한 게시물입니다.")
            self.assertIn(content_input.text, "만나서 반갑습니다!")

            # 접속한 수정 페이지에서, 폼을 수정하여 제출
            smith.post('/edit-post/1',
                       data=dict(title="안녕하세요,smith가 작성한 게시물을 수정합니다.",
                                 content="수정이 잘 처리되었으면 좋겠네요!",
                                 category="2"), follow_redirects=True)
            # 수정을 완료한 후, 게시물에 접속한다면 수정한 부분이 잘 적용되어 있어야 함
            response = smith.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            title_wrapper = soup.find(id='title-wrapper')
            content_wrapper = soup.find(id='content-wrapper')

            self.assertIn("안녕하세요,smith가 작성한 게시물을 수정합니다.", title_wrapper.text)
            self.assertIn("수정이 잘 처리되었으면 좋겠네요!", content_wrapper.text)

            # 마찬가지로 smith로 접속한 상태이므로,
            response = smith.get('/posts/1')  # smith가 본인이 작성한 게시물에 접속한다면,
            soup = BeautifulSoup(response.data, 'html.parser')
            edit_button = soup.find(id='edit-button')
            self.assertIn('Edit', edit_button.text)  # "Edit" 버튼이 보여야 함
            response = smith.get('/auth/logout')  # smith 에서 로그아웃
        # james 로 로그인
        with app.test_client(user=self.james) as james:
            response = james.get('/posts/1')  # Read 를 위한 접속은 잘 되어야 하고,
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, 'html.parser')
            self.assertNotIn('Edit', soup.text)  # Edit 버튼이 보이지 않아야 함
            response = james.get('/edit-post/1')  # Update 를 위한 접속은 거부되어야 함
            self.assertEqual(response.status_code, 403)


class TestComment(unittest.TestCase):
    '''
    댓글은 폼에서의 POST 요청을 보냄으로서 이루어집니다.
    "comment" 버튼을 누르면, 폼에 있는 내용이 서버로 전송되고, 그를 받아서 데이터베이스에 저장해야 합니다.
    댓글을 저장하고 나면 댓글을 작성한 해당 게시물로 자동 이동해야 합니다.
    댓글을 저장하고 나면 댓글이 해당 게시물에 잘 달려 있는 것을 확인해야 합니다.
    댓글을 저장하고 나면 작성자가 제대로 표시되어야 합니다.
    로그인을 한 사람만 댓글을 수정할 수 있습니다.
    '''

    # 테스트를 위한 사전 준비
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        # 테스트를 위한 db 설정
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        if not path.exists("tests/" + "test_db"):  # DB 경로가 존재하지 않는다면,
            db.create_all(app=app)  # DB를 하나 만들어낸다.

        # 2명의 유저 생성하기
        self.james = get_user_model()(
            email="jamesf@example.com",
            username="james",
            password="12345",
            is_staff=False,
        )
        db.session.add(self.james)
        db.session.commit()
        self.nakamura = get_user_model()(
            email="nk222f@example.com",
            username="nakamura",
            password="12345",
            is_staff=False,
        )
        db.session.add(self.nakamura)
        db.session.commit()

        # 댓글을 작성할 게시물 하나 생성하기
        self.example_post = get_post_model()(
            title="댓글 작성을 위한 게시물을 추가합니다.",
            content="부디 테스트가 잘 통과하길 바랍니다.",
            category_id="1",
            author_id=1 # 작성자는 james
        )
        db.session.add(self.example_post)
        db.session.commit()
        self.assertEqual(get_post_model().query.count(), 1)

    # 테스트가 끝나고 나서 수행할 것, 테스트를 위한 데이터베이스의 내용들을 모두 삭제한다.
    def tearDown(self):
        os.remove('test.db')
        self.ctx.pop()

    def test_add_comment(self):
        app.test_client_class = FlaskLoginClient
        with app.test_client(user=self.james) as james:
            response = james.post('/create-comment/1', data=dict(content="만나서 반갑습니다!"))
            self.assertEqual(302, response.status_code) # 댓글을 작성하면 해당 페이지로 자동 리디렉션되어야 한다.
            self.assertEqual(get_comment_model().query.count(), 1) # 작성한 댓글이 데이터베이스에 잘 추가되어 있는가?
            response = james.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            comment_wrapper = soup.find(id="comment-wrapper")
            self.assertIn("만나서 반갑습니다!", comment_wrapper.text) # 작성한 댓글의 내용이 게시물의 상세 페이지에 잘 표시되는가?
            self.assertIn("james", comment_wrapper.text) # 작성자의 이름이 잘 표시되는가?
            self.assertIn("Edit comment", comment_wrapper.text) # 작성자로 로그인되어 있을 경우 수정 버튼이 잘 표시되는가?
            james.get('/auth/logout') # james에서 로그아웃
        with app.test_client(user=self.nakamura) as nakamura:
            response = james.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            comment_wrapper = soup.find(id="comment-wrapper")
            self.assertNotIn("Edit comment", comment_wrapper.text) # 작성자로 로그인되어 있지 않을 경우 수정 버튼이 보이지 않는가?

    def test_update_comment(self):
        '''
        임의의 유저로 댓글을 작성하고,
        띄워진 모달 창에서 수정 작업을 거친 후 수정 버튼을 누르면 예전의 댓글 내용이 수정한 내용으로 잘 바뀌어 있어야 한다.
        '''
        app.test_client_class = FlaskLoginClient
        with app.test_client(user=self.james) as james:
            response = james.post('/create-comment/1', data=dict(content="만나서 반갑습니다!")) # james 로 댓글을 하나 작성한 다음,
            self.assertEqual(response.status_code, 302) # 작성이 된 후 정상적으로 리디렉션되어야 한다.
            response = james.post('/edit-comment/1/1', data=dict(content="댓글 내용을 수정합니다!")) # 댓글을 수정해 주고,
            self.assertEqual(302, response.status_code)  # 수정이 완료된 후 정상적으로 리디렉션되어야 한다.
            response = james.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            comment_wrapper = soup.find(id='comment-wrapper')
            self.assertNotIn("만나서 반갑습니다!", comment_wrapper.text) # 기존의 댓글 내용은 있으면 안 되고
            self.assertIn("댓글 내용을 수정합니다!", comment_wrapper.text) # 수정한 댓글의 내용이 표시되어야 한다.
            james.get('/auth/logout') # james에서 로그아웃

    def test_delete_comment(self):
        pass




if __name__ == "__main__":
    unittest.main()

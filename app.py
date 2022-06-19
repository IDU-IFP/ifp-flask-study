from flask import Flask, url_for, redirect
from flask import request

from importlib import reload

# 데이터를 불러오자.
import post_data
from post_data import posts
last_id = posts[-1]['id']  # 마지막 게시물의 id 값을 저장

app = Flask(__name__)

# '/' 를 요청하면 홈페이지로 가게 된다.
@app.route('/')
def home():
    # url_for() 에 문자열로 함수 이름을 넣어 주면, 알아서 url을 생성해 준다.
    return 'This is Home page.' \
           f'<p><a href="{url_for("home")}">home</a></p>' \
           f'<p><a href="{url_for("about_me")}">about_me</a></p>' \
           f'<p><a href="{url_for("create")}">create new post</a></p>'

# '/about_me' 를 요청하면 자기소개 페이지로 가게 된다.
@app.route('/about_me/')
def about_me():
    return 'Let me introduce myself...'

# '/post/read/(포스트의 id)' 를 요청하면 해당 id에 맞는 포스트를 볼 수 있는 페이지로 가게 된다.
@app.route('/post/read/<int:id>')
def read(id):

    # reload
    reload(post_data)
    reloaded_post = posts

    title = ''
    subtitle = ''
    content = ''
    for p in reloaded_post:
        if id == p['id']:
            title = p['title']
            subtitle = p['subtitle']
            content = p['content']
    return f'제목 : {title}<br/>부제목 : {subtitle}<br/>내용 : {content}<br>'

# '/post/create' 를 요청하면 포스트를 작성할 수 있는 페이지로 가게 된다.
@app.route('/post/create', methods=['GET', 'POST'])
def create():
    # POST 요청이 들어온다면 서버는 게시물을 작성하는 역할을 수행해야 합니다.
    if request.method == 'POST':

        '''
            1. 서버로부터 넘어온 값을 저장하고,
            2. post_data.py 파일을 열고,
            3. post_data.py 의 posts 리스트에 서버에서 넘어온 값을 추가한 다음,
            4. 변경된 post_data.py 파일을 저장
        '''

        # form 태그의 name 속성으로 넘어온 값 저장하기
        title = request.form['title']
        subtitle = request.form['subtitle']
        content = request.form['content']

        # post_data.py 파일 열기
        data = open('post_data.py', 'a')

        global last_id

        # post_data.py 의 posts 리스트에 서버에서 넘어온 값을 추가하기
        data.write(f"\nposts.append({{ 'id':{last_id + 1}, 'title':'{title}', 'subtitle':'{subtitle}', 'content':'{content}' }})")

        data.close()
        last_id = last_id + 1 # id 자동으로 올라가게끔

        return redirect(url_for('home'))


    # GET 요청이 들어온다면 서버는 게시물을 작성하는 폼을 보여주는 역할을 수행해야 합니다.
    elif request.method == 'GET':
        return '''
        <form action="/post/create" method="POST">
            <p><input type="text" name="title" placeholder="제목을 입력하세요."></p>
            <p><input type="text" name="subtitle" placeholder="부제목을 입력하세요."></p>
            <p><textarea name="content" placeholder="내용을 입력하세요"></textarea></p>
            <p><input type="submit" value="게시물 작성하기"></p>
        </form>
        '''

if __name__ == '__main__':
    app.run(debug=True)

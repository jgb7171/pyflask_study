from flask import Blueprint, request, render_template, session
from flask import current_app as app
from app.module import dbModule

main = Blueprint('main', __name__, url_prefix='/')

# 로그인,회원가입 등의 기능을 포함하는 클래스
class ManageUser():
	def checkUser(self, userName, password):
		try:
			db_class = dbModule.Database()

			sql = "SELECT idno, username, password, name \
					FROM testDB.user \
					WHERE username = '{userName}' \
					AND password = '{password}'".format(
						userName=userName, password=password)

			row = db_class.executeOne(sql)

			if row is not None:
				return '/main/index.html'
			else:
				return '/main/login.html'
		except:
			return '/main/login.html'

# http://127.0.0.1:5000/로 접속했을때 세션 체크해서
# 로그인화면으로 보낼지 메인화면으로 보낼지
@main.route('/', methods=['GET'])
def index():
    if not session.get('logged_in'):
        return render_template('/main/login.html')
    else:
        return render_template('/main/index.html')

# 로그인버튼 눌렀을 때의 동작
@main.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('/main/login.html')
	else:
		userName = request.form['username']
		password = request.form['password']
		try:
			data = ManageUser.checkUser('', userName, password)
			if data is not None:
				session['logged_in'] = True
				return render_template(data)
			else:
				return 'Login failed'
		except:
			return 'Login failed'

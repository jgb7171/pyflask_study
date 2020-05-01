from flask import Blueprint, request, render_template, session, redirect, url_for
from flask import current_app as app
from app.module import dbModule
from app.module import logModule

main = Blueprint('main', __name__, url_prefix='/')

# 로그인,회원가입 등의 기능을 포함하는 클래스
class ManageUser():
    usr = ''
    pwd = ''

    def __init__(self, userName, password):
        self.usr = userName
        self.pwd = password

    def checkUser(self):
        try:
            db_class = dbModule.Database()

            sql = "SELECT idno, username, password, name \
                    FROM testDB.user \
                    WHERE username = '{userName}' \
                    AND password = '{password}'".format(
                        userName=self.usr, password=self.pwd)

            logModule.log(request, 'sql: ' + sql)

            row = db_class.executeOne(sql)

            logModule.log(request, 'row: ' + str(row))

            return row

        except Exception as ex:
            logModule.log(request, '에러가 발생 했습니다' + str(ex))
            return 'Failed check user'

    def createUser(self, name, sex):
        try:
            db_class = dbModule.Database()

            sql = "INSERT INTO user (username, password, name, sex) \
                    VALUES ('{userName}', '{password}', '{name}', {sex});".format(
                        userName=self.usr, password=self.pwd, name=name, sex=sex)

            logModule.log(request, 'sql: ' + sql)

            db_class.execute(sql)

            db_class.commit()

        except Exception as ex:
            logModule.log(request, '에러가 발생 했습니다' + str(ex))
            db_class.rollback()
            return 'Failed create user'

# http://127.0.0.1:5000/로 접속했을때 세션 체크해서
# 로그인화면으로 보낼지 메인화면으로 보낼지
@main.route('/', methods=['GET'])
def index():
    logModule.log(request, session.get('logged_in'))
    if not session.get('logged_in'):
        return render_template('/main/login.html')
    else:
        if 'name' in session:
            return render_template('/main/index.html', name = session.get('name'))
        else:
            return render_template('/main/index.html')

# 로그인버튼 눌렀을 때의 동작
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/main/login.html')
    else:
        try:
            userName = request.form['username']
            password = request.form['password']
            manageUser = ManageUser(userName = userName, password = password)
            data = manageUser.checkUser()
            if data is not None:
                session['name'] = data['name']
                session['logged_in'] = True
                logModule.log(request, 'name: ' + session.get('name'))
                logModule.log(request, 'logged_in: ' + str(session.get('logged_in')))
                return redirect(url_for('main.index'))
            else:
                logModule.log(request, 'name: ' + session.get('name'))
                logModule.log(request, 'logged_in: ' + str(session.get('logged_in')))
                return redirect(url_for('main.index'))
        except Exception as ex:
            logModule.log(request, '에러가 발생 했습니다' + str(ex))
            return 'Failed login'

@main.route('/logout', methods=['GET'])
def logout():
    logModule.log(request, 'logout')
    session.pop('name', None)
    session.pop('logged_in', None)
    return redirect(url_for('main.index'))

@main.route('/join', methods=['GET'])
def join():
    logModule.log(request, 'join')
    return render_template('/main/join.html')

@main.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('/main/login.html')
    else:
        try:
            joinUserName = request.form['username']
            joinPassword = request.form['password']
            joinName = request.form['name']
            joinSex = request.form['sex']

            #joinManageUser = ManageUser(userName = joinUserName, password = joinPassword)
            #data = joinManageUser.checkUser()

            if joinSex == 'male':
                sex = 0
            else:
                sex = 1
            
            joinManageUser = ManageUser(userName = joinUserName, password = joinPassword)
            joinManageUser.createUser(joinName,sex)

            return render_template('/main/login.html')

        except Exception as ex:
            logModule.log(request, '에러가 발생 했습니다' + str(ex))
            return 'Failed registration'





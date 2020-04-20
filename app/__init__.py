from flask import Flask
 
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# 파일 이름이 index.py이므로
from app.main.index import main as main 
 
# 위에서 추가한 파일을 연동해주는 역할
app.register_blueprint(main) # as main으로 설정해주었으므로

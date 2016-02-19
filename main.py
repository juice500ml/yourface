from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask.ext.bcrypt import Bcrypt

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://yourface:rocks@localhost/yourfaceDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
admin = Admin(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password_hash = db.Column(db.String(60), nullable=False)
    first_name_kr = db.Column(db.String(50), nullable=False)
    last_name_kr = db.Column(db.String(50), nullable=False)
    first_name_en = db.Column(db.String(50), nullable=False)
    middle_name_en = db.Column(db.String(50))
    last_name_en = db.Column(db.String(50), nullable=False)
    student_number = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, password_hash, first_name_kr, last_name_kr, first_name_en, middle_name_en, last_name_en, student_number, last_login):
        self.username = username
        self.password_hash = password_hash
        self.first_name_kr = first_name_kr
        self.last_name_kr = last_name_kr
        self.first_name_en = first_name_en
        self.middle_name_en = middle_name_en
        self.last_name_en = last_name_en
        self.student_number = student_number
        self.last_login = last_login

    def __repr__(self):
        return '<User %r>' % self.username

admin.add_view(ModelView(User,db.session))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return """
        <script src="//code.jquery.com/jquery-1.12.0.min.js"></script>
        <form action="/register" method="POST">
            ID: <input type=text class='usr' id=usr name=usr maxlength="50" /><br>
            PW: <input type=password class='pwd' id=pwd name=pwd /><br>
            PW Again: <input type=password class='pwda' id=pwda name=pwda /><br>
            First Name(KO): <input type=text class='fnk' id=fnk name=fnk maxlength="50"/><br>
            Last Name(KO): <input type=text class='lnk' id=lnk name=lnk maxlength="50"/><br>
            First Name(EN): <input type=text class='fne' id=fne name=fne maxlength="50" /><br>
            Middle Name(EN): <input type=text class='mne' id=mne name=mne maxlength="50" /><br>
            Last Name(EN): <input type=text class='lne' id=lne name=lne maxlength="50" /><br>
            Student Number: <input type=text class='sn' id=sn name=sn maxlength="50" /><br>
            <input type=submit />
        </form>
        <script>
            $('.usr').change(
                function(){
                    var check_id = "/check_username/" + $('.usr').val();
                    $.get(
                        check_id,
                        function (data){
                            alert("쓰셔도 좋습니다.");
                        }
                    ).fail(
                        function (data){
                            alert("겹치는 ID가 있습니다.");
                        }
                    );
                }
            );
            
            var changed_pwda = false;
            $('.pwd').change(
                function(){
                    if ( $('.pwd').val() != $('.pwda').val() )
                        if(changed_pwda)
                            alert("PW가 다릅니다.");
                }
            );

            $('.pwda').change(
                function(){
                    changed_pwda = true;
                    if ( $('.pwd').val() != $('.pwda').val() ) alert("PW가 다릅니다.");
                }
            );

            $('.fnk').change(
                function(){ if ( $('.fnk').val() == "" ) alert("빈 칸입니다."); }
            );
            $('.lnk').change(
                function(){ if ( $('.lnk').val() == "" ) alert("빈 칸입니다."); }
            );
            $('.fne').change(
                function(){ if ( $('.fne').val() == "" ) alert("빈 칸입니다."); }
            );
            $('.lne').change(
                function(){ if ( $('.lne').val() == "" ) alert("빈 칸입니다."); }
            );
            $('.sn').change(
                var num = $('.sn').val();
                function(){
                    if ( num == "") alert("빈 칸입니다.");
                    else if( num !== parseInt(num,10) ) alert("숫자가 아닙니다.")
                }
            );
        </script>
        """
    else:
        username = request.form['usr']
        if not username: return 'Failed', 400
        if len(username)>50: return 'Failed', 400
        found = User.query.filter(
                User.username == username,
                ).first()
        if found: return "Existing Username", 400

        if not request.form['pwd']: return 'Failed', 400
        if request.form['pwd'] != request.form['pwda']: return 'Failed', 400
        password_hash = bcrypt.generate_password_hash(request.form['pwd'])

        first_name_kr = request.form['fnk']
        if not first_name_kr or len(first_name_kr)>50: return 'Failed', 400

        last_name_kr = request.form['lnk']
        if not last_name_kr or len(last_name_kr)>50: return 'Failed', 400

        first_name_en = request.form['fne']
        if not first_name_en or len(first_name_en)>50: return 'Failed', 400
        
        middle_name_en = request.form['mne']
        if len(middle_name_en)>50: return 'Failed', 400
        
        last_name_en = request.form['lne']
        if not last_name_en or len(last_name_en)>50: return 'Failed', 400

        try:
            student_number = int(request.form['sn'])
        except ValueError:
            return 'Failed', 400

        last_login = datetime.now()

        db.session.add(User(username,
            password_hash,
            first_name_kr, 
            last_name_kr,
            first_name_en,
            middle_name_en,
            last_name_en,
            student_number,
            last_login,
            ))
        db.session.commit()
        return "성공하였습니다!"

@app.route("/check_username/<username>")
def check_username(username):
    found = User.query.filter(
            User.username == username,
    ).first()
    if found:
        return "Existing Username", 400
    return "Good to go!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

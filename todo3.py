from flask import *
app = Flask(__name__)



from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///app.db') #user.dbというデータベースを使うという宣言
Base = declarative_base() #データベースのテーブルの親

import datetime
    
class Content3(Base):
    __tablename__ = 'contents3'
    id = Column(Integer, primary_key=True, unique=True) #整数型のidをprimary_keyとして被らないようにする
    content = Column(String)
    date = Column(String)
    day = Column(Integer)
    
    
  
    def __repr__(self):
      return "Content3<{}, {}, {}, {}>".format(self.id,self.content,self.date,self.day)

Base.metadata.create_all(engine) #データベースを構築


SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()



@app.route("/",methods=["GET","POST"])
def start():
    cont = session.query(Content3).all()
    if request.method == "GET":
        return render_template("ToDo.html",cont=cont)
    
    date1 = datetime.date.today()
    days = int(request.form["day"])
    date2 = date1 + datetime.timedelta(days=days)
    mess = Content3(content=request.form["content"],date=date2)
    session.add(mess)
    session.commit()
    cont = session.query(Content3).order_by(Content3.date).all()
    return render_template("ToDo.html",cont = cont)

@app.route("/delete/<int:id>",methods=["POST","GET"])
def delete(id):
    cont = session.query(Content3).all()
    cont = session.query(Content3).filter_by(id=id).first()
    session.delete(cont)
    # mess = Content(content=request.form["content"])
    # session.add(mess)
    session.commit()
    cont = session.query(Content3).all()
    # return render_template("ToDo.html",cont=cont)
    return redirect("/")







if __name__  == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8888, threaded=True)






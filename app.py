from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import Heap as h

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
heap = h.MaxHeap(2**10 - 1)
flag = 0

class Lists(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200),nullable=False)
    priority = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return '<Element %r>' %self.id

@app.route('/', methods=['POST','GET'])
def insertHome():
    if request.method == 'POST':
        sent_elem = request.form['content']
        v,p=0,0
        try:
            print(sent_elem)
            v,p=map(str,sent_elem.split())
            print(v,p,"sss")
        except:
            return "Please enter space seperated values while inserting a value"
        heap.insert(int(p),v)
        print(heap.Heap)
        new_val =Lists(content=v,priority=p)
        try:
            db.session.add(new_val)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'
    else:
        list = Lists.query.order_by(Lists.id).all()
        values=[]
        priorities=[]
        for i in list:
            values.append(i.content)
            priorities.append(i.priority)
            global flag
            if flag < len(list):
                heap.insert(i.priority,i.content)
                flag += 1
        print(heap.Heap)
        print("Values are",values,"Priorities are",priorities)
        return render_template('index.html',items = list)

@app.route('/delete')
def delete():
    delv = heap.extractMax()
    print(delv)
    obj = Lists.query.filter_by(priority = delv).first()
    print(obj)
    item_to_delete = Lists.query.get_or_404(obj.id)
    try:    
        db.session.delete(item_to_delete)
        db.session.commit()
        print(delv)
        print(heap.Heap)
        return redirect('/')

    except:
        return 'Error Deleting'

if __name__ == '__main__':

    app.run(debug=True)
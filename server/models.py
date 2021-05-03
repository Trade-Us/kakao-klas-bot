from server import db

class IDWithSubject(db.Model):
    UserID = db.Column(db.String(20), db.ForeignKey('user.ID', ondelete='CASCADE'), primary_key=True)
    SubjectID = db.Column(db.String(20), db.ForeignKey('subject.ID', ondelete='CASCADE'), primary_key=True)

class User(db.Model):
    ID = db.Column(db.String(20), primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(20), nullable=False)
    UserKey = db.Column(db.String(200), nullable=False)

class Subject(db.Model):
    ID = db.Column(db.String(20), primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Professor = db.Column(db.String(20), nullable=False)
    Schedule = db.Column(db.String(20), nullable=False)

class Assignment(db.Model):
    UserID = db.Column(db.String(20), primary_key=True)
    Title = db.Column(db.String(50), nullable=False,primary_key=True)
    StartDate = db.Column(db.DateTime(),nullable=False)
    EndDate = db.Column(db.DateTime(),nullable=False)
    Submit = db.Column(db.Boolean,nullable=False)
    SubjectID = db.Column(db.String(20), db.ForeignKey('subject.ID', ondelete='CASCADE'),nullable=False,primary_key=True)

class Notice(db.Model):
    Title = db.Column(db.String(50), nullable=False,primary_key=True)
    Writer = db.Column(db.String(20), nullable=False)
    Date = db.Column(db.DateTime(),nullable=False)
    Contents = db.Column(db.Text(), nullable=False)
    SerialNum = db.Column(db.Integer, nullable=False)
    SubjectID = db.Column(db.String(20), db.ForeignKey('subject.ID',ondelete='CASCADE'), nullable= False,primary_key=True)

class OnlineLecture(db.Model):
    UserID = db.Column(db.String(20),nullable = False,primary_key=True)
    Title = db.Column(db.String(50),nullable = False)
    StartDate = db.Column(db.DateTime(),nullable=False)
    EndDate = db.Column(db.DateTime(),nullable=False)
    Progress = db.Column(db.Integer, nullable=False)
    Contents = db.Column(db.Text(), nullable=False)
    Week = db.Column(db.Integer, nullable=False,primary_key=True)
    Episode = db.Column(db.Integer, nullable=False,primary_key=True)
    SubjectID = db.Column(db.String(20),db.ForeignKey('subject.ID',ondelete='CASCADE'), nullable = False,primary_key=True)

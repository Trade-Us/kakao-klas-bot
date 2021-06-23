from sqlalchemy import Column, Integer, String, DateTime , Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class IDWithSubject(Base):
    __tablename__ = 'id_with_subject'
    UserID = Column(String(20), ForeignKey('user.ID', ondelete='CASCADE'), primary_key=True)
    SubjectID = Column(String(20), ForeignKey('subject.ID', ondelete='CASCADE'), primary_key=True)

    def __init__(self, UserID, SubjectID):
        self.UserID = UserID
        self.SubjectID = SubjectID  
    def __repr__(self):
        return "<IDWithSubject('%s', '%s')>" %(self.UserID, self.SubjectID)


class User(Base):
    __tablename__ = 'user'
    ID = Column(String(20), primary_key=True)
    Name = Column(String(20), nullable=False)
    Password = Column(String(100), nullable=False)
    UserKey = Column(String(200),nullable=False)
    def __init__(self, ID, Name, Password,UserKey):
        self.ID = ID
        self.Name = Name
        self.Password = Password
        self.UserKey = UserKey
    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s')>" %(self.ID, self.Name,self.Password, self.UserKey)

class NewUser(Base):
    __tablename__ = 'new_user'
    ID = Column(String(20), primary_key=True)
    Name = Column(String(20), nullable=False)
    Password = Column(String(100), nullable=False)
    UserKey = Column(String(200),nullable=False)
    def __init__(self, ID, Name, Password,UserKey):
        self.ID = ID
        self.Name = Name
        self.Password = Password
        self.UserKey = UserKey
    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s')>" %(self.ID, self.Name,self.Password, self.UserKey)

class Subject(Base):
    __tablename__ = 'subject'
    ID = Column(String(20), primary_key=True)
    Name = Column(String(20), nullable=False)
    Professor = Column(String(20), nullable=False)
    Schedule = Column(String(20), nullable=False)

    def __init__(self, ID, Name, Professor, Schedule):
        self.ID = ID
        self.Name = Name
        self.Professor = Professor
        self.Schedule = Schedule
    def __repr__(self):
        return "<Subject('%s', '%s', '%s', '%s')>" %(self.ID, self.Name, self.Professor, self.Name)

class Assignment(Base):
    __tablename__ = 'assignment'
    UserID = Column(String(20), primary_key=True)
    Title = Column(String(50), nullable=False,primary_key=True)
    StartDate =Column(DateTime(),nullable=False)
    EndDate = Column(DateTime(),nullable=False)
    Submit = Column(Boolean,nullable=False)
    SubjectID = Column(String(20), ForeignKey('subject.ID', ondelete='CASCADE'),nullable=False,primary_key=True)

    def __init__(self,UserID, Title, StartDate, EndDate, Submit, SubjectID):
        self.UserID = UserID
        self.Title = Title
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.Submit = Submit
        self.SubjectID = SubjectID
    def __repr__(self):
        return "<Assignment('%s', '%s', '%s', '%s', '%s', '%s')>" %(self.UserID, self.Title, str(self.StartDate), str(self.EndDate), str(self.Submit),self.SubjectID)

class Notice(Base):
    __tablename__ = 'notice'
    Title = Column(String(50), nullable=False,primary_key=True)
    Writer = Column(String(20), nullable=False)
    Date = Column(DateTime(),nullable=False)
    Contents = Column(Text(), nullable=False)
    SubjectID = Column(String(20), ForeignKey('subject.ID',ondelete='CASCADE'), nullable= False,primary_key=True)

    def __init__(self, Title, Writer, Date, Contents, SubjectID):

        self.Title = Title
        self.Writer = Writer
        self.Date = Date
        self.Contents = Contents
        self.SubjectID = SubjectID
    def __repr__(self):
        return "<Assignment('%s', '%s', '%s', '%s', '%s')>" %(self.Title, self.Writer, str(self.Date), str(self.Contents),self.SubjectID)

class OnlineLecture(Base):
    __tablename__ = 'online_lecture'
    UserID = Column(String(20),nullable = False,primary_key=True)
    Title = Column(String(50),nullable = False)
    StartDate = Column(DateTime(),nullable=False)
    EndDate = Column(DateTime(),nullable=False)
    Progress = Column(Integer, nullable=False)
    Contents = Column(Text(), nullable=False)
    Week = Column(Integer, nullable=False,primary_key=True)
    Episode = Column(Integer, nullable=False,primary_key=True)
    SubjectID = Column(String(20),ForeignKey('subject.ID',ondelete='CASCADE'), nullable = False,primary_key=True)

    def __init__(self,UserID, Title,StartDate, EndDate, Progress, Contents, Week, Episode,SubjectID):
        self.UserID = UserID
        self.Title = Title
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.Progress = Progress
        self.Contents = Contents
        self.Week = Week
        self.Episode = Episode
        self.SubjectID = SubjectID
    def __repr__(self):
        return "<OnlineLecture('%s', '%s', '%s', '%s', '%d', '%s', '%d', '%d', '%s')>" %(self.UserID, self.Title, str(self.StartDate), str(self.EndDate), self.Progress, str(self.Contents),self.Week,self.Episode,self.SubjectID)


class Scores(Base):
    __tablename__ = 'scores'
    ID = Column(String(20), primary_key=True)
    Name = Column(String(20), nullable=False)
    SubjectName = Column(String(20), primary_key=True)
    Score = Column(String(10), nullable=False)
    def __init__(self, ID, Name, SubjectName, Score):
        self.ID = ID
        self.Name = Name
        self.SubjectName = SubjectName
        self.Score = Score
    def __repr__(self):
        return "<Scores('%s', '%s', '%s', '%s')>" %(self.ID, self.Name,self.SubjectName, self.Score)

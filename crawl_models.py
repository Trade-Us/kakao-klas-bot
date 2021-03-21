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
    Password = Column(String(20), nullable=False)
    def __init__(self, ID, Name, Password):
        self.ID = ID
        self.Name = Name
        self.Password = Password
    def __repr__(self):
        return "<User('%s', '%s', '%s')>" %(self.ID, self.Name,self.Password)

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
        self.Name = Name
    def __repr__(self):
        return "<Subject('%s', '%s', '%s', '%s')>" %(self.ID, self.Name, self.Professor, self.Name)

class Assignment(Base):
    __tablename__ = 'assignment'
    ID = Column(Integer, primary_key=True)
    Title = Column(String(50), nullable=False)
    StartDate =Column(DateTime(),nullable=False)
    EndDate = Column(DateTime(),nullable=False)
    Submit = Column(Boolean,nullable=False)
    SubjectID = Column(String(20), ForeignKey('subject.ID', ondelete='CASCADE'),nullable=False)

    def __init__(self, Title, StartDate, EndDate, Submit, SubjectID):

        self.Title = Title
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.Submit = Submit
        self.SubjectID = SubjectID
    def __repr__(self):
        return "<Assignment('%d', '%s', '%s', '%s', '%s', '%s')>" %(self.ID, self.Title, str(self.StartDate), str(self.EndDate), str(self.Submit),self.SubjectID)

class Notice(Base):
    __tablename__ = 'notice'
    ID = Column(Integer, primary_key=True)
    Title = Column(String(50), nullable=False)
    Writer = Column(String(20), nullable=False)
    Date = Column(DateTime(),nullable=False)
    Contents = Column(Text(), nullable=False)
    SerialNum = Column(Integer, nullable=False)
    SubjectID = Column(String(20), ForeignKey('subject.ID',ondelete='CASCADE'), nullable= False)

    def __init__(self, Title, Writer, Date, Contents, SerialNum, SubjectID):

        self.Title = Title
        self.Writer = Writer
        self.Date = Date
        self.Contents = Contents
        self.SerialNum = SerialNum
        self.SubjectID = SubjectID
    def __repr__(self):
        return "<Assignment('%d', '%s', '%s', '%s', '%s', '%d', '%s')>" %(self.ID, self.Title, self.Writer, str(self.Date), str(self.Contents),self.SerialNum,self.SubjectID)

class OnlineLecture(Base):
    __tablename__ = 'online_lecture'
    ID = Column(Integer, primary_key=True)
    StartDate = Column(DateTime(),nullable=False)
    EndDate = Column(DateTime(),nullable=False)
    Progress = Column(Integer, nullable=False)
    Contents = Column(Text(), nullable=False)
    Week = Column(Integer, nullable=False)
    Episode = Column(Integer, nullable=False)
    SubjectID = Column(String(20),ForeignKey('subject.ID',ondelete='CASCADE'), nullable = False)

    def __init__(self, StartDate, EndDate, Progress, Contents, Week, Episode,SubjectID):

        self.StartDate = StartDate
        self.EndDate = EndDate
        self.Progress = Progress
        self.Contents = Contents
        self.Week = Week
        self.Episode = Episode
        self.SubjectID = SubjectID
    def __repr__(self):
        return "<OnlineLecture('%d', '%s', '%s', '%d', '%s', '%d', '%d', '%s')>" %(self.ID, str(self.StartDate), str(self.EndDate), self.progress, str(self.Contents),self.Week,self.Episode,self.SubjectID)
def add_Notice(data):

    title=data[1]
    writer=data[3]
    date=data[4]
    contents=""
    serialNum=data[0]
    subjectID=""

    notice=Notice(title, writer,date, contents, serialNum, subjectID)
    db_session.add(notice)
    db_session.commit()
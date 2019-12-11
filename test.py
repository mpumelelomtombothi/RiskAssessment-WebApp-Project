def domain(id):
    cur1 = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()

    result = cur1.execute("SELECT id, question, question_code, answers FROM assessment WHERE DOMAIN = %s",[id] )
    question = cur1.fetchall()

    q = {}
    ans = {}
    for i in question:
        if i['question'] != '':
            q[i['question_code']] = i['question']
            answers = i['answers'].replace('(','')
            answers = answers.replace(')','')
            answers=answers.split(',')
            ans[i['question_code']] = answers
            #li_u_removed = [str(i) for i in ans]
    

   
    return render_template('domain.html', question = q, answers =ans)
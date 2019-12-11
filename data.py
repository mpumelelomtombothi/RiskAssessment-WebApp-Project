def Domains():
    domains = [
        {'name':'Information Security Governance and Risk Management'},
        {'name':'Legal,Regulations & Compliance'},
        {'name':'Business Continuity & Disaster Recovery Planning'},
        {'name':'Privacy'},
        {'name':'Asset Management'},
        {'name':'Human Resource'},
        {'name':'Supplier Security'},
        {'name':'Physical (Environment) Security'},
        {'name':'Security Architecture and Design'},
        {'name':'Telecommunications and Network Security'},
        {'name':'Access Control'},
        {'name':'Operations Security'},
        {'name':'Cryptography'},
        {'name':'Software Development and Application Security'},
        {'name':'Incident Response'}
    ]
    return domains

def Questions(q):
    question_list = []
    for question in q:
        if question not in question_list:
            question_list.append(question)
            #print question_list
        #questions = [{'question': q}]

    return question_list

def Answers(ans):
    answers_list = []
    for answer in ans:
        if answer not in answers_list:
            answers_list.append(answer)
            print answer
        #questions = [{'question': q}]

    return answers_list














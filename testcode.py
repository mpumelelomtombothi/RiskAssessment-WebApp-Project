# -*- coding: utf-8 -*-
import MySQLdb
from xlrd import open_workbook

db = MySQLdb.connect("localhost", "mpumi", "sabricsql", "TESTDB")


wb = open_workbook('actualsheet.xlsx')
ws = wb.sheet_by_name('All Questions')
cursor = db.cursor()

for row in range(11,ws.nrows):
    
    domain = ws.cell(row, 3).value
    question_code = ws.cell(row, 5).value
    function = ws.cell(row, 7).value
    responsible_role = ws.cell(row, 8).value
    priority_level = ws.cell(row, 9).value
    question_present = ws.cell(row, 10).value
    threat_category = ws.cell(row, 11).value
    example_vulnerability = ws.cell(row, 12).value
    question = ws.cell(row, 13).value
    ans = ws.cell(row, 67).value, ws.cell(row, 68).value, ws.cell(row, 69).value,ws.cell(row, 70).value, ws.cell(row, 71).value, ws.cell(row, 72).value, ws.cell(row, 73).value, ws.cell(row, 74).value
    controls = ws.cell(row, 80).value, ws.cell(row, 81).value, ws.cell(row, 82).value, ws.cell(row, 83).value, ws.cell(row, 84).value, ws.cell(row, 85).value, ws.cell(row, 86).value
    standard = ws.cell(row, 87).value, ws.cell(row, 88).value, ws.cell(row, 89).value, ws.cell(row, 90).value, ws.cell(row, 91).value, ws.cell(row, 92).value, ws.cell(row, 93).value

    try:
    
        print ans
        cursor.execute('insert into assessment (DOMAIN,QUESTION_CODE,FUNCTION,RESPONSIBLE_ROLE,PRIORITY_LEVEL,QUESTION_PRESENT,THREAT_CATEGORY,EXAMPLE_VULNERABILITY,QUESTION,ANSWERS,CONTROLS,STANDARDS) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % \
                        (domain,question_code,function,responsible_role,priority_level,question_present,threat_category,example_vulnerability,question,ans,controls,standard))
    except:
        pass

    db.commit()

db.close()




   
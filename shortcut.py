import pyodbc
from collections import defaultdict
import os
def connection():
    connection=pyodbc.connect(driver='{SQL Server}', server='10.52.2.22,50001', database='cvent_report',uid='cvent',pwd='n0rth')
    connection.autocommit=True
    cursor=connection.cursor()
    
    connection_silo=pyodbc.connect(driver='{SQL Server}', server='10.20.16.147,50001', database='cvent_report',uid='cvent',pwd='n0rth')
    connection_silo.autocommit=True
    cursor_silo=connection_silo.cursor()
    
    cursor.execute(str(execute_query('t2')))
    connection.commit()
    cursor_silo.execute(str(execute_query('s432')))
    connection_silo.commit()

    count=1
    result=compare_decision(cursor,cursor_silo)
    print count,result
    p=cursor.nextset()
    q=cursor_silo.nextset()
    count+=1
    while p and q:
        result=compare_decision(cursor,cursor_silo)
        print count,result
        count+=1
        p=cursor.nextset()
        q=cursor_silo.nextset()
    cursor.close()
    del cursor
    cursor_silo.close()
    del cursor_silo
    connection.close()
    connection_silo.close()

def execute_query(region):
    files=os.listdir(os.getcwd())
    for f in files:
        if region in f:
            execute = f
    with open(execute,'r') as current_execution:
    
        commands= current_execution.read()
        
    return commands
def compare_decision(cursor,cursor_silo):

    t2=cursor.fetchall()
    
    silo=cursor_silo.fetchall()
  
    result_t2,result_silo,result_temp=[],[],[]
    column_t2=[col[0] for col in cursor.description]
    column_silo=[col[0] for col in cursor_silo.description]

    for i in t2:
        result_t2.append(dict(zip(column_t2,i)))
    for i in silo:
        result_silo.append(dict(zip(column_silo,i)))
    
    dict_t2,dict_silo=defaultdict(list),defaultdict(list)
    for i in result_t2:
        for j in i:
            dict_t2[j].append(i[j])
        

    for i in result_silo:
        for j in i:
            dict_silo[j].append(i[j])
    for i in dict_t2:
        if not len(dict_t2[i])==len(dict_silo[i]):
            return "Unequal"
        elif len(dict_t2[i])==len(dict_silo[i]) and i.endswith(('stub', 'num', 'date', 'by')):
            result_temp.append(compare_similarity(dict_t2[i],dict_silo[i]))
            
        else:
            result_temp.append(compare_equality(dict_t2[i],dict_silo[i]))
            
    
    if "Unequal" in result_temp:
        return "Unequal"
    else:
        return "Equal"
        



def compare_temp(a,b):
    temp_a,temp_b,count_a,count_b=[],[],[],[]
    for i in a:
        if i not in temp_a:
            temp_a.append(i)
    for i in b:
        if i not in temp_b:
            temp_b.append(i)
    for i in temp_a:
        count_a.append(a.count(i))
    for i in temp_b:
        count_b.append(b.count(i))
    return zip(temp_a,count_a),zip(temp_b,count_b)


def compare_equality(a,b):
    res=[]
    comp_a,comp_b=compare_temp(a,b)
    for i,j in zip(comp_a,comp_b):
        if i[0]==j[0] and i[1]==j[1]:
            res.append("True")
        else:
            res.append("False")
    if "False" in res:
        return "Unequal"
    return "Equal"

def compare_similarity(a,b):
    res=[]
    comp_a,comp_b=compare_temp(a,b)
    for i,j in zip(comp_a,comp_b):
        if len(comp_a)==len(comp_b) and i[1]==j[1]:
            res.append("True")
        else:
            res.append("False")
    if "False" in res:
        return "Unequal"
    return "Equal"

if __name__=='__main__':
    connection()

import cx_Oracle


userpwd = "teste" # Obtain password string from a user prompt or environment variable


try:
    pool = cx_Oracle.SessionPool("tester", userpwd, "localhost/XE", min=2, max=5, increment=1, encoding="UTF-8")
except cx_Oracle.DatabaseError as error:
    print(error)

con1 = pool.acquire()
con2 = pool.acquire()
con3 = pool.acquire()
con4 = pool.acquire()
con5 = pool.acquire()

cur1 = con1.cursor()
cur2 = con2.cursor()
cur3 = con3.cursor()
cur4 = con4.cursor()
cur5 = con5.cursor()

for result in cur1.execute("select 'cur1: ' || sysdate from dual"):
    print(result)
for result in cur2.execute("select 'cur2: ' || sysdate from dual"):
    print(result)
for result in cur3.execute("select 'cur3: ' || sysdate from dual"):
    print(result)
for result in cur4.execute("select 'cur4: ' || sysdate from dual"):
    print(result)
for result in cur5.execute("select 'cur5: ' || sysdate from dual"):
    print(result)

try:
    con6 = pool.acquire()
except cx_Oracle.DatabaseError:
    pool.release(con5)
    con6 = pool.acquire()
    cur6 = con6.cursor()
    for result in cur6.execute("select 'cur6: ' || sysdate from dual"):
        print(result)

pool.release(con1)
pool.release(con2)
pool.release(con3)
pool.release(con4)
pool.release(con6)
pool.close()

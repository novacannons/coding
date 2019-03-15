import cx_Oracle
import paramiko

cmd = "free -m | awk '/Mem:/' | awk '{print $2, $3, $4}'"
conn = cx_Oracle.connect('espresso/8282082@192.168.6.206:1521/cpberp11')
db = conn.cursor()
db.execute('select ip, port from svr_list')

ret = []
for record in db:
	c = list(record)
	ret.append(c)

#db.close()
#conn.close()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def connection(host, port):
	print(host)
	ssh.connect(host, username='chk1417', port=port, password='8282op82@#')
	ssh.invoke_shell()
	stdin, stdout, stderr = ssh.exec_command(cmd)
	for line in stdout:
		a = line.rstrip('\n').split(' ')
		b = int(a[2])*100/int(a[0])
		#print("%0.1f"%b)
		#print(b)
		db.execute("insert into MEM (ip, SEQ, mem, REG_DATE) values (:ip, MEM_SEQ.NEXTVAL, :mem, SYSDATE)", ip=host, mem=b)
		db.execute("commit")
	ssh.close()


for i in range(len(ret)):
	#print(ret[i][0])
	connection(ret[i][0], ret[i][1])
		

db.close()
conn.close()

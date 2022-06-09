from termcolor import cprint















#host and port should stay in the 19/20 lines

HOST='192.168.43.219'
PORT=4466
from os import mkdir, path, system

dir_exist = path.isdir("./monitor_transfers")
if dir_exist == False:
	mkdir("./monitor_transfers")

cprint("[!] Transfers will be found in ./monitor_transfers", 'yellow' ,attrs=['bold'])
cprint(('[!] To stop serving run: pkill -f "python3 Scripts/monitor_server.py" && pkill -f "nc -lvp{port}"').format(port=PORT), 'yellow' ,attrs=['bold'])

i=1
while True:
	command = "nc -lvp"+ str(PORT) +" > monitor_transfers/docs" +str(i)
	system(command)
	i += 1

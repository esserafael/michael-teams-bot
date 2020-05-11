import subprocess, json, re


command = "Get-Service -Name Audiosrv -ComputerName asl-ad04"

p = subprocess.Popen(
    [
        "powershell.exe", 
        "({}) | ConvertTo-Json -Compress".format(command)
    ], 
    stdout=subprocess.PIPE
    )

result = (p.communicate()[0]).decode('cp1252')

if re.search("^{", result):
    print("Valido")

print(result)
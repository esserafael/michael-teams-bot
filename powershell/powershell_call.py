import subprocess, json, re

class PowershellCall:
    def __init__(self):
        pass

    def invoke(self, command: str):
        p = subprocess.Popen(
            [
                "powershell.exe", 
                "({}) | ConvertTo-Json -Compress".format(command)
            ], 
            stdout=subprocess.PIPE
            )
        result = (p.communicate()[0]).decode('cp1252')

        if re.search("^{", result):
            return json.loads(result)
            
        return

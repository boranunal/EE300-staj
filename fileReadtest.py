cmdFile = open('testCMD.txt','r')

cmds = cmdFile.readlines()
for cmd in cmds:
    cmd = cmd.strip()
    cmd = cmd.split()[0]
    print(cmd)

# import os

# path = "D:\games\Quake III QuadDamaged\quake3e.x64.exe"

# path2 = "*Minecraft*.exe"
# os.system("taskkill /im {}".format(path2))


import wmi
import os
import time
# Initializing the wmi constructor
f = wmi.WMI()
PERIOD_MIN = 1  
# Printing the header for the later columns
# print("pid   Process name")

STOPLIST = ['Minecraft'] 
#['gaming', 'minecraft', 'Minecraft', 'msedge']
def stop_minecraft():
    print("stop minecraft!")
    flag = True
    while flag:
        for process in f.Win32_Process():
            for word in STOPLIST:
                if word in process.Name:
                    with open("prlist.txt", "w") as fout:
                        print(process, file=fout)
                    print(f"{process.ProcessId:<10} {process.Name}") 
                    os.system("taskkill /f /im {}".format(process.Name))
                    flag = False


    
def list_processes():
    with open("prlist.txt", "w") as fout:
        processes = list(f.Win32_Process())
        print(processes, file=fout) 
        
MINECRAFT_CAPTION = 'Minecraft.Windows.exe'
def get_minecraft_process():
    for p in f.Win32_Process():
        if p.Caption == MINECRAFT_CAPTION:
            return p
    return None
   
def kill_p(pid):
    os.system("taskkill /f /im {}".format(pid))
    
def db_check(mp):
    print(mp.Caption)
    print(mp.CreationDate)
    print(mp.ProcessId)
    
    
if __name__ == "__main__":
    mp = get_minecraft_process()
    kill_p(mp.ProcessId)
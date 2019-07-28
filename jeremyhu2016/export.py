import os
directory = '/Users/jeremy/Repositories/10minuteseveryday/jeremyhu2016'
subdirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
totalnum = 0
errnum = 0
for modelname in subdirectories:
    if modelname.startswith("week"):
        continue
    cmd = '/Users/jeremy/Repositories/dust3d/Debug/dust3d.app/Contents/MacOS/dust3d' + ' ./' + modelname + '/' + modelname + '.ds3 -o /Users/jeremy/Desktop/allinone/' + modelname + '.fbx'
    returnvalue = os.system(cmd)
    totalnum = totalnum + 1
    if 0 != returnvalue:
        errnum = errnum + 1
        print modelname, "export failed"
print errnum, totalnum
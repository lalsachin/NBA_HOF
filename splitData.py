import glob
import os
import shutil
from random import shuffle

ret = []
for fName in glob.glob('/Users/rahulmatta/Desktop/EECS 349/NBA_HOF/NBA_DATA_HALL_OF_FAMERS/*'):
    ret.append(fName)


shuffle(ret)

lengthRet = len(ret)

#for r in ret:
#ll    print(r)

for i in range(120):
    shutil.copyfile(ret[i],'/Users/rahulmatta/Desktop/EECS 349/NBA_HOF/Training/'+os.path.basename(ret[i]))

for i in range(120,146):
    shutil.copyfile(ret[i],'/Users/rahulmatta/Desktop/EECS 349/NBA_HOF/Testing/'+os.path.basename(ret[i]))

for i in range(146,172):
    shutil.copyfile(ret[i],'/Users/rahulmatta/Desktop/EECS 349/NBA_HOF/Validation/'+os.path.basename(ret[i]))


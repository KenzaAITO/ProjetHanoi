#Magician
import math


dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)
moveX=0;moveY=0;moveZ=10;moveFlag=-1
pos = dType.GetPose(api)
x = pos[0]
y = pos[1]
z = pos[2]
rHead = pos[3]
while(True):
    moveFlag *= -1
    for i in range(5):
        dType.SetPTPCmd(api, 2, x+moveX, y+moveY, z+moveZ, rHead, 1)
        moveX += 10 * moveFlag
        dType.SetPTPCmd(api, 2, x+moveX, y+moveY, z+moveZ, rHead, 1)
        dType.SetPTPCmd(api, 2, x+moveX, y+moveY, z, rHead, 1)
        dType.SetEndEffectorSuctionCup(api, enableCtrl,  on, isQueued=0)


#Magician
import math


dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)
moveX=0;moveY=0;moveZ=10;moveFlag=-1
pos = dType.GetPose(api)
x = pos[0]
y = pos[1]
z = pos[2]
rHead = pos[3]
while(True):
    moveFlag *= -1
    for i in range(5):
        dType.SetPTPCmd(api, 2, x+moveX, y+moveY, z+moveZ, rHead, 1)
        moveX += 10 * moveFlag
        dType.SetPTPCmd(api, 2, x+moveX, y+moveY, z+moveZ, rHead, 1)
        dType.SetPTPCmd(api, 2, x+moveX, y+moveY, z, rHead, 1)
        dType.SetEndEffectorSuctionCup(api, enableCtrl,  on, isQueued=0)


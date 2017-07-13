# Autogenerated with SMOP 
from smop.core import *
# ClosureAlgoritm.m

    
@function
def ClosureAlgoritm(umano_id=None,posture_0=None,posture_1=None,arm_posture=None,graspFingers=None,*args,**kwargs):
    varargin = ClosureAlgoritm.varargin
    nargin = ClosureAlgoritm.nargin

    #graspFingers = [1 1 1 0 0]
    
    arm_postureStr=mat2str(reshape(transpose(arm_posture),1,numel(arm_posture)))
# ClosureAlgoritm.m:5
    # CMC, MCP (Extension, Flexion, Adduccion, Abduccion) 
# IP, PIP, DIP (Extension, Flexion)
# ORDEN DE LOS DATOS: CMC MCP ( IP || PIP DIP )
    thumb_limits=orProblemSendCommand(cat('gethandlimits Thumb'),umano_id)
# ClosureAlgoritm.m:10
    index_limits=orProblemSendCommand(cat('gethandlimits Index'),umano_id)
# ClosureAlgoritm.m:11
    middle_limits=orProblemSendCommand(cat('gethandlimits Middle'),umano_id)
# ClosureAlgoritm.m:12
    ring_limits=orProblemSendCommand(cat('gethandlimits Ring'),umano_id)
# ClosureAlgoritm.m:13
    small_limits=orProblemSendCommand(cat('gethandlimits Small'),umano_id)
# ClosureAlgoritm.m:14
    limites[1,:]=Convert_str2mat(thumb_limits,1,12)
# ClosureAlgoritm.m:16
    limites[2,:]=Convert_str2mat(index_limits,1,12)
# ClosureAlgoritm.m:17
    limites[3,:]=Convert_str2mat(middle_limits,1,12)
# ClosureAlgoritm.m:18
    limites[4,:]=Convert_str2mat(ring_limits,1,12)
# ClosureAlgoritm.m:19
    limites[5,:]=Convert_str2mat(small_limits,1,12)
# ClosureAlgoritm.m:20
    limites_inf=dot(cat(limites[:,1],limites[:,3],limites[:,5],limites[:,7],limites[:,9],limites[:,11]),pi) / 180
# ClosureAlgoritm.m:22
    limites_sup=dot(cat(limites[:,2],limites[:,4],limites[:,6],limites[:,8],limites[:,10],limites[:,12]),pi) / 180
# ClosureAlgoritm.m:23
    matrix_normals_contactPointsIN=matlabarray([])
# ClosureAlgoritm.m:26
    robots=orEnvGetRobots()
# ClosureAlgoritm.m:27
    robot=robots[1]
# ClosureAlgoritm.m:28
    posture_inicial=copy(posture_0)
# ClosureAlgoritm.m:30
    N=50
# ClosureAlgoritm.m:32
    velocity=(posture_1 - posture_0) / N
# ClosureAlgoritm.m:33
    numGraspFingers=size(find(graspFingers == 1),2)
# ClosureAlgoritm.m:34
    i=0
# ClosureAlgoritm.m:35
    fingersIN=matlabarray(cat(1,1,1,1,1))
# ClosureAlgoritm.m:36
    flag=numel(find(fingersIN == 0))
# ClosureAlgoritm.m:37
    while flag < numGraspFingers:

        i=i + 1
# ClosureAlgoritm.m:40
        if i > 100:
            break
        if i > (N - 5):
            velocity[find(graspFingers == 0),:]=(posture_1[find(graspFingers == 0),:] - posture_0[find(graspFingers == 0),:]) / N
# ClosureAlgoritm.m:43
        posture_anterior=copy(posture_0)
# ClosureAlgoritm.m:46
        posture_0,fingersOUT,matrix_normals_contactPointsOUT=CloseHandVelocity(1,posture_anterior,fingersIN,umano_id,arm_postureStr,posture_inicial,velocity,fingersIN,limites_inf,limites_sup,matrix_normals_contactPointsIN,nargout=3)
# ClosureAlgoritm.m:47
        fingersIN=copy(fingersOUT)
# ClosureAlgoritm.m:48
        matrix_normals_contactPointsIN=copy(matrix_normals_contactPointsOUT)
# ClosureAlgoritm.m:49
        fingersOUT,matrix_normals_contactPointsOUT=checkCollisionODE(matrix_normals_contactPointsIN,robot,fingersIN,umano_id,nargout=2)
# ClosureAlgoritm.m:50
        flag=numel(find(fingersOUT == 0))
# ClosureAlgoritm.m:51
        fingersIN=copy(fingersOUT)
# ClosureAlgoritm.m:52
        matrix_normals_contactPointsIN=copy(matrix_normals_contactPointsOUT)
# ClosureAlgoritm.m:53

    
    #Remove fingers that did not contact
    fingers=matlabarray(cat(1,2,3,4,5))
# ClosureAlgoritm.m:57
    fingers[find(fingersIN == 1)]=[]
# ClosureAlgoritm.m:58
    #codigo cierre completo FALTA ADAPTARLO
# fingers = [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15];
# joint_movements(1,:) = [1 1 1];
# joint_movements(2,:) = [1 1 1];
# joint_movements(3,:) = [1 1 1];
# joint_movements(4,:) = [1 1 1];
# joint_movements(5,:) = [1 1 1];
# while flag < 5
#     i = i + 1; 
#     posture_anterior = posture;
#     [posture] = CloseHandFull (i, posture_anterior, umano_id, joint_movements, arm_postureStr, posture_inicial);
#     #pause(0.01);
#     [joint_movements, fingersOUT, matrix_normals_contactPointsOUT] = checkCollisionODEFull(robot, joint_movements, fingersIN, matrix_normals_contactPointsIN);
#     flag=numel(find(fingersOUT == 0));   
#     fingersIN = fingersOUT;
#     matrix_normals_contactPointsIN = matrix_normals_contactPointsOUT;     
# end
    
    contactsVector=matlabarray([])
# ClosureAlgoritm.m:80
    finalGraspPosture=matlabarray([])
# ClosureAlgoritm.m:81
    if flag > 2:
        for i in fingers.reshape(-1):
            for j in arange(1,3).reshape(-1):
                if size(matrix_normals_contactPointsIN.point[i],1) == 0:
                    contactsVector[j,i]=0.0
# ClosureAlgoritm.m:87
                    contactsVector[j + 3,i]=0.0
# ClosureAlgoritm.m:88
                else:
                    contactsVector[j,i]=matrix_normals_contactPointsIN.point[i](j)
# ClosureAlgoritm.m:90
                    contactsVector[j + 3,i]=matrix_normals_contactPointsIN.normal[i](j)
# ClosureAlgoritm.m:91
        #Quitar las columnas que tengan 0 ya que no nos interesan y almaceno el
	#vector con 0 para algun uso futuro
        columnas=matlabarray([])
# ClosureAlgoritm.m:98
        for i in arange(1,size(contactsVector,2)).reshape(-1):
            if contactsVector[1,i] == 0:
                columnas=matlabarray(cat(columnas,i))
# ClosureAlgoritm.m:101
        contactsVector[:,columnas]=[]
# ClosureAlgoritm.m:104
        str_postura_actual=orProblemSendCommand('getposture',umano_id)
# ClosureAlgoritm.m:107
        finalGraspPosture=Convert_str2mat(str_postura_actual,5,6)
# ClosureAlgoritm.m:108
    
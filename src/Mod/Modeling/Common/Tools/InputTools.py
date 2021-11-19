#-*- coding: utf-8 -*-
import FreeCAD
import re
import Modeling

# GlobalVariablelist=Modeling.Common.Tools.ModelingCommandForM3dFile.getGlobalVariable()
pi=3.14159265358979323846

def getNumberfromUnicode(string):
    # string="A1.45，b5，6.45，8.82"
    result=re.findall(r"\d+\.?\d*",string)
    return result
def isNumber(n):
    result=True
    try:
        num=float(n)
        result = num == num
    except :
        result=False
    return result
def Stringfunctions(str1):
    # FreeCAD.Console.PrintError('is test\n')
    str1=str1.replace(' ','')
    result=''
    real_result=[]
    if len(str1)==0:
        result='0'
        real_result=[float(result),0]
        return real_result
    if isNumber(str1):
        #该部分的功能应该为：
        #自动识别当前单位，并且都转换为米！！！
        # str1=str1.lower()
        #首先应转换为小写，在每次单位转换前，都应先转换为小写
        length=currentLengthUnits()
        if length=='mm':
            result=float(str1)*0.001
        elif length=='cm':
            result=float(str1)*0.01
        else :
            result=float(str1)
        real_result=[float(result),1]
        return real_result
    list1=re.split(r'([\+\-\/\*])',str1)
    # 添加小数点后补充数的功能
    for x_point in range(len(list1)):
        if isEndofdecimalpoint(list1[x_point]):
            list1[x_point]=isEndofdecimalpoint(list1[x_point])
    
    if len(list1)==1 and isValueWithUnits(list1[0]):
        # if Trigonometricjudgment(list1[0]):
        #     result = list1[0]
        #     real_result = [result,2]
        #     break
        try:
            result=float(lengthvalueChange(list1[0]))
        except:
            result='error'+str(list1[0])
        real_result=[result,1]
        # FreeCAD.Console.PrintError(real_result)
        return real_result
    if len(list1) == 3 and list1[1] == '-' and list1[0] == '':
        if isValueWithUnits(list1[2]):
            result = lengthvalueChange(list1[2])
            result = -result
            real_result = [result,1]
            return real_result
    for member in list1:
        if len(member)==0:
            pass
        elif isNumber(member):
            result=result+member
        elif isValueWithUnits(member):
            # FreeCAD.Console.PrintError('dai dan wei')
            member=member.lower()
            result=result+member
        elif haveOperator(member):
            result=result+member
        # 新添加的三角函数判断，还有待完善@lizhenguang
        elif Trigonometricjudgment(member):
            result = result + member
        elif haveVar(member):
            result=result+'Param.'+member
        else:
            FreeCAD.Console.PrintError(member+'is not exist')
            pass
    real_result=[result,2]
    FreeCAD.Console.PrintError(str(real_result))
    return real_result
    pass

def anglefunctions(str1):
    '''
    当涉及到角度的输入的时候，调用该函数
    '''
    str1=str1.replace(' ','')
    result=''
    real_result=[]
    if len(str1)==0:
        result='0'
        real_result=[float(result),0]
        return real_result
    if isNumber(str1):
        angle=currentAngleUnits()
        if angle=='deg':
            result=float(str1)
        if angle=='rad':
            result=float(str1)*180/pi
        real_result=[float(result),1]
        return real_result
    list1=re.split(r'([\+\-\/\*])',str1)
    # FreeCAD.Console.PrintMessage('\n'+str(list1))
    # 添加小数点后补充数的功能
    for x_point in range(len(list1)):
        if isEndofdecimalpoint(list1[x_point]):
            list1[x_point]=isEndofdecimalpoint(list1[x_point])
    if len(list1)==1 and isValueWithUnits(list1[0]):
        result=anglevalueChange(list1[0])
        real_result=[result,1]
        return real_result
    if len(list1) == 3 and list1[1] == '-' and list1[0] == '':
        if isValueWithUnits(list1[2]):
            result = anglevalueChange(list1[2])
            result = -result
            real_result = [result,1]
            return real_result
    for member in list1:
        if len(member)==0:
            pass
        elif isNumber(member):
            result=result+member
        elif isValueWithUnits(member):
            # FreeCAD.Console.PrintError('dai dan wei')
            member=member.lower()
            result=result+member
        elif haveOperator(member):
            result=result+member
        # 新添加的三角函数判断，还有待完善@lizhenguang
        elif Trigonometricjudgment(member):
            result = result + member
        elif haveVar(member):
            result=result+'Param.'+member
        else:
            FreeCAD.Console.PrintError(member+'is not exist')
            pass
    real_result=[result,2]
    # FreeCAD.Console.PrintError(real_result)
    return real_result

def isValueWithUnits(str1):
    '''
    必须传入字符串
    '''
    flag=False
    if isNumber(str1[0]):
        flag=True
    return flag
    pass

def haveOperator(str_1):
    '''
    判断是否含有字符串
    '''
    result=False
    if '+' in str_1:
        result=True
    if '-' in str_1:
        result=True
    if '*' in str_1:
        result=True
    if '/' in  str_1:
        result=True
    return result

def haveVar(str1):
    from Modeling.Common.Tools import BaseObjDialog
    flag = False
    GlobalVariablelist = Modeling.Common.Tools.ModelingCommandForM3dFile.getGlobalVariable()
    list_temp = GetWorkSpaceStepListInput()
    GlobalVariablelist.append(list_temp[0])
    GlobalVariablelist.append(list_temp[1])
    GlobalVariablelist.append(list_temp[2])
    for x in GlobalVariablelist:
        if str1 == x[0]:
            flag = True
    return flag

# 获取工作区的步长  
def GetWorkSpaceStepListInput():
    import ProjectSetting
    list_step = []
    step_list = ProjectSetting.Commands.ProjectSettingsDlgData.getDlgData()
    if not FreeCAD.ActiveDocument.CoordinateSystem =='Cylindrical':
        step_x_u = step_list[0][1][1][2]
        step_y_u = step_list[0][1][2][2]
        step_z_u = step_list[0][1][3][2]
        list_step.append(['DX1',step_x_u])
        list_step.append(['DX2',step_y_u])
        list_step.append(['DX3',step_z_u])
        return list_step
    else:
        step_x_u=step_list[4][1][1][2]
        step_y_u=step_list[4][1][2][2]
        step_z_u=step_list[4][1][3][2]
        list_step.append(['DX1',step_x_u])
        list_step.append(['DX2',step_y_u])
        list_step.append(['DX3',step_z_u])
        return list_step

def getGlobalVar():
    GlobalVariablelist=Modeling.Common.Tools.ModelingCommandForM3dFile.getGlobalVariable()
    list1=[]
    for x in GlobalVariablelist:
        list1.append(x[0])
    return list1


def currentLengthUnits():
    list1=FreeCAD.Units.getDefaultUnits()
    if list1[0]==0:
        length='mm'
    elif list1[0]==1:
        length='cm'
    else :
        length='m'
    return length

def currentAngleUnits():
    list1=FreeCAD.Units.getDefaultUnits()
    if list1[1]==0:
        angle='deg'
    elif list1[1]==1:
        angle='rad'
    return angle

def lengthvalueChange(num1):
    '''
    传入的参数应该是一个带单位的字符串
    使用时应该注意
    还函数已经带有转换小写的功能
    '''
    num1=num1.lower()
    if num1.endswith('mm'):
        num1=num1.replace('mm','')
        num1=float(num1)
        num1=num1*0.001
        return num1
    if num1.endswith('cm'):
        num1=num1.replace('cm','')
        num1=float(num1)
        num1=num1*0.01
        return num1
    if num1.endswith('m'):
        num1=num1.replace('m','')
        num1=float(num1)
        return num1

def anglevalueChange(num1):
    '''
    角度和弧度的转换
    '''
    # pi=3.14159265358979323846
    #pi的定义已经放在最前面
    num1=num1.lower()
    if num1.endswith('rad'):
        num1=num1.replace('rad','')
        num1=float(num1)*180/pi
        return num1
    if num1.endswith('deg'):
        num1=num1.replace('deg','')
        num1=float(num1)
        return num1
def textChangedbefore(line_1,line_2,line_3):
    text1 = line_1.text()
    text2 = line_2.text()
    text3 = line_3.text()

    line_1.setText(text3)
    line_2.setText(text1)
    line_3.setText(text2)

def textChangedafter(line_1,line_2,line_3):
    text1 = line_1.text()
    text2 = line_2.text()
    text3 = line_3.text()
    
    line_1.setText(text2)
    line_2.setText(text3)
    line_3.setText(text1)

def isEndofdecimalpoint(num1):
    if num1.endswith('.'):
        temp_num = num1.replace('.','')
        if isNumber(temp_num):
            num1 = num1+'0'
            return num1
    if num1.endswith('.mm'):
        temp_num = num1.replace('.mm','')
        if isNumber(temp_num):
            num1 = temp_num+'.0mm'
            return num1
    if num1.endswith('.m'):
        temp_num = num1.replace('.m','')
        if isNumber(temp_num):
            num1 = temp_num+'.0m'
            return num1
    if num1.endswith('.cm'):
        temp_num = num1.replace('.cm','')
        if isNumber(temp_num):
            num1 = temp_num+'.0cm'
            return num1
    if num1.endswith('.deg'):
        temp_num = num1.replace('.deg','')
        if isNumber(temp_num):
            num1 = temp_num+'.0deg'
            return num1
    if num1.endswith('.rad'):
        temp_num = num1.replace('.rad','')
        if isNumber(temp_num):
            num1 = temp_num+'.0rad'
            return num1
    pass
# def endwithpointandunits(num2,units):
#     if num2.endswith('.mm'):
#         temp_num = num2.replace('.mm','')
#         if isNumber(temp_num):
#             num2 = temp_num+'0'
#             return num2
def Trigonometricjudgment(num1):
    if num1.startswith('sin('):
        return True
    elif num1.startswith('cos('):
        return True
    elif num1.startswith('tan('):
        return True
    elif num1.startswith('arctan('):
        return True
    return False








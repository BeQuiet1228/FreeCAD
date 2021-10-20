# -*- coding: utf-8 -*-
import FreeCAD
import re


def processingLengthExpression(expression):
    """
    对传入的表达式做处理，输入的表达式是符合用户习惯的，输出的表达式是符合FreeCAD表达式引擎要求的
    :param expression:用户输入的表达式
    :return:符合FreeCAD表达式引擎要求的表达式
    """
    # 符号表
    operators = ["+", "-", "*", "/", "^", "(", ")", ":", ","]
    # 数学表达式表
    mathSymbol = ["e", "pi",
                  "acos", "asin", "atan", "atan2", "cos", "cosh", "sin", "sinh", "tan", "tanh",
                  "exp", "log", "log10", "pow", "sqrt",
                  "abs", "ceil", "floor", "mod", "round", "trunc",
                  "average", "count", "max", "min", "stddev", "sum"]
    # 当前默认长度单位
    length = currentLengthUnits()

    expression = expression.replace(" ", "")
    exp_list = re.split(r'([+\-/*()^,:])', expression)
    result_list = []

    for i in exp_list:
        # i的长度不为0，且全部为空格
        if i.isspace():
            continue
        # i为空或i为符号或关键词
        if (len(i) == 0) or (i in operators) or (i in mathSymbol):
            pass
        # i为纯数字
        elif i.isdigit():
            # 无法判断纯数字是用作长度还是倍数所以在这里不再处理
            # i = i + length      # 拼接默认单位
            pass
        # i开头为数字
        elif i[0].isdigit():
            pass
        # i是以字母开头的非关键词
        else:
            i = "Param." + i
        result_list.append(i)

    result = ""     # 返回值
    for i in result_list:
        result += i

    return result


def processingAngleExpression():
    pass


def currentLengthUnits():
    temp_list = FreeCAD.Units.getDefaultUnits()
    if temp_list[0] == 0:
        length = 'mm'
    elif temp_list[0] == 1:
        length = 'cm'
    else:
        length = 'm'
    return length


# def lengthUnitConversion(numWithUnit):
#     """
#     长度单位转换
#     :param numWithUnit: 带单位的长度字符串
#     :return: 默认单位的长度字符串
#     """
#     temp_num = numWithUnit.lower()
#     if isLegal(numWithUnit) is None:
#         return numWithUnit
#
#     if temp_num.endswith('mm'):
#         temp_num = temp_num.replace('mm', '')
#         if temp_num.isdigit():
#             temp_num = float(temp_num)
#             temp_num = temp_num*0.001
#
#     elif temp_num.endswith('cm'):
#         temp_num = temp_num.replace('cm', '')
#         temp_num = float(temp_num)
#         temp_num = temp_num*0.01
#
#     elif temp_num.endswith('m'):
#         temp_num = temp_num.replace('m', '')
#         temp_num = float(temp_num)
#
#     return temp_num


def isLegal(numWithUnit):
    """
    检查当前字符串是否符带单位数字的规范
    :param numWithUnit:
    :return: False or True
    """
    return re.match(r'^[-+]?[0-9]*\.?[0-9]+(mm|cm|dm|m)?$', numWithUnit, re.I)

#pragma once
#include <QString>
//GBK编码的std::string转换为qstring
QString gbkStdstringToQstring(const std::string& str);
//UTF-8编码的std::string 转GBK std::string
std::string utf8StdstringToGbkStdstring(const std::string& str);
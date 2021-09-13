#pragma once
#include <QString>
//GBK编码的std::string转换为qstring
static QString gbkStdstringToQstring(const std::string& str);
//UTF-8编码的std::string 转GBK std::string
static std::string utf8StdstringToGbkStdstring(const std::string& str);
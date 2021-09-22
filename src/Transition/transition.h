#pragma once
#ifdef _TRANSITION_
#define TANSITION_API extern "C" _declspec(dllexport)
#else
#define TANSITION_API extern "C" _declspec(dllexport)
#endif // _TANSITION_

#include <QString>

//GBK编码的std::string转换为qstring
TANSITION_API QString gbkStdstringToQstring(const std::string& str);
//UTF-8编码的std::string 转GBK std::string
TANSITION_API std::string utf8StdstringToGbkStdstring(const std::string& str);
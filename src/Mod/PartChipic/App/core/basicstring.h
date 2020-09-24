#ifndef _PM3_BASIC_STRING_H
#define _PM3_BASIC_STRING_H
#include <string>
//#include <algorithm>
#include <string>
#include <vector>
namespace PM3
{
void deSpace(std::string &in);
std::string getOutOBJName(std::string in);
std::string QStringToStdString(std::string ref);
std::string StdStringToQString(std::string ref);
//std::string& replace_str(std::string& str, const std::string& to_replaced, const std::string& newchars);
std::string replace_str(std::string &strBig, const std::string &strsrc, const std::string &strdst);
std::string getStringFromFloat(float f);

std::vector<std::string> split(std::string strtem, char a);

std::string convertToString(int x);

std::string convertToStringd(double x);

}

#endif

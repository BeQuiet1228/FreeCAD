#ifndef GUI_ABOUTPARAMETER_H
#define GUI_ABOUTMYPARAMETER_H

#include <string>
#include <vector>
#include <regex>

// 全字匹配，查看target里面是否有base
bool findWholeWordsOnly(const std::string& target, const std::string& base);

// 1. 查找变量param_name与其他变量之间的联系，或者说查找哪些变量调用了param_name
// 2. 错误信息会写到error
std::vector<std::string> findLinkWithParam(const std::string& param_name, std::vector<std::pair<std::string, std::string>> all_ordered_param, std::string& error);

// 1. 查找变量列表param_names与当前工程中体的联系，或者说查找哪些体调用了这些变量
// 2. 错误信息会写到error
std::vector<std::string> findLinkWithObject(const std::vector<std::string>& param_names, std::string& error);

#endif	// GUI_ABOUTMYPARAMETER_H
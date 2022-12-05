#include "PreCompiled.h"
#include <App/Document.h>
#include <App/Application.h>
#include <App/DocumentObject.h>
#include <APP/PropertyExpressionEngine.h>
#include <unordered_map>

#include "AboutParameter.h"

using namespace App;

std::vector<std::string> findLinkWithParam(const std::string& param_name, std::vector<std::pair<std::string, std::string>> all_ordered_param, std::string& error) {
	// 报错信息待完善
	std::vector<std::string> all_changed_name;
	all_changed_name.push_back(param_name);
	error.clear();
	if (param_name.empty()) {
		error = "error";
		return all_changed_name;
	}
	for (auto it = all_ordered_param.begin(); it != all_ordered_param.end(); ++it) {
		for (const auto& i : all_changed_name) {
			if (it->first == i) {
				continue;
			}
			else if (findWholeWordsOnly(it->second, i)) {
				//it->second == "wang";
				all_changed_name.push_back(it->first);
				break;
			}
		}
	}
	//for (auto ii : all_changed_name) {
	//	std::cerr << "changed param:\t" << ii << std::endl;
	//}
	return all_changed_name;
}

std::vector<std::string> findLinkWithObject(const std::vector<std::string>& param_names, std::string& error) {
	std::vector<std::string> res;
	DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("Param");
	if (param_names.empty() || docObj == nullptr) {
		error = "error";
		return res;
	}
	std::vector<App::DocumentObject*> temp_v = docObj->getInList();
	// 该循环是所有使用Param的体(object)
  	for (const auto& i : temp_v) {
		boost::unordered_map<const ObjectIdentifier, const PropertyExpressionEngine::ExpressionInfo> pee =
			i->ExpressionEngine.getExpressions();
		// 该循环是该object所有的表达式
		for (auto it = pee.begin(); it != pee.end(); ++it) {
			// 该循环是查询obj的表达式是否使用了param_names里面的变量
			bool flag_to_break = false;
			for (const auto& j : param_names) {
				if (findWholeWordsOnly(it->second.expression->toString(), j)) {
					res.push_back(std::string(i->Label.getValue()));
					flag_to_break = true;
					break;
				}
			}
			if (flag_to_break) {
				break;
			}
		}
	}
	//boost::unordered_map<const ObjectIdentifier, const PropertyExpressionEngine::ExpressionInfo> pee =
	//	docObj->ExpressionEngine.getExpressions();
	//std::unordered_map<std::string, std::string> param_dict;
	//for (auto it = pee.begin(); it != pee.end(); ++it) {
	//	param_dict.insert(std::unordered_map<std::string, std::string>::value_type(it->first.toString(), it->second.expression->toString()));
	//}
	//for (auto i : res) {
	//	std::cerr << i << "\t";
	//}
	return res;
}

bool findWholeWordsOnly(const std::string& target, const std::string& base) {
	std::string base_s("\\b" + base + "\\b");
	std::regex base_r(base_s);
	return std::regex_search(target, base_r);
}
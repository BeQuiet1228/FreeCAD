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
	std::string param_name = "a1";
	if (param_name.empty() || docObj == nullptr) {
		error = "error";
		return res;
	}
	std::vector<App::DocumentObject*> temp_v = docObj->getInList();
	for (const auto& i : temp_v) {
		boost::unordered_map<const ObjectIdentifier, const PropertyExpressionEngine::ExpressionInfo> pee =
			i->ExpressionEngine.getExpressions();
		for (auto it = pee.begin(); it != pee.end(); ++it) {
			if (findWholeWordsOnly(it->second.expression->toString(), param_name)) {
				std::cerr << i->Label.getValue() << std::endl;
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
	return res;
}

bool findWholeWordsOnly(const std::string& target, const std::string& base) {
	std::string base_s("\\b" + base + "\\b");
	std::regex base_r(base_s);
	return std::regex_search(target, base_r);
}
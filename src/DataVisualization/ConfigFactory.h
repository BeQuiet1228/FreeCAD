#pragma once
#include "vector"
//#include "QWidget"
class QWidget;
#include "exportConfig.hpp"
namespace DV
{
	class DATA_VISUALIZATION_EXPORT ConfigPageFactory
	{
	public :
		ConfigPageFactory() = default;
		~ConfigPageFactory() = default;
	public:
		static std::vector<QWidget*>  CreateConfigWidget();
	};
}
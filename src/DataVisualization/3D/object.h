#pragma once
#include <string>
#include "DataVisualization3DExport.hpp"
namespace DV3D {
	class DATA_VISUALIZATION_3D_EXPORT Object {
	public:
		Object();
		virtual ~Object();

	private:
		std::string name;

	public:
		std::string getObjectName();
		void setObjectName(const std::string& name);

	};
}
#pragma once
#include <string>
namespace DV3D {
	class Object {
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
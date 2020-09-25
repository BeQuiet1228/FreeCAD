#include <windows.h>
#include <stdio.h>
#include "PM3VFunctional.h"
/*#include "CJsonObject.hpp"
#include "DefValue.h"
std::string readTxt(string file)
{
	ifstream ifs;
	cout << file << endl;
	ifs.open(file);   			//将文件流对象与文件关联起来，如果已经关联则调用失败
	assert(ifs.is_open());   	//若失败,则输出错误消息,并终止程序运行

	string s, re;
	while (getline(ifs, s))		//行分隔符可以显示指定，比如按照分号分隔getline(infile,s,';')
	{
		cout << s << endl;
		re += s;
	}
	ifs.close();             	//关闭文件输入流 

	return re;
}*/

int mainx(int argc, const char *argv[])
{
	/*TCHAR dest[MAX_PATH * 3];
	if (SUCCEEDED(SHGetFolderPathW(NULL, CSIDL_PERSONAL, NULL, 0, szPath))) {
		WideCharToMultiByte(CP_UTF8, 0, szPath, -1, dest, 256, NULL, NULL);
		mConfig["UserHomePath"] = dest;
	}*/
/*	std::string jsonfile = "C:\\Users\\211904\\AppData\\Roaming\\FreeCAD\\tempFunc.json";
	if (argc > 1)
		jsonfile = argv[1];
	std::string json = readTxt(jsonfile);// ();
	std::string strValue;
	neb::CJsonObject oJson(json);
	neb::CJsonObject isoJson = oJson["MathModels"][0]["Iso3D"];
	std::cout << oJson.ToString() << std::endl;
	std::cout << isoJson.ToString() << std::endl;
	std::string Fxyz; isoJson["Fxyz"].Get(0, Fxyz);
	std::string Xmax; isoJson["Xmax"].Get(0, Xmax);
	std::string Xmin; isoJson["Xmin"].Get(0, Xmin);
	std::string Ymax; isoJson["Ymax"].Get(0, Ymax);
	std::string Ymin; isoJson["Ymin"].Get(0, Ymin);
	std::string Zmax; isoJson["Zmax"].Get(0, Zmax);
	std::string Zmin; isoJson["Zmin"].Get(0, Zmin);
	
	std::cout << "Fxyz:" << Fxyz << std::endl;
	std::cout << "Xmax:" << Xmax << std::endl;
	std::cout << "Xmin:" << Xmin << std::endl;
	std::cout << "Ymax:" << Ymax << std::endl;
	std::cout << "Ymin:" << Ymin << std::endl;
	std::cout << "Zmax:" << Zmax << std::endl;
	std::cout << "Zmin:" << Zmin << std::endl;*/
	PM3::VFunctional func;
	//func.f = Fxyz;
	//PM3::DefValue3D max, min;
	//func.far_point.setValue(Xmax + "," + Ymax + "," + Zmax);
	//func.near_point.setValue(Xmin + "," + Ymin + "," + Zmin);

	PM3::ExpParser exparser;
	func.pexparser = &exparser;
//	func.update_mesh_topology();
	
		//func.saveOBJ(PM3::getOutOBJName(jsonfile));
	printf("hello\n");

	return 1;
}

#include "PreCompiled.h"
#include "TreeNode2D.h"
#include "sstream"
#include "qstring.h"
namespace Gui
{
#ifndef MAX_TYPE_NUMBER
#define  MAX_TYPE_NUMBER 7
#endif
	enum emType
	{
		CONTOUR = 0,
		PHASEPACE,
		RANGE,
		VECTOR,
		STRUCT,
		OBSERVE,
		PLANE,
	};
	struct TypeStr
	{
		std::string nameStr;
		std::string typeStr;
	};
	const TypeStr TypeStrList[MAX_TYPE_NUMBER] = {
		{
			"CONTOUR",
			"等位图"
		},
		{
			"PHASESPACE",
			"相空间图"
		},
		{
			"RANGE",
			"空间变化图"
		},
		{
			"VECTOR",
			"矢量图"
		},
		{
			"struct" ,
			"结构图"
		},
		{
			"OBSERVE",
			"时间图"
		},
		{
			"PLANE",
			"三维结构图"
		}
	};
	std::string Structdirection[3] = { "Phi-Z",
"Z-R",
"R*cos(Phi)-R*sin(Phi)" };
	std::string Structdirection_cartesian[3] = { "X_Y", "Y_Z", "X_Z" };
	TreeNode2D::TreeNode2D() {
	}
	TreeNode2D::~TreeNode2D() {

	}
	TreeNode* TreeNode2D::createNodeInfo(Hdf5Data& data, int index) {
		if (data.name.find("struct") != std::string::npos) {
			return toStructNode(data, index);
		}
		else if (data.name.find("PLANE") != std::string::npos) {
			return nullptr;
		}
		else {
			//其他图
			return toOtherNode(data, index);
		}
	}
	TreeNode* TreeNode2D::createNodeInfo(std::vector<Hdf5Data>& hdf5dataList) {
		return nullptr;
	}
	std::string TreeNode2D::getType(std::string name)
	{
		for (auto i = 0; i < MAX_TYPE_NUMBER; i++)
		{
			if (name.find(TypeStrList[i].nameStr) != std::string::npos)
			{
				return TypeStrList[i].typeStr;
			}
		}
		return "未知图";
	}
	TreeNode* TreeNode2D::toStructNode(Hdf5Data& data, int index, TreeNode* node)
	{
		if (node == nullptr)
			node = new TreeNode;
		NodeInfo mNodeInfo;
		mNodeInfo.index = index;
		if (data.name.find("struct") == std::string::npos)
			return nullptr;
		std::string dataType = getType(data.name);
		node->initNode(dataType, TreeNodeType::TREENODE_FOLDER);
		//判断是2维的还是3维的
		if (data.listDataSet.size() > 3)
		{
			switch (data.coordinateSystem)
			{
			case Hdf5Data::CARTESIAN:
			{
				for each (std::string var in Structdirection_cartesian)
				{
					TreeNode* subNode = new TreeNode;
					subNode->initNode(var, TreeNodeType::TREENODE_FILE, index);
					node->addChild(subNode);
				}
			}
			break;
			case Hdf5Data::POLAR:
			case Hdf5Data::CYLINDER:
			{
				for each (std::string var in Structdirection)
				{
					TreeNode* subNode = new TreeNode;
					subNode->initNode(var, TreeNodeType::TREENODE_FILE, index);
					node->addChild(subNode);
				}
			}
			break;
			}
		}
		else
		{
			std::string structstr = *(data.headList.begin() + 2);
			structstr.erase(std::remove_if(structstr.begin(), structstr.end(), isspace), structstr.end());
			int _j = structstr.find("=");
			structstr.erase(0, _j + 1);
			int pos1 = structstr.find("$");
			int pos2 = structstr.find("$", pos1 + 1);
			structstr = structstr.substr(pos1 + 1, pos2 - pos1 - 1);
			TreeNode* subNode = new TreeNode;
			subNode->initNode(structstr, TreeNodeType::TREENODE_FILE, index);
			node->addChild(subNode);
		}
		return node;
	}
	TreeNode* TreeNode2D::toOtherNode(Hdf5Data& data, int index, TreeNode* node)
	{
		if (node == nullptr)
			node = new TreeNode;
		std::string datatype = getType(data.name);
		//若是未知的图不做处理
		if (datatype.find("未知图") != std::string::npos)
			return nullptr;
		node->initNode(datatype, TreeNodeType::TREENODE_FOLDER);

		NodeInfo mNodeInfo;
		mNodeInfo.index = index;
		//获取观测面
		int _type = -1;
		for (auto i = 0; i < MAX_TYPE_NUMBER; i++)
		{
			if (data.name.find(TypeStrList[i].nameStr) != std::string::npos)
			{
				_type = i;
				break;
			}
		}
		std::stringstream ss;
		std::stringstream subss;
		auto getSStr = [&](std::string str)->std::string {
			std::string res;
			res = str;
			//res.erase(std::remove_if(res.begin(),res.end(),isspace),res.end());
			int pos = res.find("=");
			res.erase(0, pos + 1);
			QString qres = QString::fromStdString(res);
			qres = qres.simplified();
			//qres=qres.replace(" ","_");
			return qres.toStdString();
		};
		auto replaceStr = [&](std::string str)->std::string
		{
			QString qstr = QString::fromStdString(str);
			qstr = qstr.simplified();
			QString qregexp =QString::fromStdString("\\s{1,}");
			QString qregexp2 = QString::fromStdString("_");
			qstr = qstr.replace(qregexp, qregexp2);
			return qstr.toStdString();
		};
		//字符串拼接
		switch (_type)
		{
		case emType::VECTOR:
		{
			std::string art3 = getSStr(data.headList[2]);
			std::string art14 = getSStr(data.headList[13]);
			std::string art12 = getSStr(data.headList[11]);
			{
				art12.erase(0, art12.find("("));
				art3.erase(0, art3.find("$") + 1);
				art14.erase(0, art14.find("TIME:") + 5);
			}
			ss << "PLOT" << art12;
			subss << art3 << " " << art14;
			{
				//获取时间
				std::string mt = art14;
				mNodeInfo.time = QString::fromStdString(mt.erase(mt.find("SEC"), mt.size())).toDouble();
			}
		}
		break;
		case emType::CONTOUR:
		{
			//等位图
			std::string art3 = getSStr(data.headList[2]);
			//std::string art3=std::remove_space
			ss << art3.substr(0, art3.find("-#"));
			std::string art13 = getSStr(data.headList[12]);
			{
				art3.erase(0, art3.find("$") + 1);
				art13.erase(0, art13.find("TIME") + 4);
			}
			//测试
			subss << art3 << " " << art13;
			{
				//保存时间
				std::string mt = art13;
				mNodeInfo.time = QString::fromStdString(mt.erase(mt.find("SEC"), mt.size())).toDouble();
			}
		}
		break;
		case emType::PHASEPACE:
		{
			//相空间图
			//ss << getSStr(data.headList[2]);
			std::string art3 = getSStr(data.headList[2]);
			art3.erase(art3.find("-#"), art3.size());
			ss << art3;
			//观测对象
			art3 = getSStr(data.headList[2]);
			//观测时刻
			std::string art12 = getSStr(data.headList[11]);
			{
				//获取时间
				std::string mt = art12;
				mt.erase(0, mt.find("TIME:") + 5);
				mt.erase(mt.find("SEC"), mt.size());
				mNodeInfo.time = QString::fromStdString(mt).toDouble();
			}
			{
				int pos = art3.find("$");
				art3 = (pos == std::string::npos) ? ("") : (art3.erase(0, art3.find("$") + 1));
				{
					std::stringstream s1;
					s1 << art12.substr(art12.find("OF") + 2, (art12.find("VS") - (art12.find("OF") + 2)))
						<< " " << art12.substr(art12.find("VS") + 2, (art12.find("AT") - (art12.find("VS") + 2)));
					s1 << " " << art12.substr(art12.find("TIME") + 5, (art12.size() - (art12.find("TIME") + 5)));
					art12 = s1.str();
				}
				//art12.erase(0, art12.find("TIME"));
			}
			subss << art3 << " " << art12;
		}
		break;
		case emType::RANGE:
		{
			std::string art3 = getSStr(data.headList[2]);
			art3.erase(art3.find("-#"), art3.size());
			ss << art3;
			//观测类型
			std::string art14 = data.headList[13];
			//观测对象
			art3 = getSStr(data.headList[2]);
			//观测时刻
			std::string art12 = getSStr(data.headList[11]);
			{
				art14.erase(0, art14.find("=") + 1);
				art14.erase(art14.find(" "), art14.size());
				art3.erase(0, art3.find("$") + 1);
				art12.erase(0, art12.find("TIME") + 5);
			}
			subss << art14 << " " << art3 << " " << art12;
			{
				std::string mt = art12;
				mNodeInfo.time = QString::fromStdString(mt.erase(mt.find("SEC"), mt.size())).toDouble();
			}
		}
		break;
		case emType::OBSERVE:
		{
			std::string art3 = getSStr(data.headList[2]);
			art3.erase(art3.find("-#"), art3.size());
			ss << art3;
			std::string art14 = getSStr(data.headList[13]);
			{
				transform(art14.begin(), art14.end(), art14.begin(), toupper);
				int pos = 0;
				while (std::string::npos != (pos = art14.find("MAGINTUDE"))) art14.erase(pos, 9);
				while (std::string::npos != (pos = art14.find("OF"))) art14.erase(pos, 2);
				while (std::string::npos != (pos = art14.find("COMPONENT"))) art14.erase(pos, 9);

			}
			art3 = getSStr(data.headList[2]);
			art3.erase(0, art3.find("$") + 1);
			subss << art14 << " " << art3;
		}
		break;
		}
		//子节点下分类字符串
		TreeNode* node1 = new TreeNode(replaceStr(ss.str()), TreeNodeType::TREENODE_FOLDER);
		TreeNode* node2 = new TreeNode(replaceStr(subss.str()),TreeNodeType::TREENODE_FILE,index);
		node->addChild(node1);
		node1->addChild(node2);
		node2->nodeInfo=mNodeInfo;
		return node;
	}
};
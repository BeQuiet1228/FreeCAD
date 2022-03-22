#pragma once
#include "TreeNode.h"
namespace Gui
{
class TreeNodeManager
{
public:
	~TreeNodeManager();
	static TreeNodeManager* GetInstance();
	TreeNode createNodeInfo2D(Hdf5Data& data, int index);
	TreeNode createNodeInfo3D(Hdf5Data& data, int index);
private:
	TreeNode toStructNode(Hdf5Data& data, int index);
	TreeNode toOtherNode(Hdf5Data& data, int index);
	std::string getType(std::string name);
private:
	TreeNodeManager();
};
};

#pragma once
#include "TreeNode.h"
namespace Gui
{
class TreeNode2D
{
public:
	TreeNode2D();
	~TreeNode2D();
	TreeNode* createNodeInfo(Hdf5Data& data, int index);
	TreeNode* createNodeInfo(std::vector<Hdf5Data>& hdf5dataList);
private:
	TreeNode* toStructNode(Hdf5Data& data, int index, TreeNode* node = nullptr);
	TreeNode* toOtherNode(Hdf5Data& data, int index, TreeNode* node = nullptr);
	std::string getType(std::string name);
};
};

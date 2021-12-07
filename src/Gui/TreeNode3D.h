#pragma once
#include "TreeNode.h"
namespace Gui
{
	class TreeNode3D
	{
	public:
		TreeNode3D();
		~TreeNode3D();
		TreeNode* createNodeInfo(Hdf5Data& data, int index);
		TreeNode* createNodeInfo(std::vector<Hdf5Data>& hdf5dataList);
	};
};

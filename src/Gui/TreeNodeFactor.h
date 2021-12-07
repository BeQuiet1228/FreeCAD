#pragma once
#include "TreeNode.h"
#include "TreeNode2D.h"
#include "TreeNode3D.h"
namespace Gui
{
	class TreeNodeFactor
	{
	public:
		static TreeNodeFactor* GetInstance();
		~TreeNodeFactor();
		TreeNode* createTreeNode2D(Hdf5Data& data, int index);
		TreeNode* createTreeNode2D(std::vector<Hdf5Data>& hdf5dataList);
		TreeNode* createTreeNode3D(Hdf5Data& data, int index);
		TreeNode* createTreeNode3D(std::vector<Hdf5Data>& hdf5dataList);
	private:
		TreeNodeFactor();
	private:
		TreeNode2D mTreeNode2D;
		TreeNode3D mTreeNode3D;
	};
};

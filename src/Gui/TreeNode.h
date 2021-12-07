#pragma once
#ifndef TREE_NODE_H_
#define TREE_NODE_H_
#include "string"
#include "vector"
#include "HDF5Reader/hdf5io.h"
namespace Gui
{
	enum TreeNodeType
	{
		TREENODE_FOLDER = 0,
		TREENODE_FILE,
		TREENODE_NULL,
	};
	struct  NodeInfo
	{
		int index;
		double time;
	};
	struct TreeNode
	{
		std::string nodeStr;
		std::vector<TreeNode*> childNode;//子字节 
		TreeNodeType mTreeNodeType;//节点类型
		int index;//需要的h5索引
		NodeInfo nodeInfo;//
		TreeNode();
		TreeNode(std::string text, TreeNodeType type, int _index = -1);
		~TreeNode();
		std::vector<TreeNode*> Childs();
		int getChilds();
		void addChild(TreeNode* child);
		void initNode(std::string text, TreeNodeType type, int index = -1);
	};
}

#endif
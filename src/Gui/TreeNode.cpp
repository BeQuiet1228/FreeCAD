#include "PreCompiled.h"
#include "TreeNode.h"
namespace Gui
{
	TreeNode::TreeNode()
	{
		nodeStr = "";
		childNode.clear();
		mTreeNodeType = TREENODE_NULL;
	}
	void TreeNode::addChild(TreeNode child)
	{
		this->childNode.push_back(child);
	}
	void TreeNode::initNode(std::string text, TreeNodeType type, int index)
	{
		this->nodeStr = text;
		this->mTreeNodeType = type;
		this->index = index;
	}
	TreeNode::TreeNode(std::string text, TreeNodeType type, int _index):
		nodeStr(text),mTreeNodeType(type),index(_index)
	{}
	TreeNode::~TreeNode()
	{
		childNode.clear();
	}
};
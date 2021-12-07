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
	int TreeNode::getChilds(){
		return childNode.size();
	}
	std::vector<TreeNode*> TreeNode::Childs()
	{
		return childNode;//×Ó×Ö½Ú 
	}
	void TreeNode::addChild(TreeNode* child)
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
		for (int i = childNode.size()-1; i >=0; --i)
		{
			delete childNode[i];
		}
		childNode.clear();
	}
};
#include "PreCompiled.h"
#include "TreeNodeFactor.h"
namespace Gui
{
	TreeNodeFactor* TreeNodeFactor::GetInstance(){
		static TreeNodeFactor instancce;
		return &instancce;
	}
	TreeNodeFactor::~TreeNodeFactor(){

	}
	TreeNode* TreeNodeFactor::createTreeNode2D(Hdf5Data& data, int index) {
		return mTreeNode2D.createNodeInfo(data, index);
	}
	TreeNode* TreeNodeFactor::createTreeNode2D(std::vector<Hdf5Data>& hdf5dataList) {
		return mTreeNode2D.createNodeInfo(hdf5dataList);
	}
	TreeNode* TreeNodeFactor::createTreeNode3D(Hdf5Data& data, int index) {
		return nullptr;
	}
	TreeNode* TreeNodeFactor::createTreeNode3D(std::vector<Hdf5Data>& hdf5dataList){
		return nullptr;
	}
	TreeNodeFactor::TreeNodeFactor(){
		
	}
}
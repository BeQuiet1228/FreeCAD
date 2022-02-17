#include "UndoRedoStack.h"

DV::UndoRedoData::UndoRedoData(const Data::Rang& xr, const Data::Rang& yr)
	:xr(xr),yr(yr)
{

}

void DV::UndoRedoData::printTmp() {

}

/**
* @brief UndoRedoStack::undo 撤销之前的操作
* @param DataPtr data 返回渲染范围
* @return bool false 代表操作失败
*/
bool DV::UndoRedoStack::undo(DataPtr& data) {
	if (undoStack.size() < 2)
		return false;
	redoStack.push(undoStack.top());
	undoStack.pop();
	data = undoStack.top();

};

/**
* @brief UndoRedoStack::redo 恢复之前的撤销
* @param DataPtr & data 返回渲染数据
* @return bool false 代表操作失败
*/
bool DV::UndoRedoStack::redo(DataPtr& data)
{
	if (redoStack.empty())
		return false;
	data = redoStack.top();
	undoStack.push(data);
	redoStack.pop();
}
/**
* @brief UndoRedoStack::push 压入操作，如放大缩小操作的数据
* @param const UndoRedoData & data
* @return void
*/
void DV::UndoRedoStack::push(DataPtr data)
{
	undoStack.push(data);
	clearStack(redoStack);
}

/**
* @brief DV::UndoRedoStack::clear 清理数据
* @return void
*/
void DV::UndoRedoStack::clear()
{
	clearStack(redoStack);
	clearStack(undoStack);
}

void DV::UndoRedoStack::clearStack(DataStack& stack)
{
	while (!stack.empty())
	{
		stack.pop();
	}
}


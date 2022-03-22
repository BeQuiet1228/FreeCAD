#pragma once
#include "Data.h"
#include <stack>
#include <memory>
namespace DV {
	class UndoRedoData
	{
	public:
		UndoRedoData(const Data::Rang& xr, const Data::Rang& yr);
		UndoRedoData() = default;
		Data::Rang xr, yr;
		virtual void printTmp();//保证其安全的动态转换，预留一个虚函数表
	};

	class UndoRedoStack {
	public:
		using DataPtr = std::shared_ptr<UndoRedoData>;
		using DataStack = std::stack<DataPtr>;
	public:
		UndoRedoStack() = default;
		~UndoRedoStack() = default;


		bool undo(DataPtr& data);
		bool redo(DataPtr& data);
		void push(DataPtr data);
		void clear();
	private:
		DataStack undoStack, redoStack;
	private:
		void clearStack(DataStack& stack);//添加引用，彻底清空stack
	};
}
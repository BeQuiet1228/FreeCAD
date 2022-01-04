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
		void clearStack(DataStack stack);
	};
}
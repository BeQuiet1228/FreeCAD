#pragma  once
#include "codeeditor.h"
#include "EditorExportConfig.hpp"
#include <QString>
#include <list>
#include <QRegExp>
struct EDITOR_EXPORT M3dLine
{
	QString str;		//文本
	unsigned int num;	//行号
};
class EDITOR_EXPORT M3dCommandType {
public:
	M3dCommandType(const QString& w);
public:
	QRegExp regx;
	QString word;
};
class EDITOR_EXPORT M3dCommand
{
public:
	M3dCommand() = default;
	~M3dCommand() = default;
public:
	QString cmd;	//命令
	QString text;
	std::list<M3dLine> lines;
public:
	void clear();
	QString simplified();
	bool initCmdType(std::list<M3dCommandType> types);
};
using Cmds = std::list<M3dCommand>;
class EDITOR_EXPORT M3dCommadAnalysis {
public:
	M3dCommadAnalysis();
	~M3dCommadAnalysis() = default;
public:
	void setText(const QString& t) {
		this->text = t;
	}
	Cmds analysisText();
private:
	QString text;	//分割文本
	std::list<M3dCommandType> types;
private:
	//将整个文本切割为一条一条的命令
	Cmds slicingCmd();
};
class EDITOR_EXPORT M3dEditor :public CodeEditor {
public:
	M3dEditor(QWidget* parent = 0);
	~M3dEditor();

	Cmds getCmds();
private:
	M3dCommadAnalysis analysis;
};
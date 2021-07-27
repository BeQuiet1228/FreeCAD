#pragma once
#ifndef SMARTDIALOG_H_
#define SMARTDIALOG_H_
#include"VariateInputDialog.h"
class smartDialog :public VariateInputDialog
{
	Q_OBJECT
public:
	smartDialog(QWidget* parent = nullptr);
	~smartDialog();
};
#endif // !SMARTDIALOG_H_

#pragma once
#include <QWidget>

class QLineEdit;
class QToolButton;

namespace OriginUI {
	enum InputLineEditLayoutMod {
		BUTTON_LEFT = 0,		//按钮在左边		
		BUTTON_RIGHT		//按钮在右边
	};

	class InputLineEditD;
	class InputLineEdit:public QWidget {
		Q_OBJECT
	public:
		InputLineEdit(QWidget *parent = 0);
		~InputLineEdit();

		//设置布局mod
		void setButtonLaoutMod(const InputLineEditLayoutMod& mod);
		InputLineEditLayoutMod getButtonLaoutMod();

		//设置按钮图标
		void setOkIcon(QIcon icon);
		void setCancelIcon(QIcon icon);

		//获取按钮指针
		QToolButton* getOkButton();
		QToolButton* getCancelButton();
		//获取编辑器
		QLineEdit* getLineEdit();
	public Q_SLOTS:
		void textChanged(const QString& text);
	protected:
		void paintEvent(QPaintEvent* event);
		void keyPressEvent(QKeyEvent* event);
	private:
		InputLineEditD* d;

	};

}
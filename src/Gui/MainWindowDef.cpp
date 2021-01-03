#include "PreCompiled.h"
#include "MainWindowDef.h"
#include "ui_MainWindowDef.h"
#include <QToolBar>
#include <QAction>
#include <QApplication>
TitleBar::TitleBar(QWidget* parent /*= 0*/)
	:QWidget(parent)
{

}

void TitleBar::mouseMoveEvent(QMouseEvent *event)
{
	QWidget::mouseMoveEvent(event);
	if (mouseIsPress)
		Q_EMIT toMove(event->pos() - mouseStartPoint);
}

void TitleBar::mousePressEvent(QMouseEvent *event)
{
	QWidget::mousePressEvent(event);
	if (event->button() == Qt::LeftButton)
	{
		mouseIsPress = true;
		mouseStartPoint = event->pos();
	}
}

void TitleBar::mouseReleaseEvent(QMouseEvent *event)
{
	QWidget::mouseReleaseEvent(event);
	if (event->button() == Qt::LeftButton)
	{
		mouseIsPress = false;
	}
}

MainWindowDef::MainWindowDef(QWidget *parent /*= 0*/)
:QWidget(parent), ui(new Ui::Window())
{
	ui->setupUi(this);
	this->setWindowFlags(Qt::FramelessWindowHint);
	connect(ui->titleBar, SIGNAL(toMove(QPoint)), this, SLOT(titleBarMove(QPoint)));
	connect(ui->btMini, SIGNAL(clicked(bool)), this, SLOT(toolButtonClicked(bool)));
	connect(ui->btClose, SIGNAL(clicked(bool)), this, SLOT(toolButtonClicked(bool)));
	connect(ui->btMaxShow, SIGNAL(clicked(bool)), this, SLOT(toolButtonClicked(bool)));

	boundaryWidth = 5;
	/*
		设置鼠标移动事件追踪。
		如果不设置此选项，那么仅当鼠标按下时才会触发moveEvent
	*/
	this->setMouseTracking(true);


	//初始化顶部的快捷栏
	toolbar = new QToolBar();
	ui->ToolbarWidget->layout()->addWidget(toolbar);
}


MainWindowDef::~MainWindowDef()
{
	delete ui;
}

void MainWindowDef::mouseMoveEvent(QMouseEvent *event)
{
	QWidget::mouseMoveEvent(event);
	changeCursor(event->pos());
	changeSize(event->pos());
}

void MainWindowDef::mousePressEvent(QMouseEvent *event)
{
	QWidget::mousePressEvent(event);
	if (event->button() == Qt::LeftButton)
	{
		leftButtonIsPress = true;
		leftButtonPressPos = event->pos();
	}
}

void MainWindowDef::mouseReleaseEvent(QMouseEvent *event)
{
	QWidget::mouseReleaseEvent(event);
	if (event->button() == Qt::LeftButton)
	{
		leftButtonIsPress = false;
	}
}

void MainWindowDef::resizeEvent(QResizeEvent *event)
{
	QWidget::resizeEvent(event);
	if (isMax)
		isMax = false;
}

void MainWindowDef::titleBarMove(QPoint pos)
{
	this->move(this->pos() + pos);
}

void MainWindowDef::toolButtonClicked(bool b)
{
	if (sender() == ui->btMini){
		this->showMinimized();
	}
	else if (sender() == ui->btClose){
		this->close();
	}else if (sender() == ui->btMaxShow)
	{
		if (!isMax)
		{
			showMax();
		}else{
			showOld();
		}
		
	}
}

void MainWindowDef::changeCursor(const QPoint& pos)
{
	//防止已经在拖拽状态的时候改变光标的状态
	if (leftButtonIsPress)
		return;
	auto rpos = this->pos() - pos;
	bool bright , bbottom ;
	bright = bbottom = false;

	if ((pos.x() + boundaryWidth - this->width()) > 0)
		bright = true;
	if ((pos.y() + boundaryWidth - this->height()) > 0)
		bbottom = true;
	
	 if (bbottom && bright)
	{
		setCursor(Qt::SizeFDiagCursor);
		cursorState = RIGHT_BOTTOM;
	}else if (bbottom)
	{
		setCursor(Qt::SizeVerCursor);
		cursorState = BOTTOM;
	}else if (bright){
		setCursor(Qt::SizeHorCursor);
		cursorState = RIGHT;
	}else{
		setCursor(Qt::ArrowCursor);
		cursorState = NONE;
	}
		

}

void MainWindowDef::changeSize(const QPoint& pos)
{
	if (cursorState == NONE)
		return;
	if (!leftButtonIsPress)
		return;
	int w, h;
	w = pos.x() - leftButtonPressPos.x();
	h = pos.y() - leftButtonPressPos.y();
	leftButtonPressPos = pos;
	switch (cursorState)
	{
	case BOTTOM:
		this->resize(this->width(), this->height() + h);
		break;
	case RIGHT:
		this->resize(this->width() + w, this->height());
		break;
	case RIGHT_BOTTOM:
		this->resize(this->width() + w, this->height() + h);
		break;
	default:
		break;
	}
}


void MainWindowDef::addCenterWidget(QWidget *widget)
{
	ui->centerWidget->layout()->addWidget(widget);
}

void MainWindowDef::addTitleShortcutAction(QAction* action)
{
	toolbar->addAction(action);
}

void MainWindowDef::showMax()
{
	oldSize = this->size();
	oldPoint = this->pos();
	resize(QApplication::desktop()->availableGeometry().size());
	move(0, 0);
	isMax = true;
}

void MainWindowDef::showOld()
{
	resize(oldSize);
	move(oldPoint);
}

#include "moc_MainWindowDef.cpp"

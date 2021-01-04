#include "PreCompiled.h"
#include "MainWindow.h"
#include "ui_MainWindow.h"

#include <QMenu>
#include <QMessageBox>
#include "picgui_ribbon/moc_MainWindow.cpp"
MainWindow::MainWindow(QWidget *parent)
  : QMainWindow(parent)
  , ui(new Ui::MainWindow)
{
  ui->setupUi(this);

  // Hide ribbon dock title bar
  ui->ribbonDockWidget->setTitleBarWidget(new QWidget());

  // Add tabs to ribbon
  ui->ribbonTabWidget->addTab(tr("Start"));
  ui->ribbonTabWidget->addTab(tr("Build"));
  ui->ribbonTabWidget->addTab(tr("BorderAndObserveSetting"));




  // Add 'Open project' button
  QToolButton *btn1 = new QToolButton;
  btn1->setText(tr("New"));
  btn1->setToolTip(tr("create a new file"));
  btn1->setEnabled(true);
  ui->ribbonTabWidget->addButton(tr("Start"), tr("File"), btn1);

  // Add 'New project' button
  QToolButton *btn2 = new QToolButton;
  btn2->setText(tr("open"));
  btn2->setToolTip(tr("open an exist file"));
  btn2->setEnabled(true);
  ui->ribbonTabWidget->addButton(tr("Start"), tr("File"), btn2);






}

MainWindow::~MainWindow()
{
  delete ui;
}

#include "FourierDialog.h"
#include "ui_FourierDialog.h"
#include <QDebug>

namespace DV {
    FourierDialog::FourierDialog(QWidget* parent)
        : QDialog(parent), ui(new Ui::FourierDialog)
    {
        ui->setupUi(this);
        QObject::connect(this->ui->pb_ok, SIGNAL(clicked(bool)), this, SLOT(slotOk()));
    }

    FourierDialog::~FourierDialog()
    {
        delete ui;
    }

    void FourierDialog::slotOk()
    {
        this->close();
    }

};

#include "moc_FourierDialog.cpp"


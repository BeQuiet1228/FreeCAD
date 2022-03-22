#include "FourierDialog.h"
#include "ui_FourierDialog.h"
#include <QDebug>

namespace DV {
    FourierDialog::FourierDialog(bool isSave, QWidget* parent)
        : QDialog(parent), ui(new Ui::FourierDialog)
    {
        ui->setupUi(this);
        changeText(isSave);
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

    void FourierDialog::changeText(bool flag) {
        if (flag) {
            ui->label_2->setText("save successfully, Visible after reopen");
        }
        else {
            ui->label_2->setText("Failed to save, data already exists");
        }
    }
};

#include "moc_FourierDialog.cpp"


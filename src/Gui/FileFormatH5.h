#include "OpenFileConfig.h"
class FileFormatH5 :public FileFormat
{
public:
	FileFormatH5()
	{
		this->format = QString::fromLocal8Bit("h5");
	}
	~FileFormatH5() = default;
	void open(const QStringList& fileList) override;
protected:
	void openOnce(const QString& fileList, App::Document* doc);
};
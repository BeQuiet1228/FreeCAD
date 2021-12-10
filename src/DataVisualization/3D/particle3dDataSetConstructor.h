#pragma  once
#include "dataSetConstructor.h"
namespace DV3D {
	class Particle3dDataSetConstructor:public DataSetConstructorH5 {
	public:
		Particle3dDataSetConstructor() = default;
		~Particle3dDataSetConstructor() =default;

	public:
		vtkSmartPointer<vtkDataSet> creatDataset() override;

	private:
		void disposThetaData(std::vector<float>& data);
	};

}
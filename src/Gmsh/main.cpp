#include <iostream>
#include <vector>
#include <gmsh.h>

int main(int argc, char** argv) {
	gmsh::initialize(argc, argv);

	try {
		// 1. 导入 STEP 文件
		std::string filename = "F:/PICGUIC_L/Example/3d/MILO-C/xinxin.brep"; // 替换为你的 STEP 文件路径
		gmsh::merge(filename);

		// 2. 获取所有几何实体（volumes）的标签
		std::vector<int> volumes;
		gmsh::vectorpair tags;
		gmsh::model::getEntities(tags, 3); // 获取所有三维实体（volumes）
		for (auto tag = tags.begin(); tag != tags.end();tag++) {
			volumes.push_back(tag->first);
		}

		// 如果没有找到volume，则退出
		if (volumes.empty()) {
			std::cerr << "Error: No volumes found in the STEP file." << std::endl;
			gmsh::finalize();
			return 1;
		}

		// 3. 设置网格尺寸
		double characteristicLength = 1.0; // 全局网格尺寸
		gmsh::option::setNumber("Mesh.CharacteristicLengthMin", characteristicLength / 2);
		gmsh::option::setNumber("Mesh.CharacteristicLengthMax", characteristicLength);

		// 你可以根据需要设置局部网格尺寸，例如：
		// gmsh::model::mesh::setSize(gmsh::model::getEntities(2), characteristicLength / 4); // 对所有面设置更小的网格尺寸

		// 4. 生成三维网格（四面体）
		gmsh::model::mesh::generate(3);

		// 5. 获取节点和单元信息
		std::vector<double> nodeCoords;
		std::vector<double> parCoor;
		std::vector<size_t> nodeTags;
		std::vector<std::vector<size_t>> elementTags;
		std::vector<std::vector<size_t>> elementNodeTags;
		std::vector<int> elementTypes;

		gmsh::model::mesh::getNodes(nodeTags, nodeCoords, parCoor);
		gmsh::model::mesh::getElements(elementTypes, elementTags, elementNodeTags, 3);

		// 遍历单元并打印信息 (四面体单元类型为 4)
		//for (size_t i = 0; i < elementTypes.size(); ++i) {
		//	if (elementTypes[0][i] == 4) {
		//		std::cout << "Tetrahedron " << elementTags[i] << ": ";
		//		for (size_t j = 0; j < 4; ++j) {
		//			std::cout << elementNodeTags[i * 4 + j] << " ";
		//		}
		//		std::cout << std::endl;
		//	}
		//}


		// 6. 将网格保存到 .msh 文件
		gmsh::write("mesh.msh");

		// 7. 可视化（可选，需要 Gmsh GUI）
		// gmsh::fltk::run();

	}
	catch (...) {
		std::cerr << "Gmsh exception: "  << std::endl;
		return 1;
	}

	gmsh::finalize();
	return 0;
}
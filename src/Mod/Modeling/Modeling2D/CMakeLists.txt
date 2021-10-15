
SET(Modeling2D_Srcs
	__init__.py
	InitGui2D.py
)
SET(Modeling2DGui_Srcs
	./Modeling2DGui/__init__.py
	./Modeling2DGui/TestMenu.py
	./Modeling2DGui/TestToolBar.py
)
SET(modeling2DResources_Srcs
./modeling2DResources/2DModelingWorkbench.png
./modeling2DResources/2DModelingWorkbench.svg
./modeling2DResources/2d圆形.svg
./modeling2DResources/2d多边形面.svg
./modeling2DResources/2d扇形.svg
./modeling2DResources/2d点.svg
./modeling2DResources/2d矩形面.svg
./modeling2DResources/mark设置.svg
./modeling2DResources/save.svg
./modeling2DResources/二次发射.svg
./modeling2DResources/优化算法.svg
./modeling2DResources/保存.svg
./modeling2DResources/修理.svg
./modeling2DResources/倒角形.svg
./modeling2DResources/关闭.svg
./modeling2DResources/函数体.svg
./modeling2DResources/函数面.svg
./modeling2DResources/剪切.svg
./modeling2DResources/参数设置.svg
./modeling2DResources/参数阵列体.svg
./modeling2DResources/吸收边界.svg
./modeling2DResources/回旋发射.svg
./modeling2DResources/圆台.svg
./modeling2DResources/圆形区域体.svg
./modeling2DResources/圆环体.svg
./modeling2DResources/圆面.svg
./modeling2DResources/场及函数定义.svg
./modeling2DResources/复制.svg
./modeling2DResources/多边形.svg
./modeling2DResources/宏粒子合并.svg
./modeling2DResources/对称边界.svg
./modeling2DResources/工作区间设置.svg
./modeling2DResources/布尔运算.svg
./modeling2DResources/并行运行.svg
./modeling2DResources/强场发射.svg
./modeling2DResources/恢复.svg
./modeling2DResources/扇形面.svg
./modeling2DResources/打开.svg
./modeling2DResources/打开log文件.svg
./modeling2DResources/投影线.svg
./modeling2DResources/投影面.svg
./modeling2DResources/挤压体.svg
./modeling2DResources/撤销.svg
./modeling2DResources/数据导出设定.svg
./modeling2DResources/文字.svg
./modeling2DResources/斜线.svg
./modeling2DResources/新型粒子定义.svg
./modeling2DResources/新建.svg
./modeling2DResources/新材料定义.svg
./modeling2DResources/旋转体.svg
./modeling2DResources/时域计算设置.svg
./modeling2DResources/时间观测.svg
./modeling2DResources/最大化.svg
./modeling2DResources/最小化.svg
./modeling2DResources/本地连接.svg
./modeling2DResources/束发射.svg
./modeling2DResources/楔形体.svg
./modeling2DResources/模型信息输入.svg
./modeling2DResources/正投影体.svg
./modeling2DResources/正投影线.svg
./modeling2DResources/正投影面.svg
./modeling2DResources/气体电离.svg
./modeling2DResources/波导端口.svg
./modeling2DResources/注释.svg
./modeling2DResources/测距.svg
./modeling2DResources/点.svg
./modeling2DResources/热致发射.svg
./modeling2DResources/爆炸式发射.svg
./modeling2DResources/环形区域体.svg
./modeling2DResources/球体.svg
./modeling2DResources/电感.svg
./modeling2DResources/矢量图观测.svg
./modeling2DResources/矩形面.svg
./modeling2DResources/空间电流源.svg
./modeling2DResources/空间观测.svg
./modeling2DResources/等位图观测.svg
./modeling2DResources/箔片.svg
./modeling2DResources/粒子相对空间观测.svg
./modeling2DResources/粒子设置.svg
./modeling2DResources/粘贴.svg
./modeling2DResources/线.svg
./modeling2DResources/网格.svg
./modeling2DResources/网络连接.svg
./modeling2DResources/自定义定时器.svg
./modeling2DResources/草图拉伸体.svg
./modeling2DResources/草图旋转体.svg
./modeling2DResources/菱形体.svg
./modeling2DResources/螺旋体.svg
./modeling2DResources/螺旋线圈.svg
./modeling2DResources/西面体.svg
./modeling2DResources/调整视角.svg
./modeling2DResources/运行停止.svg
./modeling2DResources/运行处理选项.svg
./modeling2DResources/运行时.svg
./modeling2DResources/金字塔体.svg
./modeling2DResources/阵列体.svg
./modeling2DResources/默认定时器.svg
./modeling2DResources/translations/3DModeling.pro
./modeling2DResources/translations/3DModeling_zh-CN.qm
./modeling2DResources/translations/3DModeling_zh-CN.ts
./modeling2DResources/translations/Modeling3D_zh-CN.pro
./modeling2DResources/translations/Modeling3D_zh-CN.qm
./modeling2DResources/translations/Modeling3D_zh-CN.ts
)

SET(Tools_Srcs
./Tools/CompleterTools.py
./Tools/ExpressionTools.py
./Tools/FileView.py
./Tools/InitDoc.py
./Tools/MainWindow.py
./Tools/Repair.py
./Tools/SaveM2D.py
./Tools/Tools2D.py
./Tools/ToolsForDisplay.py
./Tools/ToolsUI.py
./Tools/UpdateBoolean2D.py
./Tools/__init__.py
)
SET(all_Srcs
${Modeling2D_Srcs}
${Modeling2DGui_Srcs}
${modeling2DResources_Srcs}
${Tools_Srcs}
)
add_custom_target(Modeling2D ALL SOURCES ${all_Srcs})

fc_copy_sources(Modeling2D "${CMAKE_BINARY_DIR}/Mod/Modeling/Modeling2D" ${all_Srcs})
install(FILES ${all_Srcs} DESTINATION Mod/Modeling/Modeling2D)
#install(
#	FILES
#	${Modeling2D_Srcs}
#	DESTINATION
#	Mod/Modeling/Modeling2D
#)
#install(
#	FILES
#	${Modeling2DGui_Srcs}
#	DESTINATION
#	Mod/Modeling/Modeling2D/Modeling2DGui
#)
#install(
#	FILES
#	${translations_Srcs}
#	DESTINATION
#	Mod/Modeling/Modeling2D/modeling2DResources/translations
#)
#install(
#	FILES
#	${modeling2DResources_Srcs}
#	DESTINATION
#	Mod/Modeling/Modeling2D/modeling2DResources
#)
add_subdirectory(Modeling2DCommand)
#\src\Mod\Modeling\Modeling3D
#PYSIDE_WRAP_RC(Modeling3D_RC ./modeling3DResources/Modeling3D.qrc)
SET(Modeling3D_Srcs
__init__.py
init.py
InitGui3D.py
#Modeling3D_rc.py
#${Modeling3D_RC}
Modeling3D_rc.py
Modeling3DGuiTest.py
)
#\src\Mod\Modeling\Modeling3D\Modeling3DCommand
add_subdirectory(Modeling3DCommand)
#src\Mod\Modeling\Modeling3D\Modeling3DGui
SET(Modeling3DGui_Srcs
./Modeling3DGui/TestMenu.py
./Modeling3DGui/TestToolBar.py
./Modeling3DGui/__init__.py
)
#\src\Mod\Modeling\Modeling3D\modeling3DResources
SET(modeling3DResources_Srcs
./modeling3DResources/3DCone.svg
./modeling3DResources/3DCylinder.svg
./modeling3DResources/3DFunctionArea.svg
./modeling3DResources/3DHollowedCylinder.svg
./modeling3DResources/3DModelingWorkbench.png
./modeling3DResources/3DModelingWorkbench.svg
./modeling3DResources/3DOrthographicBody.svg
./modeling3DResources/3DParallelogram.svg
./modeling3DResources/3DPoint.svg
./modeling3DResources/3DPyramid.svg
./modeling3DResources/3DRevolution.svg
./modeling3DResources/3DSpecialCone.svg
./modeling3DResources/3DSphere.svg
./modeling3DResources/3DTorus.svg
./modeling3DResources/3DTorusFace.svg
./modeling3DResources/3DWedge.svg
./modeling3DResources/3D_Area_Conformal.svg
./modeling3DResources/3D_Area_Polygonal.svg
./modeling3DResources/3D_Area_Rectangular.svg
./modeling3DResources/3D_Array.svg
./modeling3DResources/3D_LineOblique.svg
./modeling3DResources/3D_Line_Conformal.svg
./modeling3DResources/3D_Point.svg
./modeling3DResources/3D_Vol_Annular.svg
./modeling3DResources/3D_Vol_Annular_Section.svg
./modeling3DResources/3D_Vol_Conformal.svg
./modeling3DResources/3D_Vol_Cylinder.svg
./modeling3DResources/3D_Vol_Extruded.svg
./modeling3DResources/3D_Vol_Function.png
./modeling3DResources/3D_Vol_Function.svg
./modeling3DResources/3D_Vol_Helical.svg
./modeling3DResources/3D_Vol_Parallelepipedal.svg
./modeling3DResources/3D_Vol_ParamArray.svg
./modeling3DResources/3D_Vol_Pyramid.svg
#./modeling3DResources/3D_Vol_Rhombus (2).svg
./modeling3DResources/3D_Vol_Rhombus.svg
./modeling3DResources/3D_Vol_SpecialCone.svg
./modeling3DResources/3D_Vol_Spherical.svg
./modeling3DResources/3D_Vol_Tetrahedron.svg
./modeling3DResources/3D_Vol_Toroidal_Section.svg
./modeling3DResources/3D_Vol_Wedge.svg
./modeling3DResources/DraftExtrusion.svg
./modeling3DResources/DraftRevolution.svg
./modeling3DResources/f9wing.FCStd
./modeling3DResources/Modeling3D.qrc
./modeling3DResources/refreshAll.svg
./modeling3DResources/refreshPart.svg
./modeling3DResources/save.svg
./modeling3DResources/_Operation_Clip.svg
./modeling3DResources/_Operation_Copy.svg
./modeling3DResources/_Operation_Cut.svg
./modeling3DResources/_Operation_Paste.svg
)
#\src\Mod\Modeling\Modeling3D\modeling3DResources\translations
SET(translations_Srcs
./modeling3DResources/translations/3DModeling.pro
./modeling3DResources/translations/3DModeling_zh-CN.qm
./modeling3DResources/translations/3DModeling_zh-CN.ts
./modeling3DResources/translations/Modeling3D_zh-CN.pro
./modeling3DResources/translations/Modeling3D_zh-CN.qm
./modeling3DResources/translations/Modeling3D_zh-CN.ts
)
#D:\wdt\FreeCAD\src\Mod\Modeling\Modeling3D\Tools
SET(Tools_Srcs
./Tools/ModelingByUITools.py
./Tools/OtherTools.py
./Tools/RebuildForUITools.py
./Tools/__init__.py
)

SET(all_Srcs
${Modeling3D_Srcs}
${Modeling3DGui_Srcs}
${modeling3DResources_Srcs}
${translations_Srcs}
${Tools_Srcs}
)
add_custom_target(Modeling3D ALL SOURCES ${all_Srcs})
fc_copy_sources(Modeling3D "${CMAKE_BINARY_DIR}/Mod/Modeling/Modeling3D" ${all_Srcs})
install(FILES ${all_Srcs} DESTINATION Mod/Modeling/Modeling3D)
#install(FILES ${Modeling3D_Srcs}          DESTINATION Mod/Modeling/Modeling3D)
#install(FILES ${Modeling3DGui_Srcs}       DESTINATION Mod/Modeling/Modeling3D/Modeling3DGui)
#install(FILES ${modeling3DResources_Srcs} DESTINATION Mod/Modeling/Modeling3D/modeling3DResources)
#install(FILES ${translations_Srcs}        DESTINATION Mod/Modeling/Modeling3D/modeling3DResources/translations)
#install(FILES ${Tools_Srcs} DESTINATION Mod/Modeling/Modeling3D/Tools)
#install(FILES ${Physics_Srcs} DESTINATION Mod/Modeling/Modeling3D/Physics)
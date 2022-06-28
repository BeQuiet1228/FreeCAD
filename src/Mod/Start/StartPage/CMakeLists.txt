#INSTALL(FILES ${StartPage_Scripts}
#    DESTINATION Mod/Start/StartPage
#)
#
#INSTALL(FILES ${StartPage_Resources}
#    DESTINATION ${CMAKE_INSTALL_DATADIR}/Mod/Start/StartPage
#)
#
#INSTALL(DIRECTORY images/ 
#    DESTINATION ${CMAKE_INSTALL_DATADIR}/Mod/Start/StartPage/images
#)
SET(Sources_Srcs
	ArchDesign.py
	DefaultWorkbench.py
	EnableDownload.py
	LoadArchExample.py
	LoadDrawingExample.py
	LoadFemExample2D.py
	LoadFemExample3D.py
	LoadFemExample3DNewSolver.py
	LoadMRU0.py
	LoadMRU1.py
	LoadMRU2.py
	LoadMRU3.py
	LoadPartDesignExample.py
	LoadRobotExample.py
	LoadSchenkel.py
	Mesh.py
	PartDesign.py
	Ship.py
	StartPage.css
	StartPage.html
	StartPage.js
	StartPage.py
	TranslationTexts.py
	__init__.py
	#
	images
)
File(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Start/StartPage)
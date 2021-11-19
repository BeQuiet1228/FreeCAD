IF(BUILD_GUI)
    PYSIDE_WRAP_RC(Ship_QRC_SRCS resources/Ship.qrc)
ENDIF(BUILD_GUI)
SET(ShipMain_SRCS
    InitGui.py
    ShipGui.py
    Instance.py
    TankInstance.py
    WeightInstance.py
	Ship.py
	ToursFaceInstance.py
	${Ship_QRC_SRCS}
	resources
	shipAreasCurve
	shipCapacityCurve
	shipCreateLoadCondition
	shipCreateShip
	shipCreateTank
	shipCreateWeight
	shipGZ
	shipHydrostatics
	shipLoadExample
	shipOutlineDraw
	shipUtils
)
add_custom_target(Ship)
File(COPY ${ShipMain_SRCS} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Ship)
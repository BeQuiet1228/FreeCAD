require "math"

--初始化
overvarName={};
overvar={};
variateCount=0;
function init()
cppPrint("init_start");
for i=0,variateCount-1,1 
do 
	addVariate(overvarName[i],overvar[i]);
end
	setRunDataMakeType("exhaustivity");
end
--返回
function resultDataFilter()
	cppPrint("resultDataFilter");
	return true;
end

function resultExpcet()
	cppPrint("resultExpcet");
	return true;
end
--根据传入步长创建数值
function addVarMod1(name,max,mini,stepsize)
	overvarName[variateCount]=name;
	local interval=(max-mini)/(stepsize-1);
	local lval={};
	for i=0,stepsize-1,1
	do
		lval[i]=mini+interval*i;
	end
	overvar[variateCount]=lval;
	variateCount=variateCount+1;
end
--根据队列传入
function addVarMod2(name,lvar)
	for key,var in pairs(overvarName)
	do
		if var==name then
		--获取tab的长度
		local length=#overvar[key];
		overvar[key][length+1]=lvar;
		return
		end
	end
	overvarName[variateCount]=name;
	local lval={};
	lval[0]=lvar;
	overvar[variateCount]=lval;
	variateCount=variateCount+1;
end

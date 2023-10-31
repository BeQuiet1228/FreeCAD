require "math"
--声明一个参数容器
variates = {};
variateCount = 0;
pgtF = 0;
--pgtf 是否初始化
pgtFInit = true;
pitF = 0;
valueCount = 0;
--获取F得定义
function getF(minif,maxf,avf)
	if(fmod == 0)
	then
		return maxf;
	end
	if(fmod == 1)
	then
		return minif
	end
	if(fmod == 2)
	then
		return avf;
	end
	if(fmod == 3)
	then
		return avf*math.exp(-math.abs(maxf/avf - 2));
	end
end

--保存运行参数
function saveVarToFile()
	creatVarableFileObject();
	addFileVariable("pgtF",pgtF,"n");
	local i = 1;
	while(i < variateCount + 1)
	do
		var = variates[i];
		addFileVariable("var"..i..".name",var.name,"s");
		addFileVariable("var"..i..".max",var.max,"n");
		addFileVariable("var"..i..".mini",var.mini,"n");
		addFileVariable("var"..i..".pgt",var.pgt,"n");

		local index = 1;
		while(index < valueCount + 1)
		do
			addFileVariable("var"..i..".variate"..index,var.variate[index],"n")
			addFileVariable("var"..i..".vit"..index,var.vit[index],"n");
			addFileVariable("var"..i..".pit"..index,var.pit[index],"n");
			addFileVariable("var"..i..".pitF"..index,var.pitF[index],"n");
			index = index + 1;
		end
		i = i + 1;
	end
	
	saveVariableFile("test");
	closeVariableFile();
end
--读取运行参数
function loadVarToFile()
	if(not openVariableFile("test"))
	then
		return false;
	end

	pgtF = getFileVariable("pgtF","n");

	local i = 1;
	while(i < variateCount + 1)
	do
		local var = {};
		var.name = getFileVariable("var"..i..".name","s");
		var.max = getFileVariable("var"..i..".max","n");
		var.mini = getFileVariable("var"..i..".mini","n");
		var.pgt = getFileVariable("var"..i..".pgt","n");

		print("vaar.name:"..var.name);

		var.vit = {};
		var.pit = {};
		var.pitF = {};
		var.variate = {};
		local index = 1;
		while(index < valueCount + 1)
		do
			var.variate[index] = getFileVariable("var"..i..".variate"..index,"n");
			print(",var.variate"..index..":"..var.variate[index]);
			var.vit[index] = getFileVariable("var"..i..".vit"..index,"n");
			var.pit[index] = getFileVariable("var"..i..".pit"..index,"n");
			var.pitF[index] = getFileVariable("var"..i..".pitF"..index,"n");
			index = index + 1;
		end
		variates[i] = var;
		i = i + 1;
	end
end

function printInformation()
	if(variateCount < 1)
	then
		return;
	end
	cppPrint("——————第"..getHistorySize().."轮历史最优数据——————");
	cppPrint("F = "..pgtF);
	local i = 1;
	while(i < variateCount + 1)
	do
		local var = variates[i];
		cppPrint(var.name.." = "..var.pgt);
		i = i + 1;
	end
end
--判断两个f哪一个更符合预期
--如果第一个f更符合预期 则返回true
function compareF(f1,f2)
if(excpectMod == 0)
then
	if(math.abs(f1 - excpectF) < math.abs(f2 - excpectF))
	then
		return true;
	end
	return false;
end
if(excpectMod == 1)
then
	if(f1 > f2)
	then
		return true;
	end
	return false;
end
end
--保留五位数小数点的随机浮点数
function randmoFloat(mini,max)
	if(mini > max)
	then
		local temp = max
		max = mini
		mini = temp
	end
	
	local randomValue = mini + math.random() * (max - mini)
	print("rand value"..randomValue);
	return randomValue;
end
--添加参数函数
function addVar(name,max,mini,count)
    local var = {};
    local i = 1;
	local v = {};
	var.vit = {};
	var.pgt = 0;
	var.pit = {};
	var.pitF = {};
    while(i < count + 1)
	do
		--设置参数值
		v[i] = randmoFloat(mini,max);
		--初始化参数的增量
		local vitV = math.abs(mini - max)/2;
		var.vit[i] = randmoFloat(-vitV,vitV);
		--var.vit[i] = vitV;
		var.pitF[i] = 0;
		var.pit[i] = 0;
		i = i + 1;
	end
    var.variate = v;
    var.name = name;
    var.max = max;
    var.mini = mini;
    variateCount = variateCount + 1;
    variates[variateCount] = var;
	valueCount = count;
	
	print("------");
end
function rand()
	return math.random();
end
function init()
 
 --判断是否按上次的优化数据继续优化
 if(continue)
 then
	loadVarToFile();
 end
 local index = 1;
 while(index < variateCount + 1)
 do
	--输出参数值
	local i = 1;
	local log = variates[index].name.."= "
	while(i < valueCount + 1)
	do
		log = log..variates[index].variate[i]..",";
		i = i + 1;
	end
	--cppPrint(log);
	--往c中添加变量
	addVariate(variates[index].name,variates[index].variate);
	index = index + 1;
 end
end
function resultDataFilter()
 getAllResult();
 while(nextResult())
 do
	if(not openH5File())
	then
		print("open h5file false1!");
		return false;
	end
	if(not findResultData(observeName))
	then
		print("find result false2!");
		return false;
	end
 
	if(not openDataSet())
	then
		print("open data set false3!");
		return false;
	end
	local valueSize = getDataSetVlaueSize();
	local i = 0;
	local max = getValue(0);
	local mini = getValue(0);
	local add = 0;
	local addCount = 0;
	while(i < valueSize)
	do
		local time = getValue(i);
		if(time > miniTime and time < maxTime)
		then
			local value = getValue(i+1);
			addCount = addCount + 1;
			add = add + value;
			if(value > max)
			then
				max = value;
			end
			if(value < mini)
			then
				mini = value;
			end
		end
		i = i + 2;
	end
	local av = add/addCount;
	local f = getF(mini,max,av);
	addParam(f);
	closeH5File();
 end
 saveParamsInHistory();
 local groupIndex = getHistorySize() - 1;
 local groupSize = getGroupSize(groupIndex);
 local index = 0;
 local maxF = 0;
 local maxFIndex = 0;
 while(index < groupSize)
 do
	local F = getParam(groupIndex,index,0);
	local pitF = variates[1].pitF[index + 1];
	print("pitf="..pitF..",F="..F..",x="..variates[1].variate[index + 1]);
	if(compareF(F,pitF))
	then
		local countIndex = 1;
		while(countIndex < variateCount + 1)
		do
			variates[countIndex].pitF[index + 1] = F;
			variates[countIndex].pit[index + 1] = variates[countIndex].variate[index + 1];
			--local error = variates[countIndex].pit[index + 1];
			--if( math.abs(F - 500093) < 1 and math.abs(error - 0.029) > 0.001)
			--then
			--	pgtF = 500000;
			--end
			--print("pitf="..F.."pit="..variates[countIndex].pit[index + 1]);
			countIndex = countIndex + 1;
		end
    end
	--在这里使用F初始化pgtF
	if(pgtFInit)
	then
		pgtF = F;
		pgtFInit = false;
		--保存最好的结果
		saveResultToWorkPath(index,"best");
		
		pgtF = F;
        local tempIndex = 1;
        while(tempIndex < variateCount + 1)
        do
			variates[tempIndex].pgt = variates[tempIndex].variate[index + 1];
			--cppPrint("pgtF="..F.."pgt="..variates[tempIndex].pgt)
			tempIndex = tempIndex + 1;
		end
	end
	
	if(compareF(F,pgtF))
	then
		--保存最好的结果
		saveResultToWorkPath(index,"best");
		
		pgtF = F;
        local tempIndex = 1;
        while(tempIndex < variateCount + 1)
        do
			variates[tempIndex].pgt = variates[tempIndex].variate[index + 1];
			--cppPrint("pgtF="..F.."pgt="..variates[tempIndex].pgt)
			tempIndex = tempIndex + 1;
		end
    end
	index = index + 1;
 end
 return true;
end

function resultExpcet()
  --如果超过最大优化次数 则也停止优化
 if(getHistorySize() >= optimizeMaxCount)
 then
    return true;
 end

 --判断目标模式
if(excpectMod == 0)
then
	--cppPrint("pgtF"..pgtF..",excpectF:"..excpectF..",accuracy:"..accuracy);
	if(math.abs(pgtF - excpectF) < accuracy * math.abs(pgtF))
 	then
	return true;
	end
	return false;
end
if(excpectMod == 1)
then
   if(pgtF > excpectF)
	then
   		return true;
   	end
   return false;
end
end
function optimize()
 local variateIndex = 1;
 while(variateIndex < variateCount + 1)
 do
     local index = 1;
     local tempVariate = variates[variateIndex];
	 --cppPrint("variateIndex:"..variateIndex);
	 while(index < valueCount + 1)
	 do
		--cppPrint("index:"..index)
        local temp = 0;
        local value = tempVariate.variate[index];
		local vit = tempVariate.vit[index];
        local pit = tempVariate.pit[index];
        local pgt = tempVariate.pgt;
        local mini = tempVariate.mini;
		local max = tempVariate.max;
		vmax=(max-mini)*0.15;
		vmin = -vmax;
        temp = omiga*vit + c1*rand()*(pit - value) + c2*rand()*(pgt - value);
		--cppPrint("omiga:"..omiga..",vit:"..vit..",cl:"..c1..",pit:"..pit..",pgt:"..pgt..",value:"..value);
		while(temp < vmin  or temp > vmax )
		do 
			--cppPrint("temp"..temp..",vmin:"..vmin..",vmax:"..vmax);
		  if (temp < vmin)
          then 
              temp = vmin  + math.abs(temp  - vmin )	
          else
			  temp = vmax  - math.abs(vmax  - temp);
			end		
        end		
 		tempVariate.vit[index] = temp;
        value = value + temp;
		while(value < mini or value > max)
		do
			--cppPrint("value:"..value..",mini:"..mini..",max:"..max);
			if(value < mini)
			then
				value = mini + math.abs(value - mini);
			else
				value = max - math.abs(max - value);
			end
		end
		tempVariate.variate[index] = value;
		index = index + 1;	
     end
     variates[variateIndex] = tempVariate;
	 variateIndex = variateIndex + 1;
 end
 saveVarToFile();
 init();
end
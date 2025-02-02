// 此 脚本 专 攻 循环体J

//模式【起_重复点k_终】 ： 入  --t-->    重复'BJ--fJ-->LJ--tJ'  -->  出 
//模式【起_重复点k_终】 写作 逐小重复节往前拱 的样子，即：
//  起点--t入-->                           开头    在 query__起_t入_B0.cypher ，具体请详细看该脚本
//              B0--f0-->L0--t0-->        循环体0
//              B1--f1-->L1--t1-->        循环体1
//              B2--f2-->L2--t2-->        循环体2
//         ...
//              BJ--fJ-->LJ--tJ-->        循环体J     其中 J_1==J-1
//         ...
//              B9--f9-->L9--t9-->        循环体3
//                           t出      终点            其中 t出==t9

// 写在一行 即:
//    起点     --t入-->B0--f0-->L0--t0-->    B1--f1-->L1--t1-->   B2--f2-->L2--t2-->  ...  BJ--fJ-->LJ--tJ-->  ...  B9--f9-->L9--t出-->  终点


with 
$fnCallId as param_fnCallId, 
//14 as param_fnCallId 开发调试用，生产不要使用
1 AS FnEnter, //Enter == Begin == B
2 as FnLeave //Leave == End == L
MATCH path= 

  (BJ:V_FnCallLog  {fnCallId:param_fnCallId, direct: FnEnter } ) - [fJ:E_FnEL] -> (LJ:V_FnCallLog {direct:FnLeave}  ) - [tJ:E_NxtTmPnt] -> (_:V_FnCallLog)
  
WHERE   BJ.fnCallId = LJ.fnCallId

return  
path as 路径,
BJ,
tJ
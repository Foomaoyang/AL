# basic_MOPSO
based on the version of "https://github.com/dreamoffeature/mopso", which has too many mistakes, I rewrite the MOPSO algorithm, some kernel 
operators are learned from PlatEMO, which is based on MATLAB. Although the performance of MOPSO  is not well with respect to multimodal 
problem, you can run main.py to run MOPSO

>多目标粒子群算法(MOPSO)复现代码项目结构
>>main.py             主函数，设置粒子群参数、选择测试函数
>>Mopso.py            粒子群初始化  
>
>>util   工具函数
>>>pareto.py       
>>>update.py        粒子群速度、位置更新和存档  
>>>testFunc.py      测试函数  
>>>NDsort.py        非支配解排序  
>>>drawCurve.py     绘制曲线  
>
>>img_txt             存放导出的数据和图片  
>>>pareto_fitness.txt  
>>>pareto_pop.txt  
>>>*.png  


测试方程

DTLZ1方程

$$
\left \{
\begin{case}{c}
min $f_0(x)$=$\frac{1}{2}$$x_0x_1$(1+$g(x$)) 
min $f_1(x)$=$\frac{1}{2}$$x_0$(1-$x_1$)(1+$g(x)$)
min $f_2(x)$=$\frac{1}{2}$(1-$x_0$)(1+$g(x)$) 
$g(x)$=100(10+$\sum_{i=3}^n$$(x_{i}-0.5)^2$-cos(20$\pi$($x_i$-0.5))
\end{case}
\right.
$$


DTLZ2方程

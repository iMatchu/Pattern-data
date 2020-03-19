#run.sh

# 记录一下开始时间
echo `date` >> /Users/iMatch/Desktop/Pattern/log &&
# 进入.py程序所在目录
cd /Users/iMatch/Desktop/Pattern/ &&
# 执行python脚本（注意前面要指定python运行环境/usr/bin/python，根据自己的情况改变）
/opt/anaconda3/envs/VSC/bin/python /Users/iMatch/Desktop/Pattern/pattern003.py
# 运行完成
echo 'finish' >> /Users/iMatch/Desktop/Pattern/log


40 15 * * * opt/anaconda3/envs/VSC/bin/python /Users/iMatch/Desktop/Pattern/pattern003.py
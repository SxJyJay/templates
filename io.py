###################################
############# 基础功能 #############
###################################
# 读取单个整数
import sys
n = int(sys.stdin.readline().strip())  # .strip()去除末尾的\n换行符
print(n)

# 读取一行空格分割的整数
import sys
numbers = list(map(int, sys.stdin.readline().strip().split()))
print(numbers)

# 读取多行输入（不定行数）
import sys
lines = sys.stdin.read().splitlines()
for line in lines:
    print(line)

# 读取固定行数输入（第一行输入行数，第二行输入内容）
import sys
n = int(sys.stdin.readline().strip())
for _ in range(n):
    line = sys.stdin.readline().strip()
    print(line)


###################################
############# 进阶功能 #############
###################################


# 读取多行输入，且每行为用空格分隔的整数（不定行数）
'''
输入用例：
42 21 5
1 3 5 7
2 7 6 5
9 8 5 5
'''
import sys
lines = sys.stdin.read().splitlines()
for line in lines:
    if line.strip():  # 忽略空行
        numbers = list(map(int, line.split()))  # 按空格分割并转换为整数
        print(numbers)


# 读取多行输入，每行可能是整数可能是字符串（不定行数）
'''
输入用例：
42
hello
12345
Python3.9
'''
import sys
lines = sys.stdin.read().splitlines()  # 读取所有行，去除换行符
for line in lines:
    line = line.strip()  # 去掉可能存在的空白字符
    try:
        # 尝试将它转换为整数
        num = int(line)
        print(f"整数：{num}")
    except ValueError:
        # 转换失败，说明是字符串
        print(f"字符串：{line}")


# 分隔输入（每行可能是空格分隔的多个数据）
# 如果每行里可能有多个用空格分隔的数据，并且每个数据可能是整数或字符串：
'''
输入用例：
42 135
hello aad
12345 dkk45
Python3.9 32
'''
import sys
lines = sys.stdin.read().splitlines()
for line in lines:
    line = line.strip()
    if not line:
        continue

    for item in line.split():
        try:
            num = int(item)
            print(f"整数：{num}")
        except ValueError:
            try:
                num = float(item)
                print(f"浮点数：{num}")
            except ValueError:
                print(f"字符串：{item}")


# 直接以python的列表形式输入
# ast模块就是帮助Python应用来处理抽象的语法解析的。而该模块下的literal_eval()函数：则会判断需要计算的内容计算后是不是合法的python类型，如果是则进行运算，否则就不进行运算。
'''
输入用例：
[[1,3,4],
[2,3,4],
[6,9,8]]
'''
import sys
import ast
input = sys.stdin.read().strip()
try:
    matrix = ast.literal_eval(input)  # 将带[[和,的字符串安全解析为Python对象
    print(matrix)
except Exception as e:
    print(f"解析失败: {e}")

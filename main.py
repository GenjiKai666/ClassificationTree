def importDataforPractice(file_path): #导入训练样本
    dic = {}
    with open(file_path) as file_obj:
        for line in file_obj:
            if dic.__contains__(tuple(line.split())):
                dic[tuple(tuple(line.split()))] += 1
            else:
                dic[tuple(tuple(line.split()))] = 1
    return dic

def gini(dic): #计算样本Gini不纯度
   uniqueCount  = []
   sumOfNi_2 = 0
   sum = 0
   for key in dic:
       sum += dic[key]
       if key[-1] not in uniqueCount:
           uniqueCount.append(key[-1])
   for i in range(len(uniqueCount)):
       temp = 0
       for key in dic:
           if key[-1] == uniqueCount[i]:
               temp += 1
       sumOfNi_2 += temp**2
   return (1-(sumOfNi_2)/sum**2)

def g_gini(n,dic): #以第n个标签分裂的不纯度，约定左边为否，右边为是
    dic_L = {} #分裂后左边样本
    n_L = 0 #左样本数
    dic_R = {} #右样本
    n_R = 0 #右样本数
    for key in dic:
        if int(key[n]) == 0:
            dic_L[key] = dic[key]
            n_L += 1
        else:
            dic_R[key] = dic[key]
            n_R += 1
    n = n_L + n_R
    return [(n_L*gini(dic_L)+n_R*gini(dic_R))/n,gini(dic_L),gini(dic_R),dic_L,dic_R]

def construct(tree,dic,tag,next): #构造决策树，tree为二叉树，用列表方式存储，dic为样本，tag为标签（数据结构为集合),next为下一次递归根节点位置
    if len(tag) == 0:
        return tree
    else:

        temp  = 0
        for i in tag:
            if temp == 0:
                temp = g_gini(i-1,dic)[0]
                flag = i
            else:
                if temp > g_gini(i-1,dic)[0]:
                    temp = g_gini(i-1,dic)[0]
                    flag = i
        tree[next] = flag
        tag.remove(flag)
        if g_gini(flag-1,dic)[1] == 0 and g_gini(flag-1,dic)[2] == 0:
            tree[next * 2 + 1] = list(g_gini(flag-1,dic)[3].keys())[0][-1]
            tree[next * 2 + 2] = list(g_gini(flag-1,dic)[4].keys())[0][-1]
        elif g_gini(flag-1,dic)[1] == 0:
            tree[next*2+1] = list(g_gini(flag-1,dic)[3].keys())[0][-1]
            construct(tree,g_gini(flag-1,dic)[4],tag,next*2+2)
        elif g_gini(flag-1,dic)[2] == 0:
            tree[next*2+2] = list(g_gini(flag-1,dic)[4].keys())[0][-1]
            construct(tree, g_gini(flag - 1, dic)[3], tag, next * 2 + 1)
def fit_number(target):
    flag = False
    try:
        flag = target>0
        flag = True
    finally:
        return flag
def practice(tree,data,next): #验证测试集
    i = next
    while i<len(tree):
        if fit_number(tree[i]) == True:
            if data[tree[i]] == 1:
                if fit_number(tree[i*2+2]) == True:
                    practice(tree,data,i*2+2)
                else:
                    print(tree[i*2+2])
                    break

            else:
                if fit_number(tree[i*2+1]) == True:
                    practice(tree,data,i*2+1)
                else:
                    print(tree[i*2+1])
                    break
        i=i+1

if __name__ == '__main__':
    x = importDataforPractice('训练集.txt')
    tree = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #人工设定最大长度
    construct(tree,x,{1,2,3,4},0)
    print(tree)
    with open('测试集.txt') as file_obj:
        for line in file_obj:
            temp = line.split()
            for i in range(4):
                temp[i] = int(temp[i])
            practice(tree,temp,0)
            print('')






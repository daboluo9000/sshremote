# -*- coding:utf-8 -*0

a = [1, 2, 3]
for i in range(len(a)):
    if i == 0:
        a = a[:i] + a[i + 1:]
print(a)
#!/usr/bin/env python3
"""测试 Celery 任务"""

import sys
import os

# 确保 app 目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入任务
from celery.ctasks import add, multiply


def test_celery():
    """测试 Celery 任务"""
    print("开始测试 Celery 任务...")

    # 1. 发送加法任务
    print("发送加法任务: add.delay(1, 2)")
    result1 = add.delay(1, 2)
    print(f"任务ID: {result1.id}")

    # 2. 发送乘法任务
    print("\n发送乘法任务: multiply.delay(3, 4)")
    result2 = multiply.delay(3, 4)
    print(f"任务ID: {result2.id}")

    # 3. 获取结果（等待任务完成）
    import time
    time.sleep(2)

    if result1.ready():
        print(f"\n加法任务结果: {result1.get()}")
    else:
        print("加法任务还在处理中...")

    if result2.ready():
        print(f"乘法任务结果: {result2.get()}")
    else:
        print("乘法任务还在处理中...")


if __name__ == '__main__':
    print("确保 Worker 正在运行: celery -A app.ctasks worker --loglevel=info")
    test_celery()
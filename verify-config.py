#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash Meta 配置验证脚本
验证配置文件格式是否正确
"""

import yaml
import sys
import os

def verify_config():
    print("=" * 50)
    print("  Clash Meta 配置验证工具")
    print("=" * 50)
    print()
    
    error_count = 0
    
    # 1. 验证主配置文件
    print("[1/3] 验证主配置文件...", end=" ")
    try:
        with open('data/config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("✓ 通过")
    except Exception as e:
        print(f"✗ 失败")
        print(f"   错误：{str(e)}")
        error_count += 1
        return error_count
    
    # 2. 验证占位符文件
    print("[2/3] 验证占位符文件...", end=" ")
    try:
        with open('data/proxies/placeholder.yaml', 'r', encoding='utf-8') as f:
            placeholder = yaml.safe_load(f)
        print("✓ 通过")
    except Exception as e:
        print(f"✗ 失败")
        print(f"   错误：{str(e)}")
        error_count += 1
        return error_count
    
    # 3. 检查必要配置项
    print("[3/3] 检查必要配置项...", end=" ")
    required_fields = ['mixed-port', 'dns', 'rule-providers', 'proxy-groups', 'rules', 'proxy-providers']
    missing_fields = []
    
    for field in required_fields:
        if field not in config:
            missing_fields.append(field)
    
    if len(missing_fields) == 0:
        print("✓ 通过")
    else:
        print(f"✗ 缺少字段：{', '.join(missing_fields)}")
        error_count += 1
    
    print()
    print("=" * 50)
    
    if error_count == 0:
        print("✓ 验证成功！配置文件格式正确")
        print("=" * 50)
        return 0
    else:
        print(f"✗ 验证失败！发现 {error_count} 个错误")
        print("=" * 50)
        return 1

if __name__ == '__main__':
    sys.exit(verify_config())

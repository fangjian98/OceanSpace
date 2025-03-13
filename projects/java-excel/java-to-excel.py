import re
import os

def analyze_java_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 匹配变量 (简单正则)
    variable_pattern = r'(private|public|protected)\s+(\w+)\s+(\w+);'
    variables = re.findall(variable_pattern, content)

    # 匹配方法
    method_pattern = r'(private|public|protected)\s+(\w+)\s+(\w+)\((.*?)\)'
    methods = re.findall(method_pattern, content)

    print(f"File: {file_path}")
    print("\nVariables:")
    print(f"{'Scope':<10} {'Type':<10} {'Name':<10}")
    for var in variables:
        print(f"{var[0]:<10} {var[1]:<10} {var[2]:<10}")

    print("\nMethods:")
    print(f"{'Scope':<10} {'Return':<10} {'Name':<10} {'Parameters':<10}")
    for method in methods:
        print(f"{method[0]:<10} {method[1]:<10} {method[2]:<10} {method[3]:<10}")

# 扫描整个项目
def analyze_project(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                analyze_java_file(os.path.join(subdir, file))

# 替换为你的项目路径
project_path = "/home/server/code/app/FreemeFileManager/"
analyze_project(project_path)
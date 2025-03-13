import os
import re
import pandas as pd

# 缺点
# 1. 只能匹配 Java 基础类型，无法匹配自定义类型，如MediaType、List<FileInfo>
# 2. 函数方法匹配时出现很多 if-else，解析不正确

# 定义正则表达式
CONST_PATTERN = r"(public|protected|private)?\s+static\s+final\s+(\w+)\s+(\w+)\s*=\s*.+;"  # 常量
VAR_PATTERN = r"(private|protected|public)?\s*(static)?\s*(final)?\s*(\w+)\s+(\w+)\s*;"  # 变量
METHOD_PATTERN = r"(public|protected|private)?\s+(\w+)\s+(\w+)\s*\((.*?)\)\s*\{"  # 方法

# 定义扫描目录的函数
def scan_java_files(directory):
    java_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files

# 解析 Java 文件
def parse_java_file(file_path):
    constants = []
    variables = []
    methods = []

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # 提取常量
        for match in re.finditer(CONST_PATTERN, content):
            access_modifier, const_type, const_name = match.groups()[:3]
            constants.append({
                "文件名称": os.path.basename(file_path),
                "所在目录": os.path.dirname(file_path),
                "常量名称": const_name,
                "常量类型": const_type,
                "功能说明": "常量描述待补充"
            })

        # 提取变量
        for match in re.finditer(VAR_PATTERN, content):
            access_modifier, is_static, is_final, var_type, var_name = match.groups()
            variables.append({
                "文件名称": os.path.basename(file_path),
                "变量": var_name,
                "变量类型": var_type,
                "功能说明": "变量描述待补充"
            })

        # 提取方法
        for match in re.finditer(METHOD_PATTERN, content):
            access_modifier, return_type, method_name, params = match.groups()
            methods.append({
                "文件名称": os.path.basename(file_path),
                "函数": method_name,
                "功能": "函数描述待补充",
                "格式": f"{return_type} {method_name}({params})",
                "参数": params,
                "全局变量": "待补充",
                "局部变量": "待补充",
                "返回值": return_type
            })

    return constants, variables, methods

# 主函数
def main(java_project_dir, output_excel_file):
    java_files = scan_java_files(java_project_dir)
    all_constants = []
    all_variables = []
    all_methods = []

    for java_file in java_files:
        constants, variables, methods = parse_java_file(java_file)
        all_constants.extend(constants)
        all_variables.extend(variables)
        all_methods.extend(methods)

    # 保存为 Excel 文件
    with pd.ExcelWriter(output_excel_file) as writer:
        pd.DataFrame(all_constants).to_excel(writer, sheet_name="常量", index=False)
        pd.DataFrame(all_variables).to_excel(writer, sheet_name="变量", index=False)
        pd.DataFrame(all_methods).to_excel(writer, sheet_name="函数", index=False)

    print(f"解析完成，结果已保存到 {output_excel_file}")

# 执行脚本
if __name__ == "__main__":
    java_project_dir = "/home/server/code/app/FreemeNotes"  # 替换为你的 Java 项目目录路径
    output_excel_file = "java_project_analysis_note.xlsx"  # 输出文件名
    main(java_project_dir, output_excel_file)
import os
import re
import pandas as pd

# 改进的正则表达式模式
CONST_PATTERN = r"(public|protected|private)?\s+static\s+final\s+([<>?\w\s,]+)\s+(\w+)\s*=\s*.+;"  # 支持泛型的常量模式

VAR_PATTERN = r"(private|protected|public)?\s*(static)?\s*(final)?\s*([<>?\w\s,]+)\s+(\w+)\s*;"  # 支持泛型的变量模式

# 改进的方法模式，增加了更严格的匹配
METHOD_PATTERN = r"(public|protected|private)?\s*(static)?\s*([<>?\w\s,]+)\s+(\w+)\s*\(([\s\S]*?)\)\s*(?=\{)"

# 排除模式，用于过滤掉if/else等条件语句
EXCLUDE_PATTERNS = [
    r"\s*if\s*\(.*\)\s*\{",
    r"\s*else\s*\{",
    r"\s*else\s+if\s*\(.*\)\s*\{",
    r"\s*while\s*\(.*\)\s*\{",
    r"\s*for\s*\(.*\)\s*\{",
    r"\s*switch\s*\(.*\)\s*\{",
    r"\s*catch\s*\(.*\)\s*\{",
    r"\s*synchronized\s*\(.*\)\s*\{"
]


def clean_type(type_str):
    """清理类型字符串，移除多余的空格"""
    return ' '.join(type_str.split())


def is_control_structure(line):
    """检查是否是控制结构"""
    return any(re.match(pattern, line) for pattern in EXCLUDE_PATTERNS)


def scan_java_files(directory):
    java_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files


def parse_parameters(params_str):
    """解析方法参数"""
    if not params_str.strip():
        return ""
    params = []
    current_param = []
    bracket_count = 0

    for char in params_str:
        if char == '<':
            bracket_count += 1
        elif char == '>':
            bracket_count -= 1
        elif char == ',' and bracket_count == 0:
            params.append(''.join(current_param).strip())
            current_param = []
            continue
        current_param.append(char)

    if current_param:
        params.append(''.join(current_param).strip())

    return ', '.join(params)


def parse_java_file(file_path):
    constants = []
    variables = []
    methods = []

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # 移除注释
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)  # 移除多行注释
        content = re.sub(r'//.*', '', content)  # 移除单行注释

        # 提取常量
        for match in re.finditer(CONST_PATTERN, content):
            access_modifier, const_type, const_name = match.groups()[:3]
            if const_type and const_name:
                constants.append({
                    "文件名称": os.path.basename(file_path),
                    "所在目录": os.path.dirname(file_path),
                    "常量名称": const_name,
                    "常量类型": clean_type(const_type),
                    "功能说明": "常量描述待补充"
                })

        # 提取变量
        for match in re.finditer(VAR_PATTERN, content):
            access_modifier, is_static, is_final, var_type, var_name = match.groups()
            if var_type and var_name and not is_control_structure(match.group(0)):
                variables.append({
                    "文件名称": os.path.basename(file_path),
                    "变量": var_name,
                    "变量类型": clean_type(var_type),
                    "功能说明": "变量描述待补充"
                })

        # 提取方法
        method_matches = re.finditer(METHOD_PATTERN, content)
        for match in method_matches:
            if not is_control_structure(match.group(0)):
                access_modifier, is_static, return_type, method_name, params = match.groups()
                if return_type and method_name:
                    methods.append({
                        "文件名称": os.path.basename(file_path),
                        "函数": method_name,
                        "功能": "函数描述待补充",
                        "格式": f"{clean_type(return_type)} {method_name}({parse_parameters(params)})",
                        "参数": parse_parameters(params),
                        "全局变量": "待补充",
                        "局部变量": "待补充",
                        "返回值": clean_type(return_type)
                    })

    return constants, variables, methods


def main(java_project_dir, output_excel_file):
    java_files = scan_java_files(java_project_dir)
    all_constants = []
    all_variables = []
    all_methods = []

    for java_file in java_files:
        try:
            constants, variables, methods = parse_java_file(java_file)
            all_constants.extend(constants)
            all_variables.extend(variables)
            all_methods.extend(methods)
        except Exception as e:
            print(f"处理文件 {java_file} 时出错: {str(e)}")

    # 保存为 Excel 文件
    with pd.ExcelWriter(output_excel_file) as writer:
        pd.DataFrame(all_constants).to_excel(writer, sheet_name="常量", index=False)
        pd.DataFrame(all_variables).to_excel(writer, sheet_name="变量", index=False)
        pd.DataFrame(all_methods).to_excel(writer, sheet_name="函数", index=False)

    print(f"解析完成，结果已保存到 {output_excel_file}")


if __name__ == "__main__":
    java_project_dir = "/home/server/code/app/FreemeNotes"  # 替换为你的 Java 项目目录路径
    output_excel_file = "java_project_analysis_note.xlsx"  # 输出文件名
    main(java_project_dir, output_excel_file)
import os
import re
import pandas as pd

# 改进的正则表达式模式
CONST_PATTERN = r"(?:public|protected|private)?\s+static\s+final\s+([<>?\w\s,]+)\s+(\w+)\s*=\s*.+;"

# 改进的变量模式
VAR_PATTERN = r"(?:private|protected|public)?\s*(?:static)?\s*(?:final)?\s*([<>?\w\s,]+)\s+(\w+)\s*(?:=\s*[^;]+)?;"

# 改进的方法模式，更准确的匹配
METHOD_PATTERN = r"(?:public|protected|private)?\s*(?:static)?\s*(?:abstract\s+)?([<>?\w\s,]+)\s+(\w+)\s*\(([\s\S]*?)\)\s*(?:throws\s+[\w\s,]+\s*)?(?=\{|;)"

# 排除关键字
EXCLUDE_KEYWORDS = {
    'if', 'else', 'for', 'while', 'switch', 'catch', 'finally', 'synchronized',
    'return', 'break', 'continue', 'throw', 'assert', 'case', 'default'
}

# 有效的Java类型集合
VALID_JAVA_TYPES = {
    'void', 'boolean', 'byte', 'char', 'short', 'int', 'long', 'float', 'double',
    'String', 'Object', 'Boolean', 'Byte', 'Character', 'Short', 'Integer', 'Long',
    'Float', 'Double', 'List', 'Map', 'Set', 'Collection', 'ArrayList', 'HashMap',
    'HashSet', 'Vector', 'LinkedList', 'TreeMap', 'TreeSet', 'StringBuilder',
    'StringBuffer', 'View', 'ViewGroup', 'Context', 'Activity', 'Fragment',
    'Intent', 'Bundle', 'Cursor', 'Handler', 'Thread', 'Runnable', 'Exception',
    'RuntimeException', 'Button', 'TextView', 'EditText', 'ImageView', 'LinearLayout',
    'RelativeLayout', 'FrameLayout', 'RecyclerView', 'ListView', 'GridView'
}


def clean_type(type_str):
    """清理并验证类型字符串"""
    if not type_str:
        return ""
    cleaned = ' '.join(type_str.split())
    base_type = re.sub(r'<.*>', '', cleaned).split()[0]
    if base_type in EXCLUDE_KEYWORDS:
        return ""
    return cleaned


def clean_name(name):
    """清理并验证名称"""
    if not name:
        return ""
    name = name.strip()
    if not re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', name) or name in EXCLUDE_KEYWORDS:
        return ""
    return name


def is_valid_java_type(type_str):
    """验证是否是有效的Java类型"""
    if not type_str:
        return False

    # 清理类型字符串
    base_type = re.sub(r'<.*>', '', type_str.strip()).split()[0]

    # 检查是否是已知的Java类型
    if base_type in VALID_JAVA_TYPES:
        return True

    # 检查是否是自定义类型（首字母大写）
    if re.match(r'^[A-Z][a-zA-Z0-9_$]*$', base_type):
        return True

    return False


def parse_parameters(params_str):
    """解析方法参数"""
    if not params_str or params_str.isspace():
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
            param = ''.join(current_param).strip()
            if param:
                params.append(param)
            current_param = []
            continue
        current_param.append(char)

    if current_param:
        param = ''.join(current_param).strip()
        if param:
            params.append(param)

    valid_params = []
    for param in params:
        param_parts = param.split()
        if len(param_parts) >= 2:
            param_type = param_parts[0]
            if is_valid_java_type(param_type):
                valid_params.append(param)

    return ', '.join(valid_params)


def remove_comments_and_strings(content):
    """移除注释、字符串字面量和注解"""
    # 移除多行注释
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    # 移除单行注释
    content = re.sub(r'//.*', '', content)
    # 移除字符串字面量
    content = re.sub(r'"(?:\\.|[^"\\])*"', '""', content)
    # 移除注解
    content = re.sub(r'@\w+(?:\([^)]*\))?', '', content)
    return content


def extract_method_info(match, return_type):
    """提取方法信息"""
    try:
        method_name = match.group(2)
        params = match.group(3)

        # 验证方法名
        method_name = clean_name(method_name)
        if not method_name or method_name in EXCLUDE_KEYWORDS:
            return None

        # 验证返回类型
        return_type = clean_type(return_type)
        if not return_type and return_type != 'void':
            return None

        return {
            "函数": method_name,
            "功能": "函数描述待补充",
            "格式": f"{return_type} {method_name}({parse_parameters(params)})",
            "参数": parse_parameters(params),
            "全局变量": "待补充",
            "局部变量": "待补充",
            "返回值": return_type
        }
    except Exception:
        return None


def parse_java_file(file_path):
    constants = []
    variables = []
    methods = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 预处理内容
        content = remove_comments_and_strings(content)

        # 提取常量
        for match in re.finditer(CONST_PATTERN, content):
            try:
                const_type, const_name = match.groups()
                const_type = clean_type(const_type)
                const_name = clean_name(const_name)

                if const_type and const_name and is_valid_java_type(const_type):
                    constants.append({
                        "文件名称": os.path.basename(file_path),
                        "所在目录": os.path.dirname(file_path),
                        "常量名称": const_name,
                        "常量类型": const_type,
                        "功能说明": "常量描述待补充"
                    })
            except Exception:
                continue

        # 提取变量
        for match in re.finditer(VAR_PATTERN, content):
            try:
                var_type, var_name = match.groups()
                var_type = clean_type(var_type)
                var_name = clean_name(var_name)

                if var_type and var_name and is_valid_java_type(var_type):
                    variables.append({
                        "文件名称": os.path.basename(file_path),
                        "变量": var_name,
                        "变量类型": var_type,
                        "功能说明": "变量描述待补充"
                    })
            except Exception:
                continue

        # 提取方法
        for match in re.finditer(METHOD_PATTERN, content):
            try:
                return_type = match.group(1)
                method_info = extract_method_info(match, return_type)

                if method_info:
                    method_info["文件名称"] = os.path.basename(file_path)
                    methods.append(method_info)
            except Exception:
                continue

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

    return constants, variables, methods


def main(java_project_dir, output_excel_file):
    java_files = []
    all_constants = []
    all_variables = []
    all_methods = []

    # 扫描Java文件
    try:
        for root, _, files in os.walk(java_project_dir):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"扫描目录时出错: {str(e)}")
        return

    # 处理每个文件
    for java_file in java_files:
        try:
            constants, variables, methods = parse_java_file(java_file)
            all_constants.extend(constants)
            all_variables.extend(variables)
            all_methods.extend(methods)
        except Exception as e:
            print(f"处理文件 {java_file} 时出错: {str(e)}")
            continue

    # 保存结果
    try:
        with pd.ExcelWriter(output_excel_file) as writer:
            pd.DataFrame(all_constants).to_excel(writer, sheet_name="常量", index=False)
            pd.DataFrame(all_variables).to_excel(writer, sheet_name="变量", index=False)
            pd.DataFrame(all_methods).to_excel(writer, sheet_name="函数", index=False)
        print(f"解析完成，结果已保存到 {output_excel_file}")
    except Exception as e:
        print(f"保存Excel文件时出错: {str(e)}")


if __name__ == "__main__":
    java_project_dir = "/home/server/code/app/FreemeNotes"
    output_excel_file = "java_project_analysis_note.xlsx"
    main(java_project_dir, output_excel_file)
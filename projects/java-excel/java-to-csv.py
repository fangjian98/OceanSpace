import os
import javalang
from prettytable import PrettyTable


def parse_java_file(file_path):
    """
    解析单个 Java 文件，提取类、变量和方法信息
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    try:
        tree = javalang.parse.parse(content)
    except (javalang.parser.JavaSyntaxError, Exception) as e:
        print(f"Error parsing {file_path}: {e}")
        return []

    parsed_data = []

    for path, node in tree:
        if isinstance(node, javalang.tree.ClassDeclaration):
            class_name = node.name
            variables = []
            methods = []

            # 提取类中的变量
            for field in node.fields:
                for decl in field.declarators:
                    variable_info = {
                        'name': decl.name,
                        'type': field.type.name,
                        'visibility': field.modifiers
                    }
                    variables.append(variable_info)

            # 提取类中的方法
            for method in node.methods:
                method_info = {
                    'name': method.name,
                    'parameters': [(param.type.name, param.name) for param in method.parameters],
                    'return_type': method.return_type.name if method.return_type else 'void',
                    'visibility': method.modifiers,
                    'description': method.documentation if method.documentation else 'N/A'
                }
                methods.append(method_info)

            parsed_data.append({
                'class_name': class_name,
                'variables': variables,
                'methods': methods
            })

    return parsed_data


def parse_project_directory(directory):
    """
    遍历项目目录，解析所有 .java 文件
    """
    all_parsed_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                parsed_data = parse_java_file(file_path)
                all_parsed_data.extend(parsed_data)
    return all_parsed_data


def display_parsed_data(parsed_data):
    """
    将解析结果以表格方式输出
    """
    for class_data in parsed_data:
        print(f"\nClass: {class_data['class_name']}\n")

        # 输出变量信息
        if class_data['variables']:
            print("Variables:")
            table = PrettyTable()
            table.field_names = ["Variable Name", "Type", "Visibility"]
            for var in class_data['variables']:
                table.add_row([var['name'], var['type'], ', '.join(var['visibility'])])
            print(table)

        # 输出方法信息
        if class_data['methods']:
            print("Methods:")
            table = PrettyTable()
            table.field_names = ["Method Name", "Parameters", "Return Type", "Visibility", "Description"]
            for method in class_data['methods']:
                parameters = ', '.join([f"{ptype} {pname}" for ptype, pname in method['parameters']])
                table.add_row([method['name'], parameters, method['return_type'], ', '.join(method['visibility']),
                               method['description']])
            print(table)


if __name__ == "__main__":
    # 替换为你的 Java 项目目录
    project_directory = "/home/server/Desktop/T750U/FreemeNotes/"
    parsed_data = parse_project_directory(project_directory)
    display_parsed_data(parsed_data)
from wuling.tool.http_parser import parse_http_file


def generate_test_case(txt_file, case_path):
    parse_http_file(txt_file, case_path)

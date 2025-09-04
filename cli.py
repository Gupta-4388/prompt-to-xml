from prompt_to_xml.converter import convert_to_xml
import argparse

def main():
    parser = argparse.ArgumentParser(description="Prompt to XML CLI")
    parser.add_argument("prompt", type=str, help="The natural language prompt")
    args = parser.parse_args()

    xml_output = convert_to_xml(args.prompt)
    print(xml_output)

if __name__ == "__main__":
    main()

from prompt_to_xml.converter import convert_to_xml

def handler(request):
    if request.method == "POST":
        try:
            data = request.json()
            prompt = data.get("prompt", "")
            xml_output = convert_to_xml(prompt)
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": {"xml": xml_output},
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": {"error": str(e)},
            }
    else:
        return {
            "statusCode": 405,
            "body": {"error": "Method not allowed"},
        }

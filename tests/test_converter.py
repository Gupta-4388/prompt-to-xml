from prompt_to_xml.converter import convert_to_xml

def test_basic_conversion():
    prompt = "Book a flight to Berlin on Oct 1st. It's urgent."
    xml = convert_to_xml(prompt)
    assert "<query>" in xml
    assert "<intent>" in xml

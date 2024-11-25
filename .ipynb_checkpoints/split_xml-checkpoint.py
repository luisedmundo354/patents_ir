from lxml import etree

def process_xml_file(input_file_path):
    file_counter = 0

    with open(input_file_path, 'r') as file:
        xml_content = file.read()

    # Split the document
    sections = xml_content.split('<!DOCTYPE')

    for section in sections:
        if section.strip():
            section = '<!DOCTYPE' + section if file_counter > 0 else section

            # Parse the section
            parser = etree.XMLParser(recover=True)
            try:
                tree = etree.fromstring(section, parser=parser)

                # Extract the patent number
                doc_number_elem = tree.find('.//doc-number')
                patent_number = doc_number_elem.text.strip() if doc_number_elem is not None else f'unknown_{file_counter}'

                # Define the output file name
                output_file_name = f'xml_patents_wn/{patent_number}.xml'
                with open(output_file_name, 'w') as output_file:
                    output_file.write(etree.tostring(tree, pretty_print=True, encoding='unicode'))
            except Exception as e:
                print(f"Error processing section {file_counter}: {e}")

            file_counter += 1

    return "Processing completed"
from lxml import etree

def extract_text(element):
    """Helper function to extract text from an element and its children."""
    texts = [(element.text or "").strip()]
    for child in element:
        if child.tag == 'claim-ref':
            texts.append((child.text or "").strip())
        if child.tail:
            texts.append((child.tail or "").strip())
    return ' '.join(filter(None, texts))

def print_claim_texts(element, level=0):
    """Recursively print each claim-text, including text after claim-ref."""
    if element.tag == 'claim-text':
        print("  " * level + extract_text(element))
    for child in element:
        print_claim_texts(child, level + 1)

def print_tag_text(tag_name, root):
    for element in root.findall(f'.//{tag_name}'):
        if element.text:
            print(f"{tag_name}: {element.text.strip()}")

def print_citation_doc_numbers(root):
    for idx, doc_number in enumerate(root.xpath('.//citation//patcit//document-id//doc-number'), 1):
        print(f"Citation {idx}: Document Number {doc_number.text.strip()}")

def print_patent(path):
    try:
        with open(path, 'rb') as file:
            tree = etree.parse(file, etree.XMLParser(recover=True))
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return

    patent_details = {
        "Patent Name": './/invention-title',
        "Patent Number": './/doc-number',
        "Patent Abstract": './/abstract/p',
        "Patent U.S. CI. Main classification": './/main-classification'
    }

    for detail, xpath in patent_details.items():
        element = root.find(xpath)
        if element is not None and element.text:
            print(f"{detail}: {element.text.strip()}")
        else:
            print(f"No {detail.lower()} found.")

    print("Patent International Classification:")
    for tag in [
        'classification-level', 'section', 'class', 'subclass',
        'main-group', 'subgroup', 'further-classification'
    ]:
        print_tag_text(tag, root)

    for claim in root.findall('.//claim'):
        print(f"Claim {claim.get('num')}:")
        print_claim_texts(claim)
        print()

    try:
        print_citation_doc_numbers(root)
    except Exception as e:
        print(f"Error processing citations: {e}")
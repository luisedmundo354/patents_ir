from lxml import etree
from patent_model import Patent, InternationalClassification, Claims
import json

def extract_and_convert_to_json(xml_path: str) -> str:
    try:
        with open(xml_path, 'rb') as file:
            tree = etree.parse(file, etree.XMLParser(recover=True))
        root = tree.getroot()
        international_classifications = parse_international_classifications(root)
        title = root.find('.//invention-title').text.strip() if root.find('.//invention-title') is not None else ""
        abstract = root.find('.//abstract/p').text.strip() if root.find('.//abstract/p') is not None else ""
        inventors = [e.text.strip() for e in root.findall('.//applicant/addressbook/last-name') if e.text]
        document_number = root.find('.//doc-number').text.strip() if root.find('.//doc-number') is not None else ""
        publication_date = root.find('.//date').text.strip() if root.find('.//date') is not None else ""
        assignees = [e.text.strip() for e in root.findall('.//assignees/assignee/addressbook/orgname') if e.text]
        #claims = [extract_claim_text(claim) for claim in root.findall('.//claim//claim-text')]
        description = [''.join(e.itertext()).strip() for e in root.findall('.//description//p')]
        citations = [e.text.strip() for e in root.findall('.//citation//document-id//doc-number')]
        us_classification = root.find('.//main-classification').text.strip() if root.find('.//main-classification') is not None else ""
        claims_elements = root.findall('.//claim')
        claims = []
        
        for claim_element in claims_elements:
            claim_number = claim_element.get('id', '')
            #print(claim_number)
        
            preamble_element = claim_element.find('.//claim-text')
            if preamble_element is not None:
                # Get text directly under claim-text
                preamble_text_parts = [preamble_element.text.strip() if preamble_element.text else ""]
        
                ref_text_elements = preamble_element.findall('.//claim-ref')
                for ref_text in ref_text_elements:
                    if ref_text.text:
                        preamble_text_parts.append(ref_text.text.strip())
        
                    # If there's tail text (text following </ref-text>)
                    if ref_text.tail:
                        preamble_text_parts.append(ref_text.tail.strip())
        
                # Join all preamble parts including ref-text
                preamble = " ".join(preamble_text_parts)
            
            components = []
            component_elements = preamble_element.findall('.//claim-text') if preamble_element is not None else []
            for comp in component_elements:
                component_text = comp.text.strip() if comp.text else ""
                subcomponents = []
                for sub in comp.findall('.//claim-text'):
                    sub_text = sub.text.strip() if sub.text else ""
                    subcomponents.append(sub_text)
                
                components.append({"component": component_text, "subcomponents": subcomponents})
            
            claim = Claims(claim_number=claim_number, preamble=preamble, components=components)
            claims.append(claim)

        patent = Patent(
            title=title,
            abstract=abstract,
            inventors=inventors,
            document_number=document_number,
            publication_date=publication_date,
            assignees=assignees,
            claims=claims,
            description=description,
            citations=citations,
            international_classifications=international_classifications,
            us_classification=us_classification
        )
        
        return patent.to_json(), patent

    except Exception as e:
        print(f"Error processing XML: {e}")
        return ""

def extract_preamble(claim_element):
    """Helper function to extract the preamble from a claim."""
    return (claim_element.find('claim-text').text or "").strip().split('.')[0] if claim_element.find('claim-text') is not None else ""

def extract_components(claim_element):
    """Helper function to extract components from a claim."""
    components = []
    component_elements = claim_element.findall('.//claim-text//claim-ref')
    for comp in component_elements:
        components.append({"component": comp.text.strip(), "subcomponents": []})
    return components

def parse_international_classifications(root):
    classifications = []
    classification_level = root.find('.//classification-level').text.strip() if root.find('.//classification-level') is not None else ""
    section = root.find('.//section').text.strip() if root.find('.//section') is not None else ""
    classification_class = root.find('.//class').text.strip() if root.find('.//class') is not None else ""
    subclass = root.find('.//subclass').text.strip() if root.find('.//subclass') is not None else ""
    main_group = root.find('.//main-group').text.strip() if root.find('.//main-group') is not None else ""
    subgroup = root.find('.//subgroup').text.strip() if root.find('.//subgroup') is not None else ""
    
    classifications.append(InternationalClassification(
        classification_level=classification_level,
        section=section,
        classification_class=classification_class,
        subclass=subclass,
        main_group=main_group,
        subgroup=subgroup
    ))
    return classifications

def json_to_patent(json_data: str) -> Patent:
    data = json.loads(json_data)
    
    international_classifications = [
        InternationalClassification(**ic) for ic in data.get('international_classifications', [])
    ]
    
    patent = Patent(
        title=data.get('title', ""),
        abstract=data.get('abstract', ""),
        inventors=data.get('inventors', []),
        document_number=data.get('document_number', ""),
        publication_date=data.get('publication_date', ""),
        assignees=data.get('assignees', []),
        claims=data.get('claims', []),
        description=data.get('description', []),
        citations=data.get('citations', []),
        us_classification=data.get('us_classification', ""),
        international_classifications=international_classifications
    )
    return patent
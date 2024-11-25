from dataclasses import dataclass, field
from typing import List, Dict, Any
import json

@dataclass
class InternationalClassification:
    classification_level: str = ""
    section: str = ""
    classification_class: str = ""
    subclass: str = ""
    main_group: str = ""
    subgroup: str = ""

    def to_dict(self):
        """Converts the International Classification to a dictionary."""
        return {
            "classification_level": self.classification_level,
            "section": self.section,
            "classification_class": self.classification_class,
            "subclass": self.subclass,
            "main_group": self.main_group,
            "subgroup": self.subgroup
        }

@dataclass
class Claims:
    claim_number: str = ""
    preamble: str = ""
    components: List[Dict[str, Any]] = field(default_factory=list)

    def add_component(self, component_name: str, subcomponents: List[Dict[str, List[str]]] = None):
        if subcomponents is None:
            subcomponents = []
        self.components.append({
            "component": component_name,
            "subcomponents": subcomponents
        })

    def to_dict(self):
        return {
            "claim_number": self.claim_number,
            "preamble": self.preamble,
            "components": self.components
        }

@dataclass
class Patent:
    title: str = ""
    abstract: str = ""
    inventors: List[str] = field(default_factory=list)
    document_number: str = ""
    publication_date: str = ""
    assignees: List[str] = field(default_factory=list)
    claims: List[Any] = field(default_factory=list) 
    description: List[str] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)
    us_classification: str = ""
    international_classifications: List[InternationalClassification] = field(default_factory=list)

    def to_json(self) -> str:
        """Converts the patent to a JSON string."""
        patent_dict = {
            "title": self.title,
            "abstract": self.abstract,
            "inventors": self.inventors,
            "document_number": self.document_number,
            "publication_date": self.publication_date,
            "assignees": self.assignees,
            "claims": [claim.to_dict() for claim in self.claims],
            "description": self.description,
            "citations": self.citations,
            "us_classification": self.us_classification,
            "international_classifications": [ic.to_dict() for ic in self.international_classifications]
        }
        return json.dumps(patent_dict, indent=4)
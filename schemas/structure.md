MIM
│
├── Foundation Layer
│   │
│   └── common.yaml                                            (checked)
│
├── Ontology Support Layer
│   │
│   ├── ontology_source.yaml
│   ├── ontology_term.yaml
│   └── prefix_association.yaml
│
├── People & Organization Layer
│   │
│   ├── agent.yaml                                             (checked)
│   ├── institution.yaml                                       (checked)
│   └── attribution.yaml                                       (checked)
│
├── Governance & Provenance Layer
│   │
│   ├── license.yaml                                           (checked)
│   ├── funding.yaml
│   ├── grant_reference.yaml
│   └── external_reference.yam                                 (checked)
│
├── Experimental Workflow Layer
│   │
│   ├── project.yaml
│   ├── investigation.yaml
│   ├── study.yaml
│   │   ├── study_design.yaml
│   │   └── factor.yaml
│   │
│   ├── assay.yaml
│   ├── process.yaml
│   │   └── parameter_value.yaml                               
│   │
│   └── protocol.yaml
│       ├── protocol_component.yaml                            (checked)
│       │   ├── hardware_component.yaml                        (checked)
│       │   ├── software_component.yaml                        (checked)
│       │   └── reagent_component.yaml                         (checked)
│       └── parameter_specification.yaml                       (checked)
│
├── Biological Material Layer
│   │
│   ├── material.yaml
│   ├── organism.yaml
│   ├── strain.yaml
│   │
│   └── sample.yaml
│       ├── sample_characteristic_definition.yaml
│       └── sample_characteristic_value.yaml
│
├── Measurement Layer
│   │
│   ├── measurement.yaml
│   ├── value.yaml
│   ├── quantity_value.yaml
│   ├── numeric_value.yaml
│   ├── categorical_value.yaml
│   ├── text_value.yaml
│   └── date_value.yaml
│
├── Research Asset Layer
│   │
│   ├── asset.yaml                                             (checked)
│   │
│   ├── data_file.yaml
│   ├── workflow.yaml
│   ├── model.yaml
│   ├── sop.yaml                                               (checked)
│   ├── publication.yaml
│   ├── document.yaml
│   └── presentation.yaml
│
├── Extension Mechanism
│   │
│   └── profile_specific_metadata.yaml
│
└── Domain Profile Layer
    │
    ├── bioimaging
    ├── flocytometry
    ├── proteomics
    ├── metabolomics
    └── genomics










ProjectProject
   │
   ▼
Investigation
   │
   ▼
Study
   │
   ├── StudyDesign
   ├── Factor
   │
   ▼
Assay
   │
   ├── Sample
   │      └── Characteristics
   │
   ├── Process
   │      │
   │      ├── Protocol
   │      │      └── ParameterSpecification
   │      │
   │      ├── ParameterValue
   │      │
   │      └── Measurement
   │
   └── Research Assets
           ├── DataFile
           ├── Workflow
           ├── Model
           ├── SOP
           ├── Publication
           ├── Document
           └── Presentation
MIM-schema
│
├── Foundation Layer
│   │
│   └── common.yaml                                            (checked)
│
├── Ontology Support Layer
│   │
│   ├── ontology_source.yaml
│   └── ontology_term.yaml
│
├── People & Organization Layer
│   │
│   ├── agent.yaml                                             (checked)
│   └── institution.yaml                                       (checked)
│
├── Governance & Provenance Layer
│   │
│   ├── license.yaml                                           (checked)
│   ├── funding.yaml                                           (checked)
│   └── external_reference.yam                                 (checked)
│
├── Experimental Workflow Layer
│   │
│   ├── project.yaml                                           (checked)
│   ├── investigation.yaml                                     (checked)
│   ├── study.yaml                                             (checked)
│   │   ├── study_design.yaml                                  (checked)
│   │   └── factor.yaml                                        (checked)        
│   │
│   ├── assay.yaml                                             (checked) 
│   ├── process.yaml                                           (checked)
    │   ├── treatment.yaml                                     (checked)
│   │   └── parameter_value.yaml                               (checked)
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
│   ├── material.yaml                                          (checked)
│   │   └── sample.yaml                                        (checked)
│   │       ├── sample_characteristic_definition.yaml          (checked)
│   │       └── sample_characteristic_value.yaml               (checked)
│   ├── organism.yaml                                          (checked) 
│   └── strain.yaml                                            (checked) 
│
├── Measurement Layer
│   │
│   └── measurement.yaml                                       (checked)
│   └── value.yaml                                             (checked)
│       ├── quantity_value.yaml                                (checked)
│       ├── categorical_value.yaml                             (checked)
│       ├── text_value.yaml                                    (checked)
│       └── date_value.yaml                                    (checked)
│
├── Research Asset Layer
│   │
│   └── asset.yaml                                             (checked)
│       ├── data_file.yaml                                     (checked)
│       ├── workflow.yaml                                      (checked)
│       ├── model.yaml                                         (checked)
│       ├── sop.yaml                                           (checked)
│       ├── publication.yaml                                   (checked)
│       ├── document.yaml                                      (checked)
│       ├── presentation.yaml                                  (checked)
│       │
│       └── file_format.yaml                                   (checked)
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


===================================================================================================
                                      MIM CORE SCHEMA ARCHITECTURE
===================================================================================================

       +-------------------------------------------------------------------------------+
       |                                   MIMProject                                  |
       |  (institutions, members, funding, seek_id, web_link, attribution)             |
       +---------------------------------------+---------------------------------------+
                                               | (investigations)
                                               v
       +-------------------------------------------------------------------------------+
       |                                MIMInvestigation                               |
       |  (studies, publications, funding, attribution)                                |
       +---------------------------------------+---------------------------------------+
                                               | (studies)
                                               v
       +-------------------------------------------------------------------------------+
       |                                    MIMStudy                                   |
       |  (design, assays, publications, funding, license, attribution)                |
       +-------------------+-----------------------------------+-----------------------+
                           | (design)                          | (assays)
                           v                                   v
             +---------------------------+   +------------------------------------+
             |      MIMStudyDesign       |   |              MIMAssay              |
             |  (design_type, factors)   |   | (assay_type, technology_type,      |
             +-------------+-------------+   |  processes, samples, attribution)  |
                           |                 +--------+------------------+---------+
                           v                          |                  |
                   +---------------+                  |                  |
                   |   MIMFactor   |                  |                  |
                   +---------------+                  |                  |
                                                      |                  |
            +-----------------------------------------+                  |
            | (processes)                                                | (samples)
            v                                                            v
+-----------------------+     input / output    +-----------------------------------------------+
|      MIMProcess       |<--------------------->|                   MIMSample                   |
|  (protocol,           |                       | (is_a MIMMaterial)                            |
|   performers,         |                       | (organism, strain, characteristics,           |
|   parameter_values,   |                       |  derived_from)                                |
|   measurements)       |                       +------------------------+----------------------+
+-----------+-----------+                                                |
            |                                                            |
            | (uses protocol)                                            v
            v                                           +---------------------------------+
+-----------------------+                               |           MIMOrganism           |
|      MIMProtocol      |                               | (taxon, strain)                 |
|  (is_a MIMAsset)      |                               +---------------------------------+
|  (components,         |
|   parameters)         |
+-----------+-----------+
            |
            | (components)
            v
+-----------------------+-----------------------+
|                 MIMProtocolComponent                  |
|                 (abstract base class)                 |
+-----------+-------------------+-----------------------+
            |                   |                       |
            v                   v                       v
+-----------------------+ +-------------------+ +-----------------------+
|  MIMHardwareComponent | | MIMSoftwareComponent| |  MIMReagentComponent  |
|  (manufacturer, model)| | (repository_url)  | |  (catalog, lot_number)|
+-----------------------+ +-------------------+ +-----------------------+


===================================================================================================
                             ASSET & VALUE INHERITANCE HIERARCHIES
===================================================================================================

                    +------------------------------------------+
                    |                 MIMAsset                 |
                    | (abstract: asset_type, license, seek_id, |
                    |  attribution, external_references)       |
                    +--------------------+---------------------+
                                         |
     +-----------------+-----------------+-----------------+-----------------+
     |                 |                 |                 |                 |
     v                 v                 v                 v                 v
+----------+     +------------+    +-----------+    +-------------+    +------------+
|MIMProtocol|    |MIMDataFile |    | MIMModel  |    |MIMPublication|   |MIMWorkflow |
| (MIMSOP) |     +------------+    +-----------+    +-------------+    |MIMDocument |
+----------+                                                           |MIMPresentat.|
                                                                       +------------+


                    +------------------------------------------+
                    |                 MIMValue                 |
                    |  (abstract: value_type, unit)            |
                    +--------------------+---------------------+
                                         |
     +-------------------+---------------+-------------------+
     |                   |                                   |
     v                   v                                   v
+------------------+  +-------------------+        +--------------------+
| MIMQuantityValue |  |MIMCategoricalValue|        |    MIMTextValue    |
| (numeric_value)  |  |  (term_value)     |        |    (text_value)    |
+------------------+  +-------------------+        +--------------------+
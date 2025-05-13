# ISA and REMBI Compliant Modular Metadata Schemas

## The problem

Biological imaging can drive significant biomedical breakthroughs. However, images captured by one laboratory are often not **"interoperable"** and cannot be readily interpreted or utilized by others, leading to inefficiencies and slowing down scientific advances.

**At the heart of this interoperability crisis lies a metadata gap**. High-quality imaging experiments require rich metadata (from experimental conditions to analytical methods) to ensure rigor, reproducibility, interpretability, and data reuse. Without harmonized approaches to capture and share this contextual information, valuable images lose scientific utility.

The [**REMBI recommendations**](https://www.ebi.ac.uk/bioimage-archive/rembi-help-overview/) (REcommended Metadata for Biological Images) offer a framework for the bioimaging community to standardize imaging metadata collection, enhancing both pre-publication data management and post-publication archiving and reuse. Developed as a community-driven initiative, REMBI addresses a broad range of bioimaging use cases and is supported by public repositories like the [BioImage Archive (BIA)](https://www.ebi.ac.uk/bioimage-archive/rembi-model-reference/). However, a key limitation of REMBI is its lack of support for integrating bioimaging data with multiomics datasets.

The [**ISA framework**](https://doi.org/10.1093/bioinformatics/btq415) (Investigation-Study-Assay) is a [general-purpose metadata format](https://isa-tools.org/format/specification.html) designed to standardize experimental data management. It facilitates bottom-up metadata curation, supports community-defined reporting standards, and streamlines submissions to public repositories. However, a key limitation of ISA is its lack of native support for imaging experiments.

## The solution
This project aims to enable community-driven standardization by establishing consistent metadata practices for biological imaging while maintaining flexibility for diverse research needs. Our approach combines the strengths of both ISA and REMBI frameworks while employing modular schema design to **promote the emergence of sustainable, community-driven, bottom-up standards**. 

As a first step, this repository provides a **collaborative platform for sharing modular metadata schemas** built upon the ISA and REMBI frameworks, and making them available in user-friendly formats, including CSV, TAB, and [**LinkML (YAML)**](https://linkml.io/linkml/intro/overview.html). 




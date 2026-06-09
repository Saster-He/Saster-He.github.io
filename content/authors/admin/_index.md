---
# Display name
title: Jie He 何婕

# Name pronunciation (optional)
name_pronunciation: ''

# Full name (for SEO)
first_name: Jie
last_name: He

# Status emoji
status:
  icon: ''

# Is this the primary user of the site?
superuser: true

# Role/position/tagline
role: Biostatistician building AI-powered clinical tools

# Organizations/Affiliations to display in Biography blox
organizations:
  - name: Boston University
    url: https://www.bu.edu/sph/departments/biostatistics/

# Social network links
profiles:
  - icon: at-symbol
    url: 'mailto:hejies@bu.edu'
    label: E-mail Me
  - icon: brands/github
    url: https://github.com/Saster-He
  - icon: brands/linkedin
    url: https://www.linkedin.com/in/jiesh/


education:
  - area: PhD Biostatistics
    institution: Boston University
    date_start: 2024-09-01
    date_end: 2028-05-01
    summary: |
      Current doctoral research: extending super learner methods for survival prediction in complex sampling designs. Co-advised by [Dr. Haolin (Leo) Li](https://sites.google.com/view/haolin-leo-li-phd/) and [Dr. Scarlett Bellamy](https://www.bu.edu/sph/profile/scarlett-bellamy/).

      eFHS wearable/mobile health project, advised by [Prof. Chunyu Liu](https://www.bu.edu/sph/profile/chunyu-liu/): analyzed >1 billion observations from older adults using R, SAS, and shell scripting to study associations between digital biomarkers and cognitive function.
    button:
      text: 'Google Scholar'
      url: 'https://scholar.google.com/citations?user=L5iMhdgAAAAJ&hl=en'
  - area: MS Biostatistics
    institution: University of North Carolina at Chapel Hill
    date_start: 2019-08-01
    date_end: 2020-12-01
    summary: |
      Coursework spanning statistical theory and applied methods:
      - **Biostatistics**: Survival Analysis, Longitudinal Data Analysis, Causal Inference, Clinical Study Design
      - **Mathematics**: Real Analysis, Stochastic Modeling, Optimization and Functional Analysis
      - **Computer Science**: Data Structures and Algorithms, Parallel Computing
  - area: BSPH Biostatistics, Second Major in Computer Science, Minor in Mathematics
    institution: University of North Carolina at Chapel Hill
    date_start: 2015-08-01
    date_end: 2019-08-01
    summary: |
      Graduated with Distinction. Honors Thesis: _Weighted inference of gene expression variability in single-cell RNA-seq data_, advised by [Prof. Di Wu](https://sph.unc.edu/adv_profile/di-wu-phd/). Developed R functions to address mean-variance relationships for zero-inflated counts across 32,738 genes and 2,692 cells.

work:
  - position: Research Assistant Extern, SP & Stats
    company_name: Vertex Pharmaceuticals
    company_url: 'https://www.vrtx.com/home/'
    company_logo: ''
    date_start: 2025-08-01
    date_end: ''
    summary: |2-
      Built a Shiny/button-driven automation workflow for Tables, Figures, and Listings (TFL) generation in clinical trials. Current work adds an initial-stage LLM-agent layer so statistical programmers can request auto TFL generation in natural language instead of clicking UI buttons.

      - Designed and built a human-in-the-loop Shiny control panel for analyst review, revision, and approval
      - Automated specification-driven SDTM mapping, ADaM construction logic, and routine TFL output generation
      - Initiated a natural-language LLM-agent layer for translating analyst requests into automated TFL generation workflows
      - Added validation checks against CDISC standards and expected specifications before outputs are surfaced for review

  - position: Biostatistician
    company_name: Boston Children's Hospital
    company_url: 'https://www.childrenshospital.org/'
    company_logo: ''
    date_start: 2021-06-01
    date_end: '2024-09-01'
    summary: |2-
      Statistical collaborator in the Biostatistics and Research Department, supervised by [Dr. Edie Weller](https://research.childrenshospital.org/researchers/edie-weller). Contributed to published research across pediatric hematology, cardiology, critical care, and COVID-19 outcomes.

      - **Simulation study**: Applied and evaluated ML classification models (on EHR-based simulated structures) to assess performance across varying data types and correlation patterns
      - **Survival analysis**: Built Cox models with frailty for clustered right-censored data; validated theoretical frameworks for time-dependent covariates
      - **ECPR outcomes**: Deployed random survival forests on ELSO Registry data to identify predictors of in-hospital mortality following extracorporeal CPR
      - **R package & Shiny app**: Developed a data management tool with custom functions and an interactive app to streamline REDCap data cleaning and automate QC of clinical notes

# Skills
skills:
  - name: Programming
    items:
      - name: R / RStudio
        description: 'Advanced · Survival analysis · Package development · Shiny'
        percent: 100
        icon: devicon/rstudio
      - name: SAS
        description: 'Advanced · Clinical data analysis · Regulatory reporting'
        percent: 95
        icon: chart-bar
      - name: Python
        description: 'Proficient · Data pipelines · ML workflows · LLM tooling'
        percent: 75
        icon: devicon/python
      - name: SQL
        description: 'Proficient · Data querying and management'
        percent: 70
        icon: circle-stack
      - name: Shell Scripting
        description: 'Proficient · Workflow automation · HPC environments'
        percent: 65
        icon: command-line
      - name: PyTorch
        description: 'Familiar · Neural networks · Deep learning'
        percent: 50
        icon: devicon/pytorch
  - name: Clinical Workflow
    items:
      - name: Survival & Longitudinal Methods
        description: 'KM · Cox · Competing risks · RSF · Mixed-effects models · GEE'
        percent: 90
        icon: chart-bar-square
      - name: Real World Evidence
        description: 'Registry outcomes/ EHRs (ELSO) · Large cohort wearables (eFHS)'
        percent: 85
        icon: chart-bar-square
      - name: Sensitivity & Reproducibility
        description: 'Outlier diagnostics · Subgroup analyses · Reproducible R scripts'
        percent: 85
        icon: adjustments-horizontal
      - name: SAP & Specification Interpretation
        description: 'Translating programming notes into automated outputs'
        percent: 80
        icon: shield-check
      - name: Clinical Trial Design
        description: 'Coursework in study design · Simulation-based model evaluation'
        percent: 55
        icon: beaker
      - name: CDISC Standards
        description: 'Working knowledge of SDTM/ADaM structures · Exposure through TFL tooling'
        percent: 55
        icon: clipboard-document-check

---

I'm a biostatistician who builds AI-powered tools for clinical research. Most of my work lives at the intersection of rigorous statistical methodology and modern software: the kind of problems where the math matters and so does the engineering.

My PhD research at Boston University extends super learner methods for survival prediction in complex sampling designs. I also worked on the Electronic Framingham Heart Study, analyzing over a billion smartwatch and wearable sensor observations to study how digital biomarkers connect to cognitive aging in older adults. At Vertex Pharmaceuticals, I built a Shiny/button-driven automation workflow for clinical TFL generation and am developing an initial-stage LLM-agent layer for natural-language TFL requests. Before the PhD, I spent three years at Boston Children's Hospital doing applied biostatistics across pediatric cardiology, hematology, and critical care, where I built R packages, deployed survival models on registry data, and co-authored peer-reviewed publications.

Outside of work, I ski, write, and am always looking for dogs to pet.

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
      Analyzing large-scale mobile health and wearable sensor data from older adult populations to understand associations between digital biomarkers and cognitive function. Core dataset: Electronic Framingham Heart Study (>1 billion observations). Advised by [Prof. Chunyu Liu](https://www.bu.edu/sph/profile/chunyu-liu/).
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
  - position: Research Assistant Extern
    company_name: Vertex Pharmaceuticals
    company_url: 'https://www.vrtx.com/home/'
    company_logo: ''
    date_start: 2025-08-01
    date_end: ''
    summary: |2-
      Building a multi-agent automation system for Tables, Figures, and Listings (TFL) generation in clinical trials. Statistical programmers interact with LLM agents through a Shiny interface; agents handle SDTM mapping, dataset construction, and output generation end-to-end.

      - Designed the multi-agent architecture: routing, tool use, and agent handoffs across the TFL pipeline
      - Built the Shiny front end that serves as the programmer-facing interface for agent interaction
      - Agents handle SDTM domain mapping, ADaM dataset derivation, and submission-ready output generation

  - position: Biostatistician
    company_name: Boston Children's Hospital
    company_url: 'https://www.childrenshospital.org/'
    company_logo: ''
    date_start: 2021-06-01
    date_end: '2024-09-01'
    summary: |2-
      Statistical collaborator in the Biostatistics and Research Department, supervised by Dr. Edie Weller. Contributed to published research across pediatric hematology, cardiology, critical care, and COVID-19 outcomes.

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

languages:
  - name: English
    percent: 100
  - name: Chinese (Mandarin)
    percent: 100
  - name: German
    percent: 25

---

I'm a biostatistician and PhD student at Boston University working at the intersection of wearable health data and AI-powered clinical tools.

My PhD research (with Prof. Chunyu Liu) uses smartwatch and mobile health data from the Electronic Framingham Heart Study to study associations between digital biomarkers and cognitive function in older adults. The dataset has over 1 billion observations, so a lot of the work is about building pipelines that can actually handle that scale.

At Vertex Pharmaceuticals, I'm building a multi-agent automation system for TFL (Tables, Figures, and Listings) generation in clinical trials. Statistical programmers use a Shiny interface to interact with LLM agents that handle SDTM mapping, dataset construction, and output generation. The goal is to automate the routine parts of clinical statistical programming so teams can focus on the work that requires real judgment.

Before the PhD, I spent three years at Boston Children's Hospital as a biostatistician: survival models, machine learning on EHR data, R package development, and Shiny apps for clinical data management.

Outside of work, I ski, write, and am always looking for dogs to pet.

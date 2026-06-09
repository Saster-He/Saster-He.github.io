---
title: 'TFL Automation at Vertex Pharmaceuticals'
summary: 'A Shiny/button-driven automation workflow for Tables, Figures, and Listings generation in clinical trials, with an initial-stage LLM-agent layer for natural-language TFL requests.'
tags:
  - Python
  - R
  - SAS
  - LLM
  - Automation
  - Clinical
date: '2025-08-01'
featured: true

external_link: ''

image:
  caption: ''
  focal_point: Smart
---

## Overview

Every drug approval requires submission-ready clinical study deliverables: standardized datasets (SDTM, ADaM) and a Clinical Study Report (CSR) containing Tables, Figures, and Listings (TFL) that document trial results. Producing these deliverables involves repetitive statistical programming work that has to be done correctly and consistently for every study.

This project built a Shiny/button-driven automation workflow for routine TFL generation. The newer LLM-agent component is in its initial stage: allowing users to describe auto TFL generation requests in natural language instead of clicking UI buttons.

## Architecture

The system is organized around a **human-in-the-loop automation pattern**:

1. **Automation layer**: The completed workflow uses an R Shiny interface as the front-end control panel. Statistical programmers provide analysis specifications, trigger TFL generation through UI controls, review generated outputs, and approve or revise before downstream use.

2. **LLM agent layer**: The initial-stage agent layer is designed to replace button-driven interactions with natural-language requests. Current work focuses on specification interpretation, SDTM mapping, ADaM construction logic, and auto TFL generation from analyst prompts.

3. **ADaM Spec reasoning engine**: Initiated in summer 2026, this component focuses on mapping analysis specifications to ADaM construction logic. It is still in its early phase.

4. **Validation layer**: Automated checks run against CDISC standards and expected specifications before output is surfaced to the programmer for review.

The completed Shiny automation keeps programmers in control while reducing manual overhead on routine TFL outputs. The LLM-agent layer extends that workflow toward natural-language interaction, but remains early-stage.

## Technical Stack

- **R Shiny**: Front-end interface, button-driven automation, and human-in-the-loop control panel
- **Python**: Initial-stage LLM agent orchestration and pipeline automation
- **R and SAS**: Statistical programming and output generation
- **Shell scripting**: Workflow automation and environment management

## Why It Matters

TFL generation is a prerequisite for every regulatory submission, and it is time-consuming to do manually. Automating routine outputs lets statistical programmers spend more effort on the judgment calls that require expertise: methodology, specification review, validation, and interpretation of results. The natural-language agent layer aims to make that automation easier to use by letting analysts state what they need directly.

_This project is ongoing (Aug 2025 to Present). Details are limited due to confidentiality._

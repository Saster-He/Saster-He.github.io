---
title: 'TFL Automation with Multi-Agent LLMs at Vertex Pharmaceuticals'
summary: 'A multi-agent system for Tables, Figures, and Listings (TFL) generation in clinical trials. LLM agents handle SDTM mapping, dataset construction, and output generation; statistical programmers interact through a Shiny interface.'
tags:
  - Python
  - R
  - SAS
  - Automation
  - Clinical
  - LLM
date: '2025-08-01'
featured: true

external_link: ''

image:
  caption: ''
  focal_point: Smart
---

## Overview

Clinical statistical programming for regulatory submissions is labor-intensive: deriving SDTM-compliant datasets, building ADaM analysis datasets, and producing Tables, Figures, and Listings (TFLs) for every study endpoint. This project automates that pipeline using a multi-agent LLM system, with statistical programmers as the humans in the loop.

## Architecture

The system is built around a team of specialized LLM agents, orchestrated behind a Shiny front end:

- **Shiny interface** -- the programmer-facing layer where users submit analysis requests, review agent outputs, and provide corrections or approvals
- **Routing agent** -- interprets the programmer's request and delegates to the appropriate downstream agent
- **SDTM mapping agent** -- maps raw clinical data to SDTM domains, handling domain-specific conventions and CDISC compliance
- **Dataset construction agent** -- derives ADaM datasets from mapped SDTM inputs, applying analysis-specific transformations
- **Output generation agent** -- produces submission-ready tables, listings, and figures from the constructed datasets

Agents pass structured outputs between each other; the programmer can intervene or redirect at any stage through the Shiny interface.

## Technical Stack

- **R / Shiny** -- programmer-facing front end and output rendering
- **Python** -- agent orchestration, LLM tooling, pipeline framework
- **R and SAS** -- statistical output generation and validation
- **Shell scripting** -- environment management and workflow automation

## Why It Matters

Every drug approval requires submission-ready SDTM and TFL deliverables. When the routine programming work is handled by agents, statistical teams can focus on methodology, specification review, and the judgment calls that require real expertise. The Shiny interface keeps programmers in control without requiring them to manage the underlying automation layer directly.

_This project is ongoing (Aug 2025--Present). Details limited due to confidentiality._

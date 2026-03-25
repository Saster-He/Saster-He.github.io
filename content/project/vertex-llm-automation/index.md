---
title: 'TFL Automation at Vertex Pharmaceuticals'
summary: 'A multi-agent system for automating Tables, Figures, and Listings generation in clinical trials, with statistical programmers driving LLM agents through a Shiny interface.'
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

Every drug approval requires submission-ready clinical study deliverables: standardized datasets (SDTM, ADaM) and a Clinical Study Report (CSR) containing Tables, Figures, and Listings (TFL) that document trial results. Producing these deliverables is largely manual statistical programming work that has to be done correctly and consistently for every study.

This project builds a multi-agent automation system to handle that work.

## Architecture

The system is organized around a **human-in-the-loop agent pattern**:

1. **Shiny front-end**: Statistical programmers interact with the system through an R Shiny interface. They provide analysis specifications, review agent-generated outputs, and approve or revise before submission.

2. **LLM agent layer**: Agents interpret the provided specifications and generate statistical programming code for each requested output. The agents handle SDTM domain mapping, ADaM dataset construction logic, and TFL output generation.

3. **Validation layer**: Automated checks run against CDISC standards and expected specifications before output is surfaced to the programmer for review.

The Shiny interface keeps programmers in control while eliminating the repetitive parts of routine TFL work. Analysts drive the agents rather than writing boilerplate code by hand.

## Technical Stack

- **R Shiny**: Front-end interface and human-in-the-loop control panel
- **Python**: LLM agent orchestration and pipeline automation
- **R and SAS**: Statistical programming and output generation
- **Shell scripting**: Workflow automation and environment management

## Why It Matters

TFL generation is a prerequisite for every regulatory submission, and it is time-consuming to do manually. Automating routine outputs means statistical programmers can spend their effort on the judgment calls that require expertise: methodology, specification review, and interpretation of results.

_This project is ongoing (Aug 2025 to Present). Details are limited due to confidentiality._

---
title: 'Home'
date: 2023-10-24
type: landing

design:
  spacing: "5rem"

sections:
  - block: biography
    content:
      username: admin
      button:
        text: Download CV
        url: uploads/resume.pdf
    design:
      banner:
        filename: kalen-emsley-Bkci_8qcdvQ-unsplash.jpg
      biography:
        style: 'font-size: 0.92em; line-height: 1.7;'

  - block: markdown
    content:
      title: What I'm Working On
      subtitle: ''
      text: |-
        <div class="now-grid">

        **PhD Research at Boston University Biostatistics**
        Analyzing large-scale smartwatch and mobile health data from the Electronic Framingham Heart Study (>1 billion observations) to understand associations between wearable-derived measures and cognitive function in older adults.
        _Advisor: Prof. Chunyu Liu_

        ---

        **Research Extern at Vertex Pharmaceuticals** _(Aug 2025 to Present)_
        Building a multi-agent system that automates the Tables, Figures, and Listings (TFL) pipeline for clinical trial submissions. Statistical programmers drive LLM agents through a Shiny interface to handle SDTM mapping, dataset construction, and output generation.

        </div>
    design:
      background:
        gradient_start: '#f8faff'
        gradient_end: '#f1f5f9'
        gradient_angle: 160

  - block: collection
    content:
      title: Selected Projects
      subtitle: ''
      text: ''
      count: 6
      filters:
        folders:
          - project
        featured_only: false
      sort_by: 'Date'
      sort_ascending: false
    design:
      view: card
      columns: '2'

  - block: experience
    content:
      username: admin
    design:
      date_format: 'Jan 2006'
      is_education_first: false

  - block: skills
    content:
      title: Skills
      username: admin

  - block: markdown
    content:
      title: Languages
      text: |-
        English (native) · Chinese/Mandarin (native) · German (basic)
---

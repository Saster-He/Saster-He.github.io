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

        **PhD Research, Boston University Biostatistics**
        Extending super learner methods for survival prediction in complex sampling designs, with applications to longitudinal clinical data. Co-advised by [Dr. Haolin (Leo) Li](https://sites.google.com/view/haolin-leo-li-phd/) and [Dr. Scarlett Bellamy](https://www.bu.edu/sph/profile/scarlett-bellamy/).

        ---

        **Research Extern at Vertex Pharmaceuticals** _(Aug 2025 to Present)_
        Built a Shiny/button-driven automation workflow for clinical Tables, Figures, and Listings (TFL) generation. Current work adds an initial-stage LLM-agent layer so statistical programmers can request auto TFL generation in natural language instead of clicking UI buttons.

        </div>

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
        English (professional) · Chinese/Mandarin (native) · German (basic)
---

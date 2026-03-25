---
title: 'Gene Expression Variability in Single-Cell RNA-seq'
summary: 'Honors thesis: a weighted hypothesis testing framework for differential variability in scRNA-seq data, with R tools to address the mean-variance relationship in zero-inflated count data.'
tags:
  - R
  - Bioinformatics
  - Statistics
  - Single-Cell
date: '2019-05-01'
featured: false

external_link: ''

image:
  caption: ''
  focal_point: Smart
---

## Motivation

Most differential expression analysis in single-cell RNA-seq focuses on differences in *mean* expression between cell populations. But gene expression variability — the variance of expression across cells — carries its own biological signal. Genes that are more variable in one condition vs. another can indicate heterogeneous cell states, developmental plasticity, or disease-associated dysregulation.

The challenge: zero-inflated count data in scRNA-seq creates a strong mean-variance dependency that biases naive variability tests. A gene with higher mean expression will appear more variable simply due to distributional properties, not biology.

## Methods

Developed a weighted hypothesis testing framework that:

- **Accounts for mean-variance dependency** in zero-inflated negative binomial count data
- **Tests for differential variability** between cell populations using a weighted statistic that stabilizes variance estimates across the expression range
- **Scales to large datasets** — validated on 32,738 genes across 2,692 single cells

## Implementation

All methods implemented as R functions, using the `MAST` and `edgeR` frameworks as a foundation. The weighting scheme was derived analytically and validated via simulation.

## Recognition

Awarded **Honors Thesis with Highest Distinction** by the University of North Carolina at Chapel Hill, 2019.

_Advisor: [Prof. Di Wu](https://sph.unc.edu/adv_profile/di-wu-phd/), Department of Biostatistics, UNC Gillings School of Global Public Health._

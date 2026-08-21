---
permalink: /resources-running-analyses/
title: "Running analyses"
layout: single
toc: true
toc_sticky: true
---

## About running analyses

This page gives new team members (bachelor and master students) an overview of the main analysis types we run and what each one is used for. Detailed step-by-step guides are linked per section below.

{: .notice--info}
**A note on the guides.** The linked guides are hosted on SharePoint and only open with an Amsterdam UMC account. You will get this account on your first day, so a link that doesn't open yet is expected before then.

{: .notice--info}
**A note on running analyses on the server.** All analysis types below can be run either through an interactive session or as a SLURM batch job on Luna. See the [Server](./resources-server.md) page for login instructions, SLURM basics, and example scripts. This page focuses on what each analysis does and when to use it.

Each section below follows the same structure so it stays easy to scan.

- **What it is** - short description
- **When to use it** - typical project type
- **Inputs and outputs**
- **Guide** - link to the full protocol
- **Documentation** - placeholder for screenshots or example figures

## Quick overview

| Analysis type | Category | Main software | Typical output |
|---|---|---|---|
| **fMRIPrep** | Preprocessing | fMRIPrep | Preprocessed functional and anatomical images |
| **FreeSurfer** | Preprocessing | FreeSurfer | Cortical and subcortical segmentations, volume and thickness tables |
| **HALFpipe** | Functional statistics | HALFpipe | First and group-level activation and connectivity maps |
| **VBM** | Structural statistics | FSL / SPM | Voxel-wise grey matter statistical maps |
| **RBA** | Region-based statistics | R (brms) | Region-level effect estimates and posterior distributions |

---

## Preprocessing

### fMRIPrep

**What it is**
fMRIPrep is a standardized pipeline for preprocessing functional (and structural) MRI data. It handles motion correction, susceptibility distortion correction, spatial normalization, and confound generation, so that everyone in the team preprocesses their functional data the same way.

**When to use it**
Any project using task-based or resting-state fMRI data. This is normally the first processing step after data is organized in BIDS format.

| Input | Output |
|---|---|
| Raw MRI data in BIDS format | Preprocessed BOLD and anatomical images, confound files, HTML QC report per subject |

**Guide**
[fMRIPrep page](https://fmriprep.org/en/stable/)



---

### FreeSurfer

**What it is**
FreeSurfer reconstructs cortical surfaces and produces subcortical and cortical segmentations from anatomical (T1) scans. It is the basis for cortical thickness, surface area, and subcortical volume measures used in several of our structural projects.

**When to use it**
Any project needing cortical thickness, surface area, or subcortical volume measures, including as input for region-based analysis (RBA, see below).

| Input | Output |
|---|---|
| T1-weighted anatomical scan (often run alongside fMRIPrep) | Segmented cortical/subcortical surfaces, region-level volume and thickness tables |

**Guide**
[FreeSurfer page ](https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferBeginnersGuide)


---

## Statistical analyses

### Functional MRI statistics (HALFpipe)

**What it is**
HALFpipe is a tool for first and group-level statistical analysis of task and resting-state fMRI data, built on top of fMRIPrep outputs. It handles model specification, feature extraction (e.g. seed-based connectivity, ALFF), and group statistics through a guided interface.

**When to use it**
Once fMRIPrep preprocessing is complete and you want to test for task-related activation or functional connectivity differences.

| Input | Output |
|---|---|
| fMRIPrep-preprocessed functional data | Subject-level and group-level statistical maps |

**Guide**
[HALFpipe page ](https://enigma.ini.usc.edu/protocols/functional-protocols/)



---

### Structural statistics (VBM)

**What it is**
Voxel-based morphometry (VBM) tests for group differences in grey matter volume or density on a voxel-by-voxel basis across the whole brain, rather than in predefined regions.

**When to use it**
Whole-brain, exploratory structural comparisons between groups (for example patients vs controls), when you don't want to restrict the analysis to specific regions in advance.

| Input | Output |
|---|---|
| T1-weighted anatomical scans | Voxel-wise statistical maps (e.g. t-maps, corrected for multiple comparisons) |

**Guide**
[VBM info](https://sites.google.com/view/enigmavbm)


---

### Region-based analysis (RBA)

**What it is**
RBA tests for group differences within predefined anatomical regions (for example FreeSurfer-derived subcortical structures), using region-level summary measures rather than voxel-wise data. In our team this is typically run as a Bayesian analysis in R (using brms).

**When to use it**
When you have a clear anatomical hypothesis about specific regions, or want to complement a whole-brain approach like VBM with a more targeted, hypothesis-driven test.

| Input | Output |
|---|---|
| Region-level volume, thickness, or other summary tables (often from FreeSurfer) | Region-level effect estimates and posterior distributions, model summaries |



---



[Back to Resources](./resources.md)

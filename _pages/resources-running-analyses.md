---
permalink: /resources-running-analyses/
title: "Running analyses"
layout: single
toc: true
toc_sticky: true
---

## About running analyses

This page gives new team members (bachelor and master students) an overview of the main analysis types we run and what each one is used for. Detailed step-by-step guides are linked per section below.

**A note on the guides:** the linked guides are hosted on SharePoint and only open with an Amsterdam UMC account. You will get this account on your first day, so a link that doesn't open yet is expected before then.

**A note on running analyses on the server:** all analysis types below can be run either through an interactive session or as a SLURM batch job on Luna. See the [Server](/resources-server/) page for login instructions, SLURM basics, and example scripts. This page focuses on what each analysis does and when to use it.

Each section below follows the same structure so it stays easy to scan.

- **What it is** - short description
- **When to use it** - typical project type
- **Inputs and outputs**
- **Guide** - link to the full protocol
- **Documentation** - placeholder for screenshots or example figures

## Quick overview

| Analysis type | Category | Main software | Typical output |
|---|---|---|---|
| fMRIPrep | Preprocessing | fMRIPrep | Preprocessed functional and anatomical images |
| FreeSurfer | Preprocessing | FreeSurfer | Cortical and subcortical segmentations, volume and thickness tables |
| HALFpipe | Functional statistics | HALFpipe | First and group-level activation and connectivity maps |
| VBM | Structural statistics | FSL / SPM | Voxel-wise grey matter statistical maps |
| RBA | Region-based statistics | R (brms) | Region-level effect estimates and posterior distributions |

---

## Preprocessing

### fMRIPrep

**What it is**
fMRIPrep is a standardized pipeline for preprocessing functional (and structural) MRI data. It handles motion correction, susceptibility distortion correction, spatial normalization, and confound generation, so that everyone in the team preprocesses their functional data the same way.

**When to use it**
Any project using task-based or resting-state fMRI data. This is normally the first processing step after data is organized in BIDS format.

**Inputs and outputs**
- Input: raw MRI data in BIDS format
- Output: preprocessed BOLD and anatomical images, confound files, and an HTML quality control (QC) report per subject

**Guide**
[fMRIPrep protocol (SharePoint, Amsterdam UMC account required)](SHAREPOINT_LINK_PLACEHOLDER)

**Documentation placeholder**
_Add an example QC report screenshot and a short note on what "good" vs "flagged" output looks like here._

<!-- IMAGE PLACEHOLDER: fMRIPrep QC report example -->

---

### FreeSurfer

**What it is**
FreeSurfer reconstructs cortical surfaces and produces subcortical and cortical segmentations from anatomical (T1) scans. It is the basis for cortical thickness, surface area, and subcortical volume measures used in several of our structural projects.

**When to use it**
Any project needing cortical thickness, surface area, or subcortical volume measures, including as input for region-based analysis (RBA, see below).

**Inputs and outputs**
- Input: T1-weighted anatomical scan (often run as part of, or alongside, fMRIPrep)
- Output: segmented cortical/subcortical surfaces, region-level volume and thickness tables

**Guide**
[FreeSurfer protocol (SharePoint, Amsterdam UMC account required)](SHAREPOINT_LINK_PLACEHOLDER)

**Documentation placeholder**
_Add a screenshot of a FreeSurfer segmentation (e.g. in freeview) and an example output table here._

<!-- IMAGE PLACEHOLDER: FreeSurfer segmentation example -->

---

## Statistical analyses

### Functional MRI statistics (HALFpipe)

**What it is**
HALFpipe is a tool for first and group-level statistical analysis of task and resting-state fMRI data, built on top of fMRIPrep outputs. It handles model specification, feature extraction (e.g. seed-based connectivity, ALFF), and group statistics through a guided interface.

**When to use it**
Once fMRIPrep preprocessing is complete and you want to test for task-related activation or functional connectivity differences.

**Inputs and outputs**
- Input: fMRIPrep-preprocessed functional data
- Output: subject-level and group-level statistical maps

**Guide**
[HALFpipe protocol (SharePoint, Amsterdam UMC account required)](SHAREPOINT_LINK_PLACEHOLDER)

**Documentation placeholder**
_Add screenshots of the HALFpipe setup steps and an example group result map here._

<!-- IMAGE PLACEHOLDER: HALFpipe setup and output example -->

---

### Structural statistics (VBM)

**What it is**
Voxel-based morphometry (VBM) tests for group differences in grey matter volume or density on a voxel-by-voxel basis across the whole brain, rather than in predefined regions.

**When to use it**
Whole-brain, exploratory structural comparisons between groups (for example patients vs controls), when you don't want to restrict the analysis to specific regions in advance.

**Inputs and outputs**
- Input: T1-weighted anatomical scans
- Output: voxel-wise statistical maps (e.g. t-maps, corrected for multiple comparisons)

**Guide**
[VBM protocol (SharePoint, Amsterdam UMC account required)](SHAREPOINT_LINK_PLACEHOLDER)

**Documentation placeholder**
_Add an example VBM statistical map and a short note on the correction method used here._

<!-- IMAGE PLACEHOLDER: VBM group result example -->

---

### Region-based analysis (RBA)

**What it is**
RBA tests for group differences within predefined anatomical regions (for example FreeSurfer-derived subcortical structures), using region-level summary measures rather than voxel-wise data. In our team this is typically run as a Bayesian analysis in R (using brms).

**When to use it**
When you have a clear anatomical hypothesis about specific regions, or want to complement a whole-brain approach like VBM with a more targeted, hypothesis-driven test.

**Inputs and outputs**
- Input: region-level volume, thickness, or other summary tables (often from FreeSurfer)
- Output: region-level effect estimates and posterior distributions, model summaries

**Guide**
[RBA methodology and protocol (SharePoint, Amsterdam UMC account required)](SHAREPOINT_LINK_PLACEHOLDER)

**Documentation placeholder**
_Add an example posterior plot and a short explanation of how to interpret it here._

<!-- IMAGE PLACEHOLDER: RBA posterior distribution example -->

---

## Adding to this page

If you set up or run a new type of analysis, please add it here in the same format (what it is, when to use it, inputs and outputs, guide link, documentation). Replace the placeholder comments above with actual screenshots or short example files, and swap in the real SharePoint links once available, so the page stays useful for the next student.

[Back to Resources](/resources/)

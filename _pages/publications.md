---
layout: single
title: Publications
permalink: /publications/
toc: true
toc_sticky: true
---

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">

<style>
  /* Scoped to .labpubs- so this never leaks into the rest of the site's theme */
  .labpubs-wrap {
    --labpubs-paper: #fbfaf6;
    --labpubs-ink: #1a1a18;
    --labpubs-ink-soft: #58564d;
    --labpubs-rule: #e1ded0;
    --labpubs-accent: #2f4a3d;
    --labpubs-accent-tint: #eaf0ec;

    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: var(--labpubs-ink);
    max-width: 46rem;
    margin: 0 auto;
    padding: 2rem 1.25rem 5rem;
  }

  .labpubs-header {
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--labpubs-rule);
  }

  .labpubs-eyebrow {
    font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--labpubs-accent);
    margin: 0 0 0.6rem;
  }

  .labpubs-header h1 {
    font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
    font-size: 2.1rem;
    font-weight: 600;
    line-height: 1.15;
    margin: 0 0 0.5rem;
    color: var(--labpubs-ink);
  }

  .labpubs-header p {
    font-size: 0.95rem;
    color: var(--labpubs-ink-soft);
    margin: 0;
    line-height: 1.5;
  }

  .labpubs-year-group {
    margin-bottom: 2.75rem;
  }

  .labpubs-year-label {
    font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, monospace;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--labpubs-accent);
    background: var(--labpubs-accent-tint);
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 3px;
    margin-bottom: 1.1rem;
  }

  .labpubs-entry {
    position: relative;
    padding: 1.1rem 0 1.1rem 1.15rem;
    border-left: 2px solid var(--labpubs-rule);
    margin-bottom: 0.15rem;
    transition: border-color 0.15s ease;
  }

  .labpubs-entry:hover {
    border-left-color: var(--labpubs-accent);
  }

  .labpubs-entry-title {
    font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
    font-size: 1.22rem;
    font-weight: 600;
    line-height: 1.35;
    margin: 0 0 0.45rem;
  }

  .labpubs-entry-title a {
    color: var(--labpubs-ink);
    text-decoration: none;
    background-image: linear-gradient(var(--labpubs-accent), var(--labpubs-accent));
    background-position: 0 100%;
    background-repeat: no-repeat;
    background-size: 0% 1px;
    transition: background-size 0.2s ease;
  }

  .labpubs-entry-title a:hover {
    background-size: 100% 1px;
  }

  .labpubs-authors {
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--labpubs-ink-soft);
    max-width: 40rem;
    margin: 0 0 0.3rem;
  }

  .labpubs-citation {
    font-size: 0.88rem;
    line-height: 1.6;
    color: var(--labpubs-ink-soft);
    max-width: 40rem;
    font-style: italic;
  }

  .labpubs-citation a {
    color: var(--labpubs-accent);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    font-style: normal;
  }

  .labpubs-citation a:hover {
    border-bottom-color: var(--labpubs-accent);
  }

  .labpubs-empty {
    font-size: 0.95rem;
    color: var(--labpubs-ink-soft);
    padding: 2rem 0;
  }

  @media (max-width: 600px) {
    .labpubs-header h1 { font-size: 1.7rem; }
    .labpubs-entry-title { font-size: 1.08rem; }
  }
</style>

<div class="labpubs-wrap">
  <div class="labpubs-header">
    <p class="labpubs-eyebrow">Lab Publications</p>
    <h1>Recent Publications</h1>
    <p>Automatically synced from ORCID &middot; showing the last 5 years.</p>
  </div>

  {% assign pubs_by_year = site.data.publications | group_by: "year" %}
  {% assign pubs_by_year = pubs_by_year | sort: "name" | reverse %}

  {% if site.data.publications and site.data.publications.size > 0 %}
    {% for year_group in pubs_by_year %}
      <div class="labpubs-year-group">
        <span class="labpubs-year-label">{{ year_group.name }}</span>
        {% for pub in year_group.items %}
          <div class="labpubs-entry">
            <h2 class="labpubs-entry-title">
              {% if pub.url %}
                <a href="{{ pub.url }}" target="_blank" rel="noopener">{{ pub.title }}</a>
              {% else %}
                {{ pub.title }}
              {% endif %}
            </h2>

            {% if pub.authors %}
              <p class="labpubs-authors">
                {% for author in pub.authors %}
                  {{ author.name }}{% unless forloop.last %}{% if forloop.rindex == 2 %} and {% else %}, {% endif %}{% endunless %}
                {% endfor %}
              </p>
            {% endif %}

            <p class="labpubs-citation">
              {% if pub.journal %}{{ pub.journal }}{% endif %}{% if pub.volume %}, vol. {{ pub.volume }}{% endif %}{% if pub.issue %}, no. {{ pub.issue }}{% endif %}{% if pub.pages %}, pp. {{ pub.pages }}{% endif %}{% if pub.citation_html %} &middot; {{ pub.citation_html }}{% endif %}
            </p>
          </div>
        {% endfor %}
      </div>
    {% endfor %}
  {% else %}
    <p class="labpubs-empty">Publications will appear here once the automated ORCID sync has run.</p>
  {% endif %}
</div>
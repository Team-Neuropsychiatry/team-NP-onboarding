---
layout: page
title: Publications
permalink: /publications/
---

{% assign pubs_by_year = site.data.publications | group_by: "year" %}
{% assign pubs_by_year = pubs_by_year | sort: "name" | reverse %}

{% for year_group in pubs_by_year %}
  <h2>{{ year_group.name }}</h2>
  <ul class="publication-list">
    {% for pub in year_group.items %}
      <li class="publication-item">
        {% if pub.url %}
          <a href="{{ pub.url }}" target="_blank" rel="noopener">{{ pub.title }}</a>
        {% else %}
          <strong>{{ pub.title }}</strong>
        {% endif %}
        {% if pub.venue %}
          <br><em>{{ pub.venue }}</em>
        {% endif %}
        {% if pub.lab_authors %}
          <br><span class="pub-lab-authors">Lab authors: {{ pub.lab_authors | join: ", " }}</span>
        {% endif %}
      </li>
    {% endfor %}
  </ul>
{% endfor %}

{% if site.data.publications == empty or site.data.publications == nil %}
  <p>Publications will appear here once the automated ORCID sync has run.</p>
{% endif %}

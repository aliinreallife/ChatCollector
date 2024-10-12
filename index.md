---
layout: default
title: List of Conversations
---

## List of Conversations

<ul>
  {% for page in site.pages %}
    {% if page.path contains 'collection/' %}
      <li>
        <a href="{{ page.url | relative_url }}">{{ page.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>

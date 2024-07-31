{% set film_title = "Dunkirk" %}

SELECT
    *
from
    {{ ref('films') }}
WHERE
    title = '{{ film_title }}'
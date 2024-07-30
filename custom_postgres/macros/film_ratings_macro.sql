{% MACRO GENERATE_FILE_RATINGS() %}

WITH FILMS_WITH_RATINGS AS (
    SELECT
        FILM_ID,
        TITLE,
        RELEASE_DATE,
        PRICE,
        RATING,
        USER_RATING,
        CASE
            WHEN USER_RATING >= 4.5 THEN
                'Excellent'
            WHEN USER_RATING >=4.0 THEN
                'Good'
            WHEN USER_RATING >= 3.0 THEN
                'Average'
            ELSE
                'Poor'
        END AS RATING_CATEGORY
    FROM
        {{ REF('films') }}
), FILMS_WITH_ACTORS AS (
    SELECT
        F.FILM_ID,
        F.TITLE,
        STRING_AGG(A.ACTOR_NAME,
        ',') AS ACTORS
    FROM
        {{ REF('films') }} F
        LEFT JOIN {{ REF('film_actors') }} FA
        ON F.FILM_ID = FA.FILM_ID
        LEFT JOIN {{ REF('actors') }} A
        ON FA.ACTOR_ID = A.ACTOR_ID
    GROUP BY
        F.FILM_ID,
        F.TITLE
)
SELECT
    FWR.*,
    FWA.ACTORS
FROM
    FILMS_WITH_RATINGS FWR
    LEFT JOIN FILMS_WITH_ACTORS FWA
    ON FWR.FILM_ID = FWA.FILM_ID {% ENDMACRO %}
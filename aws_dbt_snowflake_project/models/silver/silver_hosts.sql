{{ config(materialized='incremental', unique_key='HOST_ID') }}

WITH src_bronze_hosts AS (
    SELECT * FROM {{ ref("bronze_hosts") }}
)

SELECT 
    HOST_ID,
    REPLACE(HOST_NAME, ' ', '_') AS HOST_NAME,
    HOST_SINCE,
    IS_SUPERHOST,
    RESPONSE_RATE,
    CASE
        WHEN RESPONSE_RATE > 95 THEN 'VERY GOOD'
        WHEN RESPONSE_RATE > 80 THEN 'GOOD'
        WHEN RESPONSE_RATE > 70 THEN 'FAIR'
        ELSE 'POOR'                     
    END AS RESPONSE_RATE_QUALITY,   
    CREATED_AT
FROM src_bronze_hosts

{% if is_incremental() %}
    -- Pro-tip: Include this filter so your incremental model actually filters new data!
    WHERE CREATED_AT > (SELECT MAX(CREATED_AT) FROM {{ this }})
{% endif %}

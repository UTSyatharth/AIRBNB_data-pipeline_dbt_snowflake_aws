{{ config (
        materialized='incremental' ,
        unique_key='LISTING_ID' 
    )
        }}

select 
    LISTING_ID,   
    Host_ID,      
    Property_Type,
    Room_Type,
    City,
    Country,
    Accommodates,
    Bathrooms,
    Bedrooms,
    Price_Per_Night,
    {{ tag('CAST(Price_Per_Night as INT)') }} as Price_per_night_Tag,
    CREATED_AT
    FROM {{ ref("bronze_listings")}}
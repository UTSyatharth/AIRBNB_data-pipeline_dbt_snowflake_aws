{{  config(
        materialized='incremental' ,
        unique_key='BOOKING_ID' 
    )
        }}

select 
    BOOKING_ID,
    LiSTING_ID,
    BOOKING_DATE,
    {{ multiply('NIGHTS_BOOKED','BOOKING_AMOUNT',2) }}  as TOTAL_AMOUNT, 
    SERVICE_FEE,
    CLEANING_FEE,
    BOOKING_STATUS,
    CREATED_AT
    FROM {{ ref("bronze_bookings")}}
    
{{ config(
    severity='warn'
) }}

select
    *
from {{ source('staging', 'bookings') }}
where BOOKING_AMOUNT < 200

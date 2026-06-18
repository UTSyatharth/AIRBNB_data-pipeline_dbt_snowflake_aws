{% macro tag(col)%}

    case 
        when {{ col }} < 100 then 'Low'
        when {{ col }} < 200 then 'Medium'
        else 'High'
    end

{% endmacro %}
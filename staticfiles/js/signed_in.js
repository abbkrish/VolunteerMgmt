setTimeout(function() {
     $.get("{% url 'home:home_view' %}") // Do something after 5 seconds
}, 5000);
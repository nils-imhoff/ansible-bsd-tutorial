<!DOCTYPE html>
<html>
<head>
    <title>Ansible Tutorial - Role Example</title>
    <meta charset="utf-8">
</head>

<body>
    <h1>Ansible Tutorial - Role Example</h1>
    <p>
        Workshop: <a href="https://events.eurobsdcon.org/{{ tutorial_year }}/talk/{{ tutorial_id }}">{{ tutorial_name }}</a>
    </p>

    <p>
        App-Name: {{ application_name }}
    </p>

    <p>
        {{ template_fullpath }} -> {{ template_destpath }}, {{ template_run_date }}
    </p>
</body>

</html>

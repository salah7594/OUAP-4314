flask_bdgest
============

Running run.py launches the web application. Inside the app folder, the views.py script controls
the routes, how the data is processed and which templates are rendered. The forms.py script

.
├── Dockerfile
├── README.rst
├── app
│   ├── __init__.py
│   ├── forms.py
│   ├── static
│   │   ├── LICENSE
│   │   ├── README.md
│   │   ├── css
│   │   │   ├── materialize.css
│   │   │   └── materialize.min.css
│   │   ├── fonts
│   │   │   └── roboto
│   │   └── js
│   │       ├── materialize.js
│   │       └── materialize.min.js
│   ├── templates
│   │   ├── author.html
│   │   ├── author_id.html
│   │   ├── base.html
│   │   ├── comic.html
│   │   ├── dictionaries.html
│   │   ├── index.html
│   │   ├── macros.html
│   │   ├── series.html
│   │   └── series_id.html
│   └── views.py
├── config.py
├── requirements.txt
├── run.py
└── tree.txt

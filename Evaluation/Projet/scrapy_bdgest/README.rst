=============
scrapy_bdgest
=============

Website: `bdgest <https://www.bdgest.com>`_

What is scraped?
----------------
Authors, series and comics.

But what exactly?
-----------------
Authors:

* author id (mandatory)
* url
* first name
* last name
* nickname
* country
* personal web page
* birth date
* death date
* image

Series:

* series id (mandatory)
* author id
* url
* name
* genre
* status
* number of volumes
* list of volume ids
* origin (country or continent)
* language

Comics:

* comic id (mandatory)
* series id
* author id
* title
* volume number
* scenario
* illustration
* coloring
* legal deposit
* editor
* collection
* format
* ISBN (International Standard Book Number)
* number of pages
* image

Storage
.......
MongoDB

Check the `pipelines.py <https://github.com/nicolasvo95/scrapy_bdgest/blob/master/bdgest/pipelines.py>`_ file for more details.

Commands
........
From the root of the project, execute the following command:

.. code-block:: bash

    > scrapy crawl authors

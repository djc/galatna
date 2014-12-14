Galatna
=======

Galatna creates an SVG-based visualization from your Google Location History.
It requires Python 2.7 and a Location History output file
(``LocationHistory.json``) as downloaded from `Google Takeout`_. An example
can be found in the project directory, as ``example.png``. I described the
motivation for and process of writing this code in a `blog post`_.

.. image:: https://raw.github.com/djc/galatna/master/example.png

To create a map, run ``process.py`` with the JSON file as an argument. It will
output some progress messages to ``stderr`` and the SVG to ``stdout``. On a
2009-era MacBook Pro, the script takes about 10s to process my 20000 data
points (about 2.5 years worth of Location History data). Use stdout
redirection to send the SVG to a file, then view in your browser of choice;
both Firefox and Chrome do okay, although it will take some time to fully
render the map if you have extensive location history.

Older versions of Takeout's Location History export feature were a bit broken,
in that they exported multiple JSON object keys of the same name with different
data. If you have a similarly broken file, ``combine.py`` can clean it up.

.. _Google Takeout: https://www.google.com/takeout/
.. _blog post: https://dirkjan.ochtman.nl/writing/2012/11/28/tracing-a-path.html

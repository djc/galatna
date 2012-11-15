Galatna
=======

Galatna creates an SVG map from your Latitude history. It requires Python 2.7
and a Latitude output file as downloaded from `Google Takeout`_.

The current version of Takeout's Latitude export feature is a bit broken, in
that it exports multiple JSON object keys of the same name with different
data. If you have a similarly broken file, ``combine.py`` can clean it up.

To create a map, run process.py with the (fixed) JSON file as an argument. It
will output some progress messages to stderr and the SVG contents to stdout.
Use stdout redirection to send the SVG to a file, the view in your browser of
choice; both Firefox and Chrome do okay, although it will take some time to
fully render the map if you have extensive location history.

.. _Google Takeout: https://www.google.com/takeout/


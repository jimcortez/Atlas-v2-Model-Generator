# Atlas-v2-xmodel
Code to create an xmodel file, and a corresponding csv file, for the Atlas v2 LED Sphere by DrZzs &amp; GrZzs

To use this script for your Atlas v2, you'll need to set the value for each ring in the "rings" dictionary to match the count of LEDs in your actual rings

You can also adjust the number of ports from 16, if you use a controller with a different port count.

Running the script will then generate an .xmodel file, and a csv file.

The xmodel file can be loaded into xlights.

In the CSV file you'll find corresponding values for the rings

DC Start is indicating the start of a data channel, and the controller port.  (Connect the beginning signal port of this ring back to the controller port listed)

PC Start is indicating the start of a power channel, and the controller port. (connect the beginning of this ring +/- back to the controller port listed)

PC End is indicating the end of a power channel, and the controller port. (connect the end of this ring +/- back to the controller port)

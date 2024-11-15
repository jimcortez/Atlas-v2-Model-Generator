# Atlas-v2-xmodel
Code to create an xmodel file, and a corresponding csv file, for the Atlas v2 LED Sphere by DrZzs &amp; GrZzs

Learn about the project here: https://www.youtube.com/watch?v=l0WGbmc9_4Q

To use this script for your Atlas v2, you'll need to set the value for each ring in the "rings" dictionary to match the count of LEDs in your actual rings

You can also adjust the number of ports from 16, if you use a controller with a different port count.

Running the script will then generate an .xmodel file, and a csv file.

The xmodel file can be loaded into xlights.

In the CSV file you'll find corresponding values for the rings

DC Start is indicating the start of a data channel, and the controller port.  (Connect the beginning signal port of this ring back to the controller port listed)

PC Start is indicating the start of a power channel, and the controller port. (connect the beginning of this ring +/- back to the controller port listed)

PC End is indicating the end of a power channel, and the controller port. (connect the end of this ring +/- back to the controller port)

This (terribly drawn) image shows how I did a single set of rings.  

* Blue -
* Red +
* Green Signal

There are also the "inline" WAGO connectors, one per wire shown, between the pigtails of the connected rings, not shown in the drawing.

![image](https://github.com/user-attachments/assets/a5ddbd50-d67d-4f7e-bc08-59dbef7a361e)

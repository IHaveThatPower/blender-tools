# blender-tools

This is a collection of addons both written by me as well as other excellent Blender users. Modifications made to other users' addons are (generally) limited to ensuring compatibility with the version of Blender provided in [Thomas Schiex's PPA of Blender](https://launchpad.net/~thomas-schiex/+archive/ubuntu/blender).

## Remove Doubles Classic

*With gratitude and appreciation for the assistance of melak47, of the Scifi-Meshes community.*

Based on current selection, merge by distance with a configurable distance parameter.

Functionally identical to `Merge > By Distance`, but allows use of the `r` hotkey when added (early enough) to `Quick Favorites`, meaning one need only press `q > r` instead of `Alt M > b` or similar. Also stores its own separation threshold, independent of `Merge > By Distance`.

## Separate &amp; Clean

*Inspired by Lewis Niven (lewisnien), of the Scifi-Meshes community.*

Behaves like the standard `Separate > Selection` function, but allows the user to define several subsequent cleanup operations to be performed on the separated object:

* Delete Modifiers
* Remove Unused Materials
* Delete Vertex Groups
* Delete Shape Keys
* Delete UV Maps
* Delete Vertex Colors
* Delete Face Maps

The cleanup operations are executed in that order.

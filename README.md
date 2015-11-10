# Blender Hy REPL
Networked REPL into [Blender](https://www.blender.org/) using [Hy](https://github.com/hylang)

## Installation
On OSX

```
cd /Applications/blender.app/Contents/Resources/2.76/scripts/startup
git clone https://github.com/nasser/blenderhyrepl
```

If Blender is already running, reload scripts by hitting `F8` or using the `Reload Scripts` op from the spacebar menu.

Run blender from the terminal to see all output for now.

## Usage
1. Under the Misc tab in the Tools pane, hit the 'Start Hy REPL' button
2. `echo "(do (import bpy) (bpy.ops.mesh.primitive_monkey_add))" | nc localhost 1952`

## License
Copyright © 2015 Ramsey Nasser, provided under the [BSD License](https://opensource.org/licenses/BSD-3-Clause)
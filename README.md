# Pixel Squall bust for Bambu Lab X1 Carbon

A single-color Squall Leonhart bust in his FFVIII SeeD formal uniform, with
an intentionally pixelated appearance and the inscription
“You’re the best looking guy here” in raised pixel lettering.

## Print file

Open `models/squall_pixel_bust.stl` in Bambu Studio. Import in **millimetres**.
The file is **190 × 102.9 × 220.5 mm** (width × depth × height), upright with
its flat base at Z=0. It fits the X1C's 256 × 256 × 256 mm build volume.
Keep the model at 100% scale to retain 1.4 mm letter strokes and 9.8 mm tall
letters. The lettering projects 1.2 mm from the plaque surface.

Revision 4 uses measured outlines from the approved gray concept image for
layered stepped hair, blunt bangs, uniform details and pixel facial features.
The cheeks and jaw are narrowed and angular. Two broad, tilted hair sections
replace the repeated thin diagonal strips; the bangs are uneven and stepped. Depth,
unseen sides and back are reconstructed; the result remains an approximation.
The fixed visual target is `references/approved_gray_concept.png`; that file is
a generated concept, not a mesh render. Use `models/actual_mesh_preview.png`
to judge what the STL actually contains.

The STL is one connected, closed solid. It contains no color information;
use a single filament. `models/actual_mesh_preview.png` is rendered from the
actual exported STL. This manually constructed mesh interprets the approved
concept; it is not an exact recovery of the geometry from the generated image.

## Suggested Bambu Studio setup

- Printer: Bambu Lab X1 Carbon, standard 0.4 mm nozzle.
- Filament: matte gray PLA; select the profile matching your actual filament.
- Layer height: 0.16 mm, with 3 walls, 5 top layers, 4 bottom layers.
- Infill: 10–15% gyroid. Do not print at 100% infill.
- Orientation: upright, flat pedestal on the plate; center on the plate.
- Supports: start with automatic tree supports, including support on the model
  where needed. Inspect the bangs, chin, collar, and raised details in Preview.
  Use the slicer's standard PLA support interface and separation settings.
- Brim: 5 mm outer brim if needed for your plate/filament adhesion.
- Keep the normal X1C start routine and calibration enabled.

Slice and inspect all layers before printing. The geometry is verified, but
this project has not been sliced in Bambu Studio or physically printed.
Support removal around the bangs needs care. Actual time, material consumption,
and support needs come from your chosen slicer profile. No machine-specific
G-code is supplied.

## Rebuild

Python 3.12 with dependencies in `requirements.txt`:

```sh
python -m pip install -r requirements.txt
python scripts/create_bust.py
blender -b -t 4 -P scripts/render_preview.py
```

The generator unions solid primitives, checks manifold status, consistent face
winding, watertightness and a single connected component, then writes the STL
and `models/mesh_validation.json`. Blender 4.3.2 was used for the actual-mesh
preview. The editable geometry source is `scripts/create_bust.py`.

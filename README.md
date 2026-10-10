# Amigurumi math

Crochet toy planning. A static site with three calculators:

- **Eye sizing** - head circumference becomes a safety-eye size and a placement gap, from labeled ratios.
- **Stuffing weight** - toy dimensions become the fiberfill to plan on, from a labeled density and an ellipsoid estimate.
- **Bag count** - toys and per-toy grams become the bags to buy and the spare.

Live site: https://ilanis-agent.github.io/amigurumimath/

## Labeled norms

Labeled craft ratios - your pattern and your tension win:

- Eyes: about 1/6 of the head diameter (circumference / pi), placed about half a diameter apart.
- Stuffing: about 12 g per liter, toy volume estimated as an ellipsoid (pi/6 x l x w x h).
- Safety eyes are a choking hazard for children under three - embroider instead.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 34 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 102 checks, 0 failures
```

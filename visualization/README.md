# Transition rows and policy order

Each sheet plots one Bellman advantage for the same alternative action. The horizontal parameter is the probability p of the first successor. The depth varies another transition row. It does not affect the advantages in these examples, so both sheets are flat along it. All rewards outside the active row are zero, and the baseline value is zero.

With successor rewards (1, −1) and (2, −1), the advantages are 2p − 1 and 3p − 1. At p = 0 both prefer the baseline. At p = 2/5 the advantages are −1/5 and 1/5, giving opposite preferences. The pair (1, 0) and (1, 1) gives p and 1, exposing a boundary tie at zero.

Extract the ZIP and open index.html. Choose an example, move p and rotate the plot by dragging or using the rotation slider. The labels and preferences use exact fractions.

Run `python3 visualization/render.py` with Pillow and Arial fonts to rebuild the GIF and ZIP. Set `Q717_FONT_DIR` to the folder containing Arial.ttf and Arial Bold.ttf if they are elsewhere.

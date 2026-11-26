# Problem and proof

For two successor-dependent rewards, determine whether their expected discounted returns rank every stationary randomized policy identically for every transition kernel. [Original question](https://arxiv.org/pdf/2411.15951v1#page=94)

1. Fix a baseline policy. Discounted occupancy flow lets the nonbaseline coordinates vary freely near a fully mixed policy. Subtracting baseline value from each row gives the advantage vector up to a constant that does not change comparisons.
2. A block determinant gives the numerator of each advantage. Two linear orders agree on an open set exactly when the vectors lie on the same positive ray or both vanish. Minors and componentwise signs encode that condition.
3. For each product face, factor each nonzero component. A factor with opposite vertex signs has an interior regular zero. Sign equality forces the other polynomial to contain that factor. Other factors have strict constant interior signs. Check their orientation at one common nonzero point.
4. The relative interiors cover every kernel and an explicit product grid locates an orientation witness. Another finite grid checks the quadratic minor identities.

With state–action rewards, a self-loop kernel and redirections toward fixed anchor states force one positive scale and one additive constant across the whole reward table. [Full proof](../paper/manuscript.pdf)

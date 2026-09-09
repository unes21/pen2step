# Analiz: ablation_n19.json  (n=19)

## Koşul başına bootstrap %95 GA
| koşul | SVR [95% GA] | F [95% GA] | Chamfer(mm) [95% GA] | DimE [95% GA] | n_valid |
|---|---|---|---|---|---|
| raw_mv | 0.368 [0.158, 0.579] | 0.000 [0.000, 0.000] | 44.242 [33.241, 57.435] | 0.996 [0.995, 0.998] | 7/19 |
| multiview_n3 | 1.000 [1.000, 1.000] | 0.095 [0.061, 0.135] | 26.401 [21.504, 31.389] | 0.526 [0.419, 0.656] | 19/19 |

## Ölçülü (has_dims) vs ölçüsüz alt-küme
| koşul | grup | n | SVR | F |
|---|---|---|---|---|
| raw_mv | ölçülü | 6 | 0.167 | 0.000 |
| raw_mv | ölçüsüz | 13 | 0.462 | 0.000 |
| multiview_n3 | ölçülü | 6 | 1.000 | 0.070 |
| multiview_n3 | ölçüsüz | 13 | 1.000 | 0.107 |

## Aile bazında (SVR / F)

**raw_mv**
| family | n | SVR | F |
|---|---|---|---|
| bracket_hole | 1 | 0.000 | 0.000 |
| cap_screw | 1 | 1.000 | 0.000 |
| chamfer_block | 1 | 1.000 | 0.000 |
| cone_hole | 1 | 0.000 | 0.000 |
| flanged_bushing | 1 | 0.000 | 0.000 |
| hex_bolt | 1 | 1.000 | 0.000 |
| keyed_cylinder | 1 | 1.000 | 0.000 |
| rod | 1 | 0.000 | 0.000 |
| rounded_plate | 1 | 0.000 | 0.000 |
| square_tube | 1 | 0.000 | 0.000 |
| staircase | 1 | 0.000 | 0.000 |
| stepped_block | 2 | 0.000 | 0.000 |
| stepped_shaft | 1 | 1.000 | 0.000 |
| t_block | 1 | 1.000 | 0.000 |
| tube | 1 | 1.000 | 0.000 |
| u_channel | 1 | 0.000 | 0.000 |
| washer | 2 | 0.000 | 0.000 |

**multiview_n3**
| family | n | SVR | F |
|---|---|---|---|
| bracket_hole | 1 | 1.000 | 0.005 |
| cap_screw | 1 | 1.000 | 0.052 |
| chamfer_block | 1 | 1.000 | 0.022 |
| cone_hole | 1 | 1.000 | 0.000 |
| flanged_bushing | 1 | 1.000 | 0.160 |
| hex_bolt | 1 | 1.000 | 0.054 |
| keyed_cylinder | 1 | 1.000 | 0.092 |
| rod | 1 | 1.000 | 0.191 |
| rounded_plate | 1 | 1.000 | 0.053 |
| square_tube | 1 | 1.000 | 0.042 |
| staircase | 1 | 1.000 | 0.045 |
| stepped_block | 2 | 1.000 | 0.141 |
| stepped_shaft | 1 | 1.000 | 0.227 |
| t_block | 1 | 1.000 | 0.078 |
| tube | 1 | 1.000 | 0.286 |
| u_channel | 1 | 1.000 | 0.067 |
| washer | 2 | 1.000 | 0.076 |

## Eşlemeli testler
| A | B | McNemar p (validite) | Wilcoxon p (F) | b01/b10 |
|---|---|---|---|---|
| raw_mv | multiview_n3 | 0.0004883 | 0.01562 | 12/0 |
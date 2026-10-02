# Shared wrong assumptions on held-out transitions (final pools, all programs agree and are wrong)


## Error type × action kind, by policy

| group | missed change / move | missed change / click | missed change / noop | hallucinated change / move | hallucinated change / click | hallucinated change / noop | wrong change / move | wrong change / click | wrong change / noop | total |
|---|---|---|---|---|---|---|---|---|---|---|
| disagree | 194 | 131 | 172 | 41 | 18 | 0 | 229 | 76 | 5 | 866 |
| llm | 269 | 211 | 213 | 31 | 12 | 0 | 34 | 76 | 0 | 846 |
| random | 81 | 188 | 74 | 14 | 0 | 0 | 189 | 49 | 41 | 636 |

## Error type × action kind, by environment

| group | missed change / move | missed change / click | missed change / noop | hallucinated change / move | hallucinated change / click | hallucinated change / noop | wrong change / move | wrong change / click | wrong change / noop | total |
|---|---|---|---|---|---|---|---|---|---|---|
| disease | 2 | 7 | 0 | 0 | 18 | 0 | 143 | 0 | 0 | 170 |
| egg | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 11 |
| gravity | 108 | 124 | 144 | 0 | 0 | 0 | 82 | 0 | 21 | 479 |
| grow | 132 | 158 | 139 | 0 | 0 | 0 | 63 | 0 | 0 | 492 |
| ice | 232 | 118 | 151 | 0 | 0 | 0 | 28 | 77 | 0 | 606 |
| magnets | 11 | 0 | 0 | 86 | 0 | 0 | 39 | 0 | 0 | 136 |
| paint | 0 | 31 | 0 | 0 | 12 | 0 | 0 | 107 | 0 | 150 |
| wind | 48 | 92 | 25 | 0 | 0 | 0 | 97 | 17 | 25 | 304 |

## Examples


### disease — hallucinated change (nothing actually happens) — click (18 cases)

- [disagree s3] action `click 6 6` (first-firing clauses [])
  - predicted: `(6,6):a>.`
  - actual: `no change`
- [disagree s3] action `click 7 5` (first-firing clauses [0, 1])
  - predicted: `(7,5):a>.`
  - actual: `no change`
- [disagree s3] action `click 3 5` (first-firing clauses [1])
  - predicted: `(3,5):a>.`
  - actual: `no change`

### disease — missed change (predicted nothing happens) — click (7 cases)

- [disagree s3] action `click 2 10` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,3):a>d`
- [llm s3] action `click 2 10` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,3):a>d`
- [llm s2] action `click 2 10` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,3):a>d`

### disease — missed change (predicted nothing happens) — move (2 cases)

- [llm s2] action `down` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(6,5):a>.`
- [llm s2] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(7,6):a>.`

### disease — wrong change — move (143 cases)

- [random s3] action `left` (first-firing clauses [2])
  - predicted: `(3,3):.>d (4,3):d>.`
  - actual: `(3,3):.>d`
- [random s0] action `up` (first-firing clauses [])
  - predicted: `(3,2):.>d (3,3):d>.`
  - actual: `(6,4):.>a (6,5):a>.`
- [disagree s2] action `down` (first-firing clauses [])
  - predicted: `(1,3):d>. (1,4):.>d`
  - actual: `(8,5):a>. (8,6):.>a`

### egg — missed change (predicted nothing happens) — move (11 cases)

- [random s0] action `down` (first-firing clauses [4])
  - predicted: `no change`
  - actual: `(7,9):t>. (8,9):t>. (9,9):t>. (6,10):t>. (10,10):t>. (6,13):.>t (10,13):.>t (7,14):.>t (8,14):.>t (9,14):.>t`
- [random s0] action `down` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(8,10):t>. (9,10):t>. (10,10):t>. (7,11):t>. (11,11):t>. (7,14):.>t (11,14):.>t (8,15):.>t (9,15):.>t (10,15):.>t`
- [random s0] action `down` (first-firing clauses [4])
  - predicted: `no change`
  - actual: `(3,9):t>. (4,9):t>. (5,9):t>. (2,10):t>. (6,10):t>. (2,13):.>t (6,13):.>t (3,14):.>t (4,14):.>t (5,14):.>t`

### gravity — missed change (predicted nothing happens) — click (124 cases)

- [disagree s3] action `click 1 11` (first-firing clauses [4])
  - predicted: `no change`
  - actual: `(1,10):.>b (2,10):.>b (1,11):.>b (2,11):.>b`
- [random s0] action `click 7 15` (first-firing clauses [8])
  - predicted: `no change`
  - actual: `(0,15):b>.`
- [disagree s3] action `click 0 5` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(1,3):b>. (2,3):b>. (0,4):.>b (0,5):.>b (1,5):.>b (2,5):.>b`

### gravity — missed change (predicted nothing happens) — move (108 cases)

- [llm s3] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,6):b>. (1,6):b>. (2,6):b>. (0,8):.>b (1,8):.>b (2,8):.>b (15,11):b>. (15,13):.>b`
- [llm s3] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(10,0):b>. (12,0):.>b (10,1):b>. (12,1):.>b (14,14):b>. (14,15):b>.`
- [llm s0] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,1):b>. (15,1):.>b (13,2):b>. (15,2):.>b (1,5):b>. (3,5):.>b (1,6):b>. (3,6):.>b`

### gravity — missed change (predicted nothing happens) — noop (144 cases)

- [llm s3] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(1,0):b>. (2,0):b>. (1,2):.>b (2,2):.>b`
- [disagree s2] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(1,9):b>. (3,9):.>b (1,10):b>. (3,10):.>b`
- [llm s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,7):b>. (14,7):b>. (13,9):.>b (14,9):.>b`

### gravity — wrong change — move (82 cases)

- [disagree s0] action `right` (first-firing clauses [])
  - predicted: `(15,10):b>. (15,11):b>.`
  - actual: `(15,10):b>. (15,12):.>b`
- [disagree s0] action `up` (first-firing clauses [])
  - predicted: `(13,4):.>b (14,4):.>b (13,6):b>. (14,6):b>.`
  - actual: `(13,5):b>. (14,5):b>. (13,7):.>b (14,7):.>b`
- [disagree s1] action `up` (first-firing clauses [])
  - predicted: `(14,11):.>b (15,11):b>. (14,12):.>b (15,12):b>.`
  - actual: `(15,11):b>. (15,13):.>b`

### gravity — wrong change — noop (21 cases)

- [random s3] action `noop` (first-firing clauses [])
  - predicted: `(15,1):.>b (15,3):b>. (13,9):.>b (14,9):.>b (13,11):b>. (14,11):b>.`
  - actual: `(15,2):b>. (15,4):.>b (13,10):b>. (14,10):b>. (13,12):.>b (14,12):.>b`
- [random s3] action `noop` (first-firing clauses [])
  - predicted: `(0,12):.>b (1,12):.>b (2,12):.>b (0,14):b>. (1,14):b>. (2,14):b>. (12,14):.>b (13,14):.>b (12,15):b>. (13,15):b>.`
  - actual: `(0,13):b>. (1,13):b>. (2,13):b>. (0,15):.>b (1,15):.>b (2,15):.>b (12,15):b>. (13,15):b>.`
- [random s2] action `noop` (first-firing clauses [])
  - predicted: `(15,1):b>. (15,3):.>b`
  - actual: `(15,1):b>. (15,3):.>b (15,15):b>.`

### grow — missed change (predicted nothing happens) — click (158 cases)

- [llm s3] action `click 15 2` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,4):b>. (13,5):.>b (13,6):b>. (13,7):.>b (12,15):b>.`
- [random s0] action `click 12 13` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(12,14):b>.`
- [llm s2] action `click 12 13` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(12,14):b>.`

### grow — missed change (predicted nothing happens) — move (132 cases)

- [disagree s3] action `down` (first-firing clauses [1, 2])
  - predicted: `no change`
  - actual: `(13,14):b>g`
- [random s1] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,3):.>b (13,4):b>. (13,5):.>b (12,13):b>. (12,14):.>b`
- [random s0] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(12,4):b>. (12,5):.>b (11,8):b>. (11,9):.>b`

### grow — missed change (predicted nothing happens) — noop (139 cases)

- [random s1] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(12,8):b>. (12,9):.>b (11,12):b>. (11,13):.>b`
- [llm s1] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(14,3):.>b (12,10):b>. (12,11):.>b`
- [disagree s2] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(14,3):.>b (12,10):b>. (12,11):.>b`

### grow — wrong change — move (63 cases)

- [random s3] action `left` (first-firing clauses [])
  - predicted: `(12,0):.>a (15,0):a>. (12,1):.>a (15,1):a>. (12,2):.>a (15,2):a>.`
  - actual: `(12,0):.>a (12,1):.>a (12,2):.>a (13,5):b>. (13,6):.>b`
- [random s3] action `left` (first-firing clauses [])
  - predicted: `(13,0):.>a (15,0):a>. (13,1):.>a (15,1):a>. (13,2):.>a (15,2):a>.`
  - actual: `(13,0):.>a (13,1):.>a (13,2):.>a`
- [disagree s3] action `right` (first-firing clauses [])
  - predicted: `(12,0):a>. (12,1):a>. (12,2):a>.`
  - actual: `(12,0):a>. (12,1):a>. (12,2):a>. (14,3):.>b`

### ice — missed change (predicted nothing happens) — click (118 cases)

- [random s2] action `click 13 15` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,0):o>a (1,0):o>a (0,1):o>a (1,1):o>a (3,3):b>l (4,4):b>l`
- [disagree s0] action `click 1 11` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,0):a>o (1,0):a>o (0,1):a>o (1,1):a>o`
- [disagree s2] action `click 12 13` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,0):o>a (1,0):o>a (0,1):o>a (1,1):o>a (4,6):b>l (3,8):b>l`

### ice — missed change (predicted nothing happens) — move (232 cases)

- [llm s2] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,0):a>. (5,0):.>a (3,3):b>. (3,4):.>b`
- [random s0] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,2):b>. (4,3):.>b (4,5):b>. (4,6):.>b (3,12):b>. (3,13):.>b`
- [disagree s3] action `left` (first-firing clauses [0])
  - predicted: `no change`
  - actual: `(2,0):.>a (5,0):a>.`

### ice — missed change (predicted nothing happens) — noop (151 cases)

- [disagree s2] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,4):b>. (4,5):.>b`
- [random s1] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(6,1):l>. (6,2):.>l (4,4):l>. (4,5):.>l (4,7):l>. (4,8):.>l (3,14):l>. (3,15):.>l`
- [llm s2] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(3,1):b>. (3,2):.>b`

### ice — wrong change — click (77 cases)

- [llm s0] action `click 1 0` (first-firing clauses [])
  - predicted: `(0,0):o>a (1,0):o>a (0,1):o>a (1,1):o>a`
  - actual: `(0,0):o>a (1,0):o>a (0,1):o>a (1,1):o>a (4,11):b>l`
- [llm s0] action `click 6 0` (first-firing clauses [])
  - predicted: `(5,0):a>o (6,0):a>o (7,0):a>o`
  - actual: `(0,0):a>o (1,0):a>o (0,1):a>o (1,1):a>o (4,5):l>b (3,9):l>b`
- [disagree s2] action `click 1 1` (first-firing clauses [])
  - predicted: `(0,0):o>a (1,0):a>o (2,0):a>o (0,1):o>a (1,1):o>a`
  - actual: `(0,0):o>a (0,1):o>a (1,1):o>a`

### ice — wrong change — move (28 cases)

- [random s0] action `left` (first-firing clauses [])
  - predicted: `(2,0):.>a (5,0):a>.`
  - actual: `(2,0):.>a (5,0):a>. (4,4):l>. (4,5):.>l (3,6):l>. (3,7):.>l`
- [random s2] action `left` (first-firing clauses [])
  - predicted: `(2,0):.>a (5,0):a>. (3,4):.>l (4,4):l>. (2,6):.>l (3,6):l>.`
  - actual: `(2,0):.>a (5,0):a>. (4,4):l>. (4,5):.>l (3,6):l>. (3,7):.>l`
- [random s0] action `left` (first-firing clauses [])
  - predicted: `(3,0):.>a (6,0):a>.`
  - actual: `(3,0):.>a (6,0):a>. (4,8):l>. (4,9):.>l (3,10):l>. (3,11):.>l`

### magnets — hallucinated change (nothing actually happens) — move (86 cases)

- [disagree s3] action `left` (first-firing clauses [])
  - predicted: `(5,8):.>b (6,8):b>. (5,9):.>b (6,9):b>.`
  - actual: `no change`
- [disagree s1] action `left` (first-firing clauses [0])
  - predicted: `(5,6):.>b (6,6):b>. (5,7):.>b (6,7):b>.`
  - actual: `no change`
- [llm s3] action `up` (first-firing clauses [])
  - predicted: `(6,7):.>b (6,9):b>.`
  - actual: `no change`

### magnets — missed change (predicted nothing happens) — move (11 cases)

- [llm s0] action `left` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,7):b>. (0,8):b>.`
- [disagree s0] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,8):.>b (0,9):.>b`
- [random s0] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,8):.>b (0,9):.>b`

### magnets — wrong change — move (39 cases)

- [random s0] action `down` (first-firing clauses [])
  - predicted: `(6,8):b>. (6,9):b>. (6,10):.>b`
  - actual: `(6,8):b>. (6,10):.>b`
- [random s0] action `down` (first-firing clauses [])
  - predicted: `(5,5):b>. (5,6):b>. (5,7):.>b`
  - actual: `(5,5):b>. (5,6):b>. (6,6):.>b (6,7):.>b`
- [random s0] action `down` (first-firing clauses [])
  - predicted: `(6,4):b>. (6,5):b>. (6,6):.>b`
  - actual: `(6,4):b>. (6,6):.>b`

### paint — hallucinated change (nothing actually happens) — click (12 cases)

- [llm s0] action `click 1 0` (first-firing clauses [])
  - predicted: `(1,0):g>o`
  - actual: `no change`
- [llm s0] action `click 13 4` (first-firing clauses [])
  - predicted: `(13,4):r>o`
  - actual: `no change`
- [llm s0] action `click 2 10` (first-firing clauses [])
  - predicted: `(2,10):g>o`
  - actual: `no change`

### paint — missed change (predicted nothing happens) — click (31 cases)

- [llm s0] action `click 15 3` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(15,3):o>g`
- [llm s3] action `click 15 3` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(15,3):o>g`
- [disagree s1] action `click 15 12` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(15,12):g>b`

### paint — wrong change — click (107 cases)

- [llm s2] action `click 15 12` (first-firing clauses [])
  - predicted: `(15,12):.>r`
  - actual: `(15,12):.>g`
- [llm s0] action `click 13 4` (first-firing clauses [])
  - predicted: `(13,4):.>o`
  - actual: `(13,4):.>r`
- [random s3] action `click 15 2` (first-firing clauses [])
  - predicted: `(15,2):.>r`
  - actual: `(15,2):.>b`

### wind — missed change (predicted nothing happens) — click (92 cases)

- [random s1] action `click 8 1` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,5):l>. (6,5):l>. (10,5):l>. (14,5):l>. (3,6):.>l (7,6):.>l (11,6):.>l (15,6):.>l (0,10):l>. (4,10):l>. (8,10):l>. (12,10):l>. (1,11):.>l (5,11):.>l (9,11):.>l (13,11):.>l`
- [llm s3] action `click 1 11` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (1,3):.>l (5,3):.>l (9,3):.>l (13,3):.>l (1,7):l>. (5,7):l>. (9,7):l>. (0,8):.>l (4,8):.>l (8,8):.>l`
- [random s2] action `click 0 1` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(3,5):l>. (7,5):l>. (11,5):l>. (2,6):.>l (6,6):.>l (10,6):.>l (3,10):l>. (7,10):l>. (2,11):.>l (6,11):.>l`

### wind — missed change (predicted nothing happens) — move (48 cases)

- [random s0] action `up` (first-firing clauses [5])
  - predicted: `no change`
  - actual: `(2,2):.>l (6,2):.>l (10,2):.>l (14,2):.>l`
- [random s1] action `right` (first-firing clauses [4, 5])
  - predicted: `no change`
  - actual: `(2,2):.>l (6,2):.>l (10,2):.>l (14,2):.>l`
- [llm s0] action `left` (first-firing clauses [5])
  - predicted: `no change`
  - actual: `(2,2):.>l (6,2):.>l (10,2):.>l (14,2):.>l`

### wind — missed change (predicted nothing happens) — noop (25 cases)

- [disagree s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,4):l>. (4,4):l>. (8,4):l>. (12,4):l>. (3,5):.>l (7,5):.>l (11,5):.>l`
- [disagree s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,5):l>. (6,5):l>. (10,5):l>. (14,5):l>. (3,6):.>l (7,6):.>l (11,6):.>l (15,6):.>l (1,10):l>. (5,10):l>. (9,10):l>. (13,10):l>. (2,11):.>l (6,11):.>l (10,11):.>l (14,11):.>l`
- [disagree s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(1,5):l>. (5,5):l>. (9,5):l>. (13,5):l>. (1,6):.>l (5,6):.>l (9,6):.>l (13,6):.>l`

### wind — wrong change — click (17 cases)

- [disagree s1] action `click 16 1` (first-firing clauses [])
  - predicted: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (2,3):.>l (6,3):.>l (10,3):.>l (14,3):.>l (1,7):l>. (5,7):l>. (9,7):l>. (13,7):l>. (1,8):.>l (5,8):.>l (9,8):.>l (13,8):.>l (3,12):l>. (7,12):l>. (11,12):l>. (15,12):l>. (3,13):.`
  - actual: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (1,3):.>l (5,3):.>l (9,3):.>l (13,3):.>l (1,7):l>. (5,7):l>. (9,7):l>. (13,7):l>. (0,8):.>l (4,8):.>l (8,8):.>l (12,8):.>l (3,12):l>. (7,12):l>. (11,12):l>. (15,12):l>. (2,13):.>`
- [disagree s1] action `click 6 1` (first-firing clauses [1])
  - predicted: `(1,4):l>. (5,4):l>. (9,4):l>. (13,4):l>. (1,5):.>l (5,5):.>l (9,5):.>l (13,5):.>l (3,9):l>. (7,9):l>. (11,9):l>. (3,10):.>l (7,10):.>l (11,10):.>l`
  - actual: `(1,4):l>. (5,4):l>. (9,4):l>. (13,4):l>. (2,5):.>l (6,5):.>l (10,5):.>l (14,5):.>l (3,9):l>. (7,9):l>. (11,9):l>. (0,10):.>l (4,10):.>l (8,10):.>l (12,10):.>l`
- [disagree s1] action `click 6 0` (first-firing clauses [])
  - predicted: `(3,3):l>. (7,3):l>. (11,3):l>. (15,3):l>. (3,4):.>l (7,4):.>l (11,4):.>l (15,4):.>l (8,8):l>. (12,8):l>. (16,8):l>. (8,9):.>l (12,9):.>l (16,9):.>l (13,13):l>. (13,14):.>l`
  - actual: `(3,3):l>. (7,3):l>. (11,3):l>. (15,3):l>. (4,4):.>l (8,4):.>l (12,4):.>l (16,4):.>l (8,8):l>. (12,8):l>. (16,8):l>. (9,9):.>l (13,9):.>l (13,13):l>. (14,14):.>l`

### wind — wrong change — move (97 cases)

- [disagree s2] action `down` (first-firing clauses [])
  - predicted: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (2,3):.>l (6,3):.>l (10,3):.>l (14,3):.>l (7,7):l>. (11,7):l>. (15,7):l>. (7,8):.>l (11,8):.>l (15,8):.>l (12,12):l>. (16,12):l>. (12,13):.>l (16,13):.>l`
  - actual: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (3,3):.>l (7,3):.>l (11,3):.>l (15,3):.>l (7,7):l>. (11,7):l>. (15,7):l>. (8,8):.>l (12,8):.>l (16,8):.>l (12,12):l>. (16,12):l>. (13,13):.>l`
- [disagree s3] action `down` (first-firing clauses [])
  - predicted: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (2,3):.>l (6,3):.>l (10,3):.>l (14,3):.>l (2,7):l>. (6,7):l>. (10,7):l>. (14,7):l>. (2,8):.>l (6,8):.>l (10,8):.>l (14,8):.>l`
  - actual: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (1,3):.>l (5,3):.>l (9,3):.>l (13,3):.>l (2,7):l>. (6,7):l>. (10,7):l>. (14,7):l>. (1,8):.>l (5,8):.>l (9,8):.>l (13,8):.>l`
- [disagree s2] action `down` (first-firing clauses [])
  - predicted: `(1,4):l>. (5,4):l>. (9,4):l>. (13,4):l>. (1,5):.>l (5,5):.>l (9,5):.>l (13,5):.>l`
  - actual: `(1,4):l>. (5,4):l>. (9,4):l>. (13,4):l>. (0,5):.>l (4,5):.>l (8,5):.>l (12,5):.>l`

### wind — wrong change — noop (25 cases)

- [random s3] action `noop` (first-firing clauses [])
  - predicted: `(0,4):l>. (4,4):l>. (8,4):l>. (12,4):l>. (0,5):.>l (4,5):.>l (8,5):.>l (12,5):.>l (3,9):l>. (7,9):l>. (11,9):l>. (3,10):.>l (7,10):.>l (11,10):.>l (1,14):l>. (5,14):l>. (9,14):l>. (13,14):l>. (1,15):.>l (5,15):.>l (9,15)`
  - actual: `(0,4):l>. (4,4):l>. (8,4):l>. (12,4):l>. (3,5):.>l (7,5):.>l (11,5):.>l (3,9):l>. (7,9):l>. (11,9):l>. (2,10):.>l (6,10):.>l (10,10):.>l (1,14):l>. (5,14):l>. (9,14):l>. (13,14):l>. (0,15):.>l (4,15):.>l (8,15):.>l (12,1`
- [random s3] action `noop` (first-firing clauses [])
  - predicted: `(2,5):l>. (6,5):l>. (10,5):l>. (14,5):l>. (2,6):.>l (6,6):.>l (10,6):.>l (14,6):.>l (1,10):l>. (5,10):l>. (9,10):l>. (13,10):l>. (1,11):.>l (5,11):.>l (9,11):.>l (13,11):.>l`
  - actual: `(2,5):l>. (6,5):l>. (10,5):l>. (14,5):l>. (3,6):.>l (7,6):.>l (11,6):.>l (15,6):.>l (1,10):l>. (5,10):l>. (9,10):l>. (13,10):l>. (2,11):.>l (6,11):.>l (10,11):.>l (14,11):.>l`
- [disagree s2] action `noop` (first-firing clauses [])
  - predicted: `(3,6):l>. (7,6):l>. (11,6):l>. (3,7):.>l (7,7):.>l (11,7):.>l`
  - actual: `(2,2):.>l (6,2):.>l (10,2):.>l (14,2):.>l (3,6):l>. (7,6):l>. (11,6):l>. (2,7):.>l (6,7):.>l (10,7):.>l`

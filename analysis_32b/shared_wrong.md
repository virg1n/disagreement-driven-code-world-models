# Shared wrong assumptions on held-out transitions (final pools, all programs agree and are wrong)


## Error type × action kind, by policy

| group | missed change / move | missed change / click | missed change / noop | hallucinated change / move | hallucinated change / click | hallucinated change / noop | wrong change / move | wrong change / click | wrong change / noop | total |
|---|---|---|---|---|---|---|---|---|---|---|
| disagree | 439 | 52 | 125 | 30 | 0 | 0 | 40 | 50 | 9 | 745 |
| llm | 572 | 69 | 160 | 6 | 0 | 0 | 9 | 7 | 0 | 823 |
| random | 137 | 93 | 64 | 6 | 1 | 0 | 87 | 70 | 0 | 458 |

## Error type × action kind, by environment

| group | missed change / move | missed change / click | missed change / noop | hallucinated change / move | hallucinated change / click | hallucinated change / noop | wrong change / move | wrong change / click | wrong change / noop | total |
|---|---|---|---|---|---|---|---|---|---|---|
| disease | 67 | 4 | 0 | 0 | 0 | 0 | 43 | 0 | 0 | 114 |
| egg | 75 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 81 |
| gravity | 109 | 27 | 37 | 0 | 0 | 0 | 32 | 9 | 9 | 223 |
| grow | 239 | 90 | 102 | 0 | 1 | 0 | 9 | 7 | 0 | 448 |
| ice | 323 | 0 | 110 | 2 | 0 | 0 | 41 | 106 | 0 | 582 |
| magnets | 8 | 0 | 0 | 34 | 0 | 0 | 11 | 0 | 0 | 53 |
| paint | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| wind | 327 | 87 | 100 | 0 | 0 | 0 | 0 | 5 | 0 | 519 |

## Examples


### disease — missed change (predicted nothing happens) — click (4 cases)

- [random s1] action `click 2 10` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,3):a>d`
- [llm s0] action `click 2 10` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,3):a>d`
- [disagree s0] action `click 2 10` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,3):a>d`

### disease — missed change (predicted nothing happens) — move (67 cases)

- [llm s1] action `left` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(3,3):.>d (4,3):d>.`
- [llm s1] action `left` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,5):.>a (3,5):a>.`
- [llm s1] action `left` (first-firing clauses [2])
  - predicted: `no change`
  - actual: `(6,4):.>a (7,4):a>.`

### disease — wrong change — move (43 cases)

- [random s0] action `down` (first-firing clauses [5])
  - predicted: `(2,2):d>. (2,3):.>d`
  - actual: `(3,5):a>. (3,6):.>a`
- [random s0] action `right` (first-firing clauses [])
  - predicted: `(1,1):d>. (2,1):.>d`
  - actual: `(7,5):a>. (8,5):.>a`
- [random s0] action `right` (first-firing clauses [])
  - predicted: `(3,2):d>. (4,2):.>d (4,4):d>. (5,4):.>d`
  - actual: `(3,2):d>. (4,2):.>d`

### egg — hallucinated change (nothing actually happens) — move (6 cases)

- [disagree s1] action `down` (first-firing clauses [])
  - predicted: `(4,12):t>. (8,12):t>. (4,15):.>t (8,15):.>t`
  - actual: `no change`
- [disagree s1] action `down` (first-firing clauses [])
  - predicted: `(3,12):t>. (7,12):t>. (3,15):.>t (7,15):.>t`
  - actual: `no change`
- [disagree s1] action `down` (first-firing clauses [4])
  - predicted: `(5,12):t>. (9,12):t>. (5,15):.>t (9,15):.>t`
  - actual: `no change`

### egg — missed change (predicted nothing happens) — move (75 cases)

- [random s1] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,10):.>t (5,10):.>t (6,10):.>t (3,11):.>t (7,11):.>t (3,14):t>. (7,14):t>. (4,15):t>. (5,15):t>. (6,15):t>.`
- [disagree s0] action `right` (first-firing clauses [2])
  - predicted: `no change`
  - actual: `(3,10):t>. (6,10):.>t (2,11):t>. (7,11):.>t (2,12):t>. (7,12):.>t (2,13):t>. (7,13):.>t (3,14):t>. (6,14):.>t`
- [random s0] action `down` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(5,10):t>. (6,10):t>. (7,10):t>. (4,11):t>. (8,11):t>. (4,14):.>t (8,14):.>t (5,15):.>t (6,15):.>t (7,15):.>t`

### gravity — missed change (predicted nothing happens) — click (27 cases)

- [llm s1] action `click 15 7` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,1):.>b (14,1):.>b (13,3):b>. (14,3):b>. (1,5):.>b (2,5):.>b (1,7):b>. (2,7):b>.`
- [random s0] action `click 14 1` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,0):b>. (15,0):.>b (13,1):b>. (15,1):.>b`
- [llm s1] action `click 7 15` (first-firing clauses [8])
  - predicted: `no change`
  - actual: `(0,7):b>r (1,7):b>. (2,7):b>. (0,9):.>b (1,9):.>b (2,9):.>b (15,12):b>. (15,14):.>b`

### gravity — missed change (predicted nothing happens) — move (109 cases)

- [llm s1] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(1,1):.>b (2,1):.>b`
- [llm s1] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(1,15):b>.`
- [llm s0] action `left` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,12):b>. (1,12):b>. (2,12):b>. (0,14):.>b (1,14):.>b (2,14):.>b (12,14):b>. (13,14):b>.`

### gravity — missed change (predicted nothing happens) — noop (37 cases)

- [llm s1] action `noop` (first-firing clauses [0])
  - predicted: `no change`
  - actual: `(1,15):.>b (3,15):b>.`
- [llm s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(15,2):b>. (15,4):.>b (13,10):b>. (14,10):b>. (13,12):.>b (14,12):.>b`
- [llm s1] action `noop` (first-firing clauses [1])
  - predicted: `no change`
  - actual: `(10,2):b>. (12,2):.>b (10,3):b>. (12,3):.>b`

### gravity — wrong change — click (9 cases)

- [disagree s1] action `click 4 9` (first-firing clauses [])
  - predicted: `(4,9):b>. (5,9):b>. (4,11):.>b (5,11):.>b`
  - actual: `(4,9):b>. (6,9):.>b (4,10):b>. (6,10):.>b`
- [disagree s1] action `click 15 7` (first-firing clauses [])
  - predicted: `(2,0):b>. (3,0):b>. (2,1):.>b (3,1):.>b`
  - actual: `(2,0):b>. (3,0):b>.`
- [disagree s1] action `click 10 14` (first-firing clauses [])
  - predicted: `(7,5):b>. (8,5):b>. (7,7):.>b (8,7):.>b`
  - actual: `(7,5):b>. (9,5):.>b (7,6):b>. (9,6):.>b (10,14):b>. (12,14):.>b (10,15):b>. (12,15):.>b`

### gravity — wrong change — move (32 cases)

- [disagree s1] action `left` (first-firing clauses [])
  - predicted: `(10,5):b>. (11,5):b>. (10,7):.>b (11,7):.>b`
  - actual: `(10,5):b>. (12,5):.>b (10,6):b>. (12,6):.>b (13,14):b>. (15,14):.>b (13,15):b>. (15,15):.>b`
- [disagree s1] action `down` (first-firing clauses [2])
  - predicted: `(15,0):b>. (15,2):.>b`
  - actual: `(15,1):b>.`
- [disagree s1] action `up` (first-firing clauses [])
  - predicted: `(3,9):b>. (4,9):b>. (3,11):.>b (4,11):.>b`
  - actual: `(3,9):b>. (5,9):.>b (3,10):b>. (5,10):.>b`

### gravity — wrong change — noop (9 cases)

- [disagree s1] action `noop` (first-firing clauses [])
  - predicted: `(1,9):b>. (2,9):b>. (1,11):.>b (2,11):.>b`
  - actual: `(1,8):.>b (2,8):.>b (1,10):b>. (2,10):b>.`
- [disagree s1] action `noop` (first-firing clauses [])
  - predicted: `(6,5):b>. (7,5):b>. (6,7):.>b (7,7):.>b`
  - actual: `(6,5):b>. (8,5):.>b (6,6):b>. (8,6):.>b (9,14):b>. (11,14):.>b (9,15):b>. (11,15):.>b`
- [disagree s1] action `noop` (first-firing clauses [])
  - predicted: `(6,9):b>. (7,9):b>. (6,11):.>b (7,11):.>b`
  - actual: `(6,9):b>. (8,9):.>b (6,10):b>. (8,10):.>b`

### grow — hallucinated change (nothing actually happens) — click (1 cases)

- [random s1] action `click 1 11` (first-firing clauses [])
  - predicted: `(0,0):o>. (3,0):.>o (0,1):o>. (3,1):.>o (0,2):o>. (3,2):.>o`
  - actual: `no change`

### grow — missed change (predicted nothing happens) — click (90 cases)

- [random s0] action `click 8 1` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,4):b>. (13,5):.>b (14,5):b>. (14,6):.>b`
- [random s0] action `click 15 2` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,4):b>. (13,5):.>b (13,6):b>. (13,7):.>b (12,15):b>.`
- [llm s1] action `click 9 15` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,11):b>. (13,12):.>b (14,12):b>. (14,13):.>b`

### grow — missed change (predicted nothing happens) — move (239 cases)

- [random s0] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,7):b>. (13,8):.>b (14,8):b>. (14,9):.>b`
- [llm s0] action `left` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(9,0):.>a (13,0):a>. (9,1):.>a (13,1):a>. (9,2):.>a (13,2):a>.`
- [disagree s1] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,0):a>. (13,1):a>. (13,2):a>.`

### grow — missed change (predicted nothing happens) — noop (102 cases)

- [disagree s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(12,5):b>. (12,6):.>b (13,8):b>. (13,9):.>b`
- [random s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,11):b>. (13,12):.>b`
- [disagree s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,9):b>. (13,10):.>b`

### grow — wrong change — click (7 cases)

- [disagree s0] action `click 0 1` (first-firing clauses [7])
  - predicted: `(0,0):o>. (3,0):.>o (0,1):o>. (3,1):.>o (0,2):o>. (3,2):.>o`
  - actual: `(0,0):o>. (3,0):.>o (0,1):o>. (3,1):.>o (0,2):o>. (3,2):.>o (12,7):b>. (12,8):.>b (11,11):b>. (11,12):.>b`
- [random s1] action `click 0 1` (first-firing clauses [7])
  - predicted: `(0,0):o>. (3,0):.>o (0,1):o>. (3,1):.>o (0,2):o>. (3,2):.>o`
  - actual: `(0,0):o>. (3,0):.>o (0,1):o>. (3,1):.>o (0,2):o>. (3,2):.>o (12,7):b>. (12,8):.>b (11,11):b>. (11,12):.>b`
- [random s1] action `click 1 0` (first-firing clauses [7])
  - predicted: `(0,0):o>. (3,0):.>o (0,1):o>. (3,1):.>o (0,2):o>. (3,2):.>o`
  - actual: `(0,0):o>. (3,0):.>o (0,1):o>. (3,1):.>o (0,2):o>. (3,2):.>o (12,3):b>. (12,5):.>b`

### grow — wrong change — move (9 cases)

- [random s0] action `right` (first-firing clauses [])
  - predicted: `(12,0):a>. (12,1):a>. (12,2):a>.`
  - actual: `(12,0):a>. (12,1):a>. (12,2):a>. (13,7):b>. (13,8):.>b`
- [random s0] action `right` (first-firing clauses [])
  - predicted: `(12,0):a>. (12,1):a>. (12,2):a>.`
  - actual: `(12,0):a>. (12,1):a>. (12,2):a>. (14,4):b>. (14,5):.>b (12,12):b>. (12,13):.>b`
- [random s0] action `right` (first-firing clauses [])
  - predicted: `(12,0):a>. (12,1):a>. (12,2):a>.`
  - actual: `(12,0):a>. (12,1):a>. (12,2):a>. (12,5):b>. (12,6):.>b (11,9):b>. (11,10):.>b`

### ice — hallucinated change (nothing actually happens) — move (2 cases)

- [random s1] action `down` (first-firing clauses [])
  - predicted: `(4,1):.>b`
  - actual: `no change`
- [random s1] action `down` (first-firing clauses [])
  - predicted: `(4,1):.>b`
  - actual: `no change`

### ice — missed change (predicted nothing happens) — move (323 cases)

- [llm s0] action `up` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,5):l>. (4,6):.>l (3,7):l>. (3,8):.>l`
- [disagree s0] action `down` (first-firing clauses [2])
  - predicted: `no change`
  - actual: `(3,1):.>b`
- [disagree s1] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,0):a>. (5,0):.>a`

### ice — missed change (predicted nothing happens) — noop (110 cases)

- [llm s1] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(3,1):b>. (3,2):.>b`
- [disagree s1] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(6,1):l>. (6,2):.>l (4,4):l>. (4,5):.>l (4,7):l>. (4,8):.>l (3,14):l>. (3,15):.>l`
- [disagree s1] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,3):l>. (4,4):.>l (3,5):l>. (3,6):.>l`

### ice — wrong change — click (106 cases)

- [random s1] action `click 4 0` (first-firing clauses [])
  - predicted: `(0,0):a>o (1,0):a>o (0,1):a>o (1,1):a>o`
  - actual: `(0,0):a>o (1,0):a>o (0,1):a>o (1,1):a>o (3,7):l>b (4,8):l>b`
- [disagree s0] action `click 2 10` (first-firing clauses [3])
  - predicted: `(0,0):o>a (1,0):o>a (0,1):o>a (1,1):o>a`
  - actual: `(0,0):o>a (1,0):o>a (0,1):o>a (1,1):o>a (4,3):b>l (3,7):b>l`
- [random s0] action `click 4 0` (first-firing clauses [])
  - predicted: `(0,0):a>o (1,0):a>o (0,1):a>o (1,1):a>o`
  - actual: `(0,0):a>o (1,0):a>o (0,1):a>o (1,1):a>o (3,7):l>b (4,8):l>b`

### ice — wrong change — move (41 cases)

- [random s1] action `left` (first-firing clauses [])
  - predicted: `(1,0):a>. (2,0):.>a (5,0):a>. (1,1):a>.`
  - actual: `(2,0):.>a (5,0):a>.`
- [random s0] action `left` (first-firing clauses [0])
  - predicted: `(2,0):.>a (5,0):a>.`
  - actual: `(3,0):.>a (6,0):a>.`
- [random s1] action `down` (first-firing clauses [])
  - predicted: `(4,1):.>b`
  - actual: `(4,1):.>l`

### magnets — hallucinated change (nothing actually happens) — move (34 cases)

- [random s0] action `up` (first-firing clauses [])
  - predicted: `(6,7):.>b (6,9):b>.`
  - actual: `no change`
- [random s0] action `up` (first-firing clauses [])
  - predicted: `(6,7):.>b (6,9):b>.`
  - actual: `no change`
- [disagree s0] action `up` (first-firing clauses [])
  - predicted: `(6,7):.>b (6,9):b>.`
  - actual: `no change`

### magnets — missed change (predicted nothing happens) — move (8 cases)

- [llm s1] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,8):.>b (0,9):.>b`
- [random s1] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,8):.>b (0,9):.>b`
- [disagree s1] action `right` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,8):.>b (0,9):.>b`

### magnets — wrong change — move (11 cases)

- [disagree s0] action `up` (first-firing clauses [7])
  - predicted: `(5,6):.>b (5,8):b>.`
  - actual: `(6,6):.>b (5,7):b>. (6,7):.>b (5,8):b>.`
- [llm s1] action `down` (first-firing clauses [])
  - predicted: `(5,5):b>. (5,7):.>b`
  - actual: `(5,5):b>. (5,6):b>. (6,6):.>b (6,7):.>b`
- [disagree s1] action `down` (first-firing clauses [])
  - predicted: `(5,5):b>. (5,7):.>b`
  - actual: `(5,5):b>. (5,6):b>. (6,6):.>b (6,7):.>b`

### paint — missed change (predicted nothing happens) — click (6 cases)

- [random s1] action `click 13 15` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(13,15):r>g`
- [disagree s1] action `click 11 8` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(11,8):r>g`
- [random s1] action `click 10 1` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(10,1):r>g`

### wind — missed change (predicted nothing happens) — click (87 cases)

- [random s0] action `click 13 1` (first-firing clauses [5])
  - predicted: `no change`
  - actual: `(2,2):.>l (6,2):.>l (10,2):.>l (14,2):.>l`
- [disagree s0] action `click 8 1` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,5):l>. (6,5):l>. (10,5):l>. (14,5):l>. (3,6):.>l (7,6):.>l (11,6):.>l (15,6):.>l (0,10):l>. (4,10):l>. (8,10):l>. (12,10):l>. (1,11):.>l (5,11):.>l (9,11):.>l (13,11):.>l`
- [random s0] action `click 9 9` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(4,4):l>. (8,4):l>. (12,4):l>. (16,4):l>. (5,5):.>l (9,5):.>l (13,5):.>l (9,9):l>. (13,9):l>. (10,10):.>l (14,10):.>l (8,14):l>. (12,14):l>. (16,14):l>. (9,15):.>l (13,15):.>l`

### wind — missed change (predicted nothing happens) — move (327 cases)

- [llm s0] action `down` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,2):.>l (6,2):.>l (10,2):.>l (14,2):.>l (2,6):l>. (6,6):l>. (10,6):l>. (1,7):.>l (5,7):.>l (9,7):.>l (1,11):l>. (5,11):l>. (0,12):.>l (4,12):.>l (0,16):l>.`
- [llm s0] action `left` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(1,3):l>. (5,3):l>. (9,3):l>. (13,3):l>. (0,4):.>l (4,4):.>l (8,4):.>l (12,4):.>l (0,8):l>. (4,8):l>. (8,8):l>. (12,8):l>. (3,9):.>l (7,9):.>l (11,9):.>l (2,13):l>. (6,13):l>. (10,13):l>. (14,13):l>. (1,14):.>l (5,14):.>`
- [llm s1] action `down` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,2):.>l (6,2):.>l (10,2):.>l (14,2):.>l (1,6):l>. (5,6):l>. (9,6):l>. (13,6):l>. (0,7):.>l (4,7):.>l (8,7):.>l (12,7):.>l`

### wind — missed change (predicted nothing happens) — noop (100 cases)

- [disagree s1] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(0,5):l>. (4,5):l>. (8,5):l>. (12,5):l>. (3,6):.>l (7,6):.>l (11,6):.>l`
- [disagree s1] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (2,3):.>l (6,3):.>l (10,3):.>l (14,3):.>l (1,7):l>. (5,7):l>. (9,7):l>. (1,8):.>l (5,8):.>l (9,8):.>l (1,12):l>. (5,12):l>. (9,12):l>. (1,13):.>l (5,13):.>l (9,13):.>l`
- [disagree s0] action `noop` (first-firing clauses [])
  - predicted: `no change`
  - actual: `(3,5):l>. (7,5):l>. (11,5):l>. (2,6):.>l (6,6):.>l (10,6):.>l (2,10):l>. (6,10):l>. (10,10):l>. (1,11):.>l (5,11):.>l (9,11):.>l (0,15):l>. (4,15):l>. (8,15):l>. (12,15):l>. (3,16):.>l (7,16):.>l (11,16):.>l`

### wind — wrong change — click (5 cases)

- [disagree s0] action `click 10 2` (first-firing clauses [])
  - predicted: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (2,3):.>l (6,3):.>l (10,3):.>l (14,3):.>l`
  - actual: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (3,3):.>l (7,3):.>l (11,3):.>l (15,3):.>l (6,7):l>. (10,7):l>. (14,7):l>. (7,8):.>l (11,8):.>l (15,8):.>l (11,12):l>. (15,12):l>. (12,13):.>l (16,13):.>l`
- [llm s0] action `click 16 1` (first-firing clauses [])
  - predicted: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (2,3):.>l (6,3):.>l (10,3):.>l (14,3):.>l`
  - actual: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (1,3):.>l (5,3):.>l (9,3):.>l (13,3):.>l (1,7):l>. (5,7):l>. (9,7):l>. (13,7):l>. (0,8):.>l (4,8):.>l (8,8):.>l (12,8):.>l (3,12):l>. (7,12):l>. (11,12):l>. (15,12):l>. (2,13):.>`
- [disagree s0] action `click 2 2` (first-firing clauses [])
  - predicted: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (2,3):.>l (6,3):.>l (10,3):.>l (14,3):.>l`
  - actual: `(2,2):l>. (6,2):l>. (10,2):l>. (14,2):l>. (1,3):.>l (5,3):.>l (9,3):.>l (13,3):.>l`

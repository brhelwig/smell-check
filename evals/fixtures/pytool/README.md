# pytool

Sums the durations listed in a file, one per line.

```
python -m pytool.cli sample.txt
```

Durations use `h`, `m`, and `s`, as in `1h30m` or `45s`. The total prints in seconds unless
the config file sets `"unit": "minutes"`.

## Configuration

`--config` names the config file. Without it, pytool reads `./pytool.json`.

| Variable | Meaning |
| :-- | :-- |
| `PYTOOL_CONFIG` | Config file path, used when `--config` is absent |
| `PYTOOL_CACHE` | Directory for cached totals |

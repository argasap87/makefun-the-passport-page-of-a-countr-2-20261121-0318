[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/competitions/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/argasap87/makefun-the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/competitions/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/argasap87/makefun-the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/competitions/the-passport-page-of-a-countr-2-20261121-0318)

# The Passport Page of a Country That Isn't There

A make.fun entry: a Python 3.13 program that renders one uncaptioned open
passport spread for the **Maritime Sovereignty of Cinnabar Reach** — a
sulfur-mining, water-rationed archipelago that does not exist — and writes
it to `/output/entry.png` (1024×724 PNG, under 1 MiB).

## The country

Cinnabar Reach is a humid archipelago of sulfur and salt mines run by
strict atmospheric-rationing maritime guilds. Its passport belongs to
**Linnea Vance, 42, Chief Surveyor of the Guild of Surveyors**, born in
Port-Vermilion — salt-crusted, grey-eyed, monocle on a chain, brass
barometer badge on her collar. The portrait matches the place: a working
surveyor of a working archipelago, not a generic face.

## What the spread shows

- **Data page** — portrait, personal data in English and Cinnabari,
  issue 12 MAR 2024 / expiry 11 MAR 2034, and a machine-readable strip
  with real ICAO 9303 check digits.
- **Visa page** — four stamps, all after the issue date, telling one
  journey home: Qal-Hadar (arrival 19 APR 2024), Brine-Head (departure
  03 JUN 2024), High Basalt Republic (arrival 14 NOV 2024),
  Port-Vermilion (arrival 02 DEC 2024).
- **The telling detail** — a Class-3 desalination-tax stamp in yellow
  security ink: the holder is allotted **3.5 litres of atmospheric
  freshwater a day**, and unauthorised air-condensation is punishable by
  asset seizure. The country rations its own citizens' drinking water.

## Run it

```sh
python3 main.py   # writes /output/entry.png (falls back to ./output/)
```

No network. Only Pillow is needed; the portrait ships in `assets/`.

# reynard-soft7

Reynard Soft7 mascot cards. Supply **777** on Robinhood Chain (chain ID **4663**). Symbol **SOFT7**.

The first wave is 7 cards. Each week after that adds 77, and week 10 reaches 777. Ten percent of every mint accrues to staked holders. The wallet ending in `77a` receives the rest. Royalty is 7.5%.

Mint is closed. The seven paintings in `proofs/` are the approval set. Tokens 8–777 are unpainted slots in `supply/catalog.json`.

The live collection of 7 is a different contract, `0x73D7b2611509C14078e16f572bE5aC7D91879DC2`. Its site is [tigerwillca.github.io](https://tigerwillca.github.io/). This repository does not deploy or mint.

`BRIEF.md` is the source of truth.

## Check the build

```bash
bash scripts/ci.sh
```

That checks the wave cap, the stake dividend, the supply map, the proof PNG checksums, and compiles `contracts/Soft7MascotCards.sol` with solc 0.8.24.

`DEVELOPERS.md` is the contract surface, the week-by-week cap, and the failures those checks report.

Open `proofs/index.html` to see the seven proofs and the banner.

## Layout

| Path | What it is |
| --- | --- |
| `DEVELOPERS.md` | Contract surface, wave table, and local-check failures. |
| `contracts/Soft7MascotCards.sol` | 777-card contract. Proofs start unapproved. Waves start closed. |
| `supply/catalog.json` | Token 1–777. Proofs, then unpainted slots. |
| `proofs/art/` | Seven card PNGs and the banner, with SHA-256 sums. |
| `proofs/meta/` | Metadata for the seven proofs. |
| `scripts/encode_set_base_uri.py` | Prints calldata for the live supply-7 contract. It does not send it. |

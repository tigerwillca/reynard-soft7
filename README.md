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

That checks the wave cap, the stake dividend, the supply map, the proof PNG checksums, the metadata server, compiles `contracts/Soft7MascotCards.sol` with solc 0.8.24, and runs that bytecode. The run covers a closed mint, the week-10 cap of 777, the 10% stake pull, and a transfer that clears stake. Nothing is deployed.

Open `proofs/index.html` to see the seven proofs and the banner. Open `proofs/waves.html` for the week-by-week cap. Mint stays closed on that page.

```bash
bash scripts/start_metadata_server.sh
```

That serves token JSON on port 8000. `GET /1.json` is the shape `tokenURI` uses when the base ends in `/`. Tokens 1–7 are the proof files. Tokens 8–777 are shells: a name, the canon description, and `external_url`. They have no image and no traits. The server does not deploy or mint.

## Layout

| Path | What it is |
| --- | --- |
| `contracts/Soft7MascotCards.sol` | 777-card contract. Proofs start unapproved. Waves start closed. |
| `supply/catalog.json` | Token 1–777. Proofs, then unpainted slots. |
| `proofs/art/` | Seven card PNGs and the banner, with SHA-256 sums. |
| `proofs/meta/` | Metadata for the seven proofs. |
| `proofs/waves.html` | Week caps from 7 to 777. Mint stays closed. |
| `scripts/metadata_server.py` | Serves `/1.json` through `/777.json` and the proof PNGs. |
| `scripts/encode_set_base_uri.py` | Prints calldata for the live supply-7 contract. It does not send it. |

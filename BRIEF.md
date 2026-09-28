# Reynard Soft7 — one source of truth

This repository is the 777-card build. The seven proof paintings in `proofs/art/` were copied from `tigerwillca/reynard-soft7-sepolia` commit `d419dcef` (`proofs/art`). They were not redrawn. Checksums are in `proofs/art/SHA256SUMS`.

The live drop is a different contract: `0x73D7b2611509C14078e16f572bE5aC7D91879DC2` on Robinhood Chain, chain ID 4663, `MAX_SUPPLY` 7. This build does not deploy, mint, or call that contract.

Mint stays closed until the seven proofs are approved.

## What the cards are

Reynard Soft7 mascot cards on Robinhood Chain, chain ID 4663. Supply 777. Waves are 7, then 77 a week: the opening week can mint 7, and each week after that adds 77, stopping at 777. Week 10 is the week the cap reaches 777.

Description, used as written on every proof:

> reynard-soft7 mascot cards on robinhood chain. ten percent of every mint routes back to soft7 holders proportional to what they hold. stake your card, feed the treasury, pull when you're ready.

Socials: [discord.gg/tigerwillca](https://discord.gg/tigerwillca), [x.com/tigerwillca](https://x.com/tigerwillca), [tigerwillca.github.io](https://tigerwillca.github.io/).

Traits, five and no others: `tier`, `color`, `eyes`, `signature`, `globe`.

Tokens 1–7 carry the proof traits. Tokens 8–777 are unpainted slots in `supply/catalog.json`. They have no name, image, or traits yet.

## Paint, eyes, amulet, clothing

Art is paintbrush, with bristle and canvas.

Every character comes off the mascot. Face paint is on all of them. No two of the seven proofs share a signature. The seven signatures, from the base mask to the most complex, are Brow Line, Cheek Marks, Solar Tick, Heart Band, Throat Outline, Layered Contour, Crown Glyphs.

The eyes are the identity. They stay fixed. Fox cards keep Amber Lock. Proofs 1, 4, and 5 are the fox cards. Proof 3 is the lean tiger: Pale Lock eyes, one gold brow tick, gold only as the faint amulet.

The potion is the engine. Color arrives in this order: the amulet catches the chakra color first, then the mask paint blooms, then the belt buckle. On a still proof, the tier shows how far that bloom has gone.

Colors differ on every proof tier: Crimson, Amber, Gold, Green, Blue, Indigo, Violet.

The banner is a purple-lime backdrop, Reynard as the hero, and the seventh-gate potion orb. The banner proof clips the fox at the shins. The seven card PNGs are the token media.

## Media

One image per token. PNG or GIF. The proof files are real PNGs (`89 50 4E 47`). Image fields in this repository are paths under `proofs/art/`. They are not a jsDelivr pin yet.

## Money

Ten percent of every mint accrues to staked holders in proportion to how many cards they have staked. The card stays in the wallet while it is staked. The holder pulls when they are ready.

The Robinhood wallet ending in 77a is `0xe53bdb2118585d5B2cD06a117d3A036AFA70677a`. It receives the other ninety percent of each mint. If nobody is staked when a mint happens, the ten percent is paid there too.

Royalty is 7.5% (750 bps), paid to that same wallet on secondary sales.

Integer division can leave dust in the stake accumulator. That dust is not pulled.

Compile the proof contract with solc 0.8.24, optimizer on, 200 runs, EVM `cancun`, metadata bytecode hash, viaIR off. `scripts/compile_proof.sh` writes `contracts/compiler-input.json`.

The proof contract starts with proofs unapproved and waves closed. `approveProofs()` then `openWaves()` are owner calls for after this set is accepted. They have not been sent. No deploy. No mint.

## What not to do from this repository

- Do not redraw the seven proofs or the banner.
- Do not invent traits or images for tokens 8–777.
- Do not deploy `Soft7MascotCards` or mint it.
- Do not send `setBaseURI` to the live supply-7 contract. `scripts/encode_set_base_uri.py` only prints calldata.

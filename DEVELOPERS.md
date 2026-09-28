# Developers

Product rules live in `BRIEF.md`. This page is the contract surface in `contracts/Soft7MascotCards.sol`, the supply map, and the checks in `scripts/ci.sh`.

Nothing here deploys or mints. `approveProofs()` and `openWaves()` are owner calls for after the seven proofs are accepted. They have not been sent.

## Setup

`bash scripts/ci.sh` is the whole check. It needs `bash`, `python3`, and `git`. `curl` is used only when `.tools/solc-0.8.24` is not already executable.

`scripts/compile_proof.sh` uses `SOLC` when that variable points at an executable. Otherwise it downloads the linux-amd64 binary `solc-0.8.24+commit.e11b9ed9` into `.tools/` (gitignored) and compiles with it. Settings written to `contracts/compiler-input.json`:

- optimizer on, 200 runs
- `evmVersion` `cancun`
- metadata `bytecodeHash` `ipfs`
- viaIR omitted. `BRIEF.md` requires it off, and this input does not turn it on
- output: abi, bytecode, deployed bytecode, metadata, and the AST

`.github/workflows/build.yml` runs `bash scripts/ci.sh` on every push and pull request, with Python 3.12.

Bytecode and compiler output land in `contracts/out/`, which is gitignored. The compiler input is committed. `ci.sh` finishes with `git diff --exit-code -- contracts/compiler-input.json`, so a source edit that changes the input fails the check until that file is regenerated and committed.

## What the check runs

| Step | Proves |
| --- | --- |
| `python3 scripts/check_waves.py` | Week caps, and the 10% dividend split by stake count. |
| `python3 scripts/check_contract.py` | Name, symbol, supply, wave, royalty, payout, chain id 4663, and the proof gate are present in the Solidity source. |
| `python3 scripts/supply.py --check` | Catalog, proof metadata, collection file, proof page, and PNG checksums match the generator. |
| inline `encode()` check | `setBaseURI(string)` calldata starts with `0x55f804b3` and is only printed. |
| `bash scripts/compile_proof.sh` | The pinned solc accepts the contract. |

`python3 scripts/supply.py --write` regenerates `supply/catalog.json`, `proofs/meta/1.json` through `7.json`, `proofs/collection.json`, and `proofs/index.html` from `scripts/supply.py`. Hand-editing those outputs fails `--check`.

```bash
python3 scripts/encode_set_base_uri.py 'https://example.com/meta/'
```

The script prints `to` and `data` for the live supply-7 contract `0x73D7b2611509C14078e16f572bE5aC7D91879DC2`. The base must end in `/`. It does not broadcast. `BRIEF.md` says not to send that calldata from this repository. The 777-card contract is a different source file and is not deployed.

## Wave cap

`waveCap()` returns 0 until `openWaves()` sets `opening` to `uint64(block.timestamp)`. After that, week index is `(block.timestamp - opening) / 7 days`. Week 0 allows 7 tokens. Each later week adds 77, and the cap stops at 777. `check_waves.py` locks this table:

| Weeks since `openWaves` | `waveCap()` | Token ids the catalog assigns to that week |
| --- | --- | --- |
| 0 | 7 | 1–7 |
| 1 | 84 | 8–84 |
| 2 | 161 | 85–161 |
| 3 | 238 | 162–238 |
| 4 | 315 | 239–315 |
| 5 | 392 | 316–392 |
| 6 | 469 | 393–469 |
| 7 | 546 | 470–546 |
| 8 | 623 | 547–623 |
| 9 | 700 | 624–700 |
| 10 and later | 777 | 701–777 |

`mint` allows the next id while `totalSupply < waveCap()`. Ids start at 1 and increment by one. A week raises that total. It does not skip ahead to a later id. The catalog's `wave` field comes from `token_wave()` in `scripts/supply.py`, which is a function of the id. Token 8 stays wave 1 in the catalog even if it is minted after week 1.

## Contract surface

Constructor argument `baseURI_` must be non-empty and end in `/` (`BadBase`). The deployer becomes `owner`. `mintPrice` starts at 0. `proofsApproved` starts false. `opening` starts at 0. `_base` is private. `tokenURI` is the read path, and it reverts `Nonexistent` until that id is minted. The URI is the base, the decimal id, and `.json` (token 1 is `1.json`, with no zero padding).

Owner calls:

| Function | Behavior |
| --- | --- |
| `approveProofs()` | Sets `proofsApproved`. A second call keeps it true and emits `ProofsApproved` again. |
| `openWaves()` | Requires `proofsApproved` (`ProofsPending`). Requires `opening == 0` (`AlreadyOpen`). Stores the current timestamp. |
| `setMintPrice(uint256)` | Stores the exact wei `mint` will require. Can be called before or after the waves open. |
| `setBaseURI(string)` | Same trailing-slash rule as the constructor. Emits `BaseURISet` and `BatchMetadataUpdate(1, 777)`. |
| `transferOwnership(address)` | Rejects the zero address (`ZeroAddress`). |

`mint()` is `payable` and returns the new id. It reverts unless all of these hold:

- `block.chainid` is 4663 (`WrongChain`)
- proofs are approved and `opening` is non-zero (`ProofsPending`)
- `msg.value` equals `mintPrice` (`WrongPrice`)
- `totalSupply` is still below `waveCap()` (`WaveFull`)

Leaving `mintPrice` at 0 means a mint must send 0 wei. A price of 1 through 9 wei has a zero dividend (`msg.value / 10`), so the whole payment goes to `PAYOUT` in that transaction.

`PAYOUT` is fixed at `0xe53bdb2118585d5B2cD06a117d3A036AFA70677a`.

## Stake accounting

Stake is a claim weight. The card stays in the holder's wallet. `stake` and `unstake` require `msg.sender` to be the recorded holder (`NotTokenOwner`, `AlreadyStaked`, `NotStaked`). An operator approval allows `transferFrom`. Transfer of a staked token settles the sender, clears that stake, then moves the card. The receiver's stake count is unchanged. Accrued wei stay with the previous holder until they `pull`.

On a mint, `dividend = msg.value / 10`.

- When `totalStaked` is 0, a non-zero dividend is paid to `PAYOUT` immediately, and `msg.value - dividend` is paid to `PAYOUT` after that. A zero dividend skips the first payment.
- When `totalStaked` is non-zero and `dividend` is non-zero, `PAYOUT` is paid `msg.value - dividend` immediately and the dividend stays in the contract. The contract adds `(dividend * 1e18) / totalStaked` to `accPerStake`. Holders withdraw with `pull()`. `pending(address)` is the view of accrued plus unsettled gain.

Weight is `stakedCount`, the number of tokens that address has staked. Integer division can credit less than the retained dividend. `check_waves.py` shows the case: three stakers and a 10 ether mint credit `1 ether / 3` each, and `3 * (1 ether / 3)` is less than 1 ether. The remainder stays in the contract. No function sweeps it. `pull` settles, zeroes `accrued`, then sends. A zero balance skips the call and still emits `Pulled` with amount 0.

A recipient that rejects ether makes the payment revert `PayFailed`, which reverts the mint or the pull.

## Catalog

`supply/catalog.json` is one object: collection fields, then `tokens` length 777. `mint` in the file is the string `"closed"`.

Tokens 1–7 are `status: "proof"`, `wave: 0`, with `name`, `description`, `image` (`proofs/art/01.png` through `07.png`), and these traits only: `tier`, `color`, `eyes`, `signature`, `globe`. Traits on the proofs:

| Id | Color | Eyes | Signature | Globe | `mascot` |
| --- | --- | --- | --- | --- | --- |
| 1 | Crimson | Amber Lock | Brow Line | Root Stone | `fox` |
| 2 | Amber | Coal Lock | Cheek Marks | Sacral Clay | omitted |
| 3 | Gold | Pale Lock | Solar Tick | Solar Dust | `tiger` |
| 4 | Green | Amber Lock | Heart Band | Heart Moss | `fox` |
| 5 | Blue | Amber Lock | Throat Outline | Throat Tide | `fox` |
| 6 | Indigo | Ink Lock | Layered Contour | Brow Night | omitted |
| 7 | Violet | Band Lock | Crown Glyphs | Crown Gate | omitted |

Tokens 8–777 are `{ "id", "wave", "status": "unpainted" }`. The generator rejects `name`, `image`, or `attributes` on those ids.

`proofs/meta/{id}.json` repeats the proof name, the canon description, the repo-relative image path, `external_url` `https://tigerwillca.github.io/`, and the five traits. `tokenURI` for a minted id is `{base}{id}.json` on the base stored in the contract.

`proofs/collection.json` carries royalty 750 and the same payout address. `proofs/art/SHA256SUMS` covers `01.png` through `07.png` and `banner.png`. Each file must start with the PNG signature `89 50 4E 47`.

## Interfaces

`supportsInterface` returns true for these ids:

| Id | Interface |
| --- | --- |
| `0x01ffc9a7` | ERC-165 |
| `0x80ac58cd` | ERC-721 |
| `0x5b5e139f` | ERC-721 metadata |
| `0x2a55205a` | ERC-2981 royalty |
| `0x49064906` | ERC-4906 metadata update |

`royaltyInfo` ignores the token id. The receiver is `PAYOUT`. The amount is `salePrice * 750 / 10000`.

`safeTransferFrom` to a contract reverts `UnsafeReceiver` unless `onERC721Received` returns its selector. The contract has no burn function and no token-by-index enumeration.

## Custom errors

| Error | When |
| --- | --- |
| `NotOwner` | Caller is not `owner`. |
| `ProofsPending` | `openWaves` before approval, or `mint` before approval and open. |
| `AlreadyOpen` | Second `openWaves`. |
| `WaveFull` | `totalSupply` has reached `waveCap()`. |
| `WrongPrice` | `msg.value` is not `mintPrice`. |
| `WrongChain` | Chain id is not 4663. |
| `BadBase` | Base URI empty or missing a trailing `/`. |
| `ZeroAddress` | `balanceOf(address(0))`, `transferOwnership`, `setApprovalForAll`, or `transferFrom` to the zero address. |
| `NotTokenOwner` | Stake or transfer `from` is not the holder. |
| `AlreadyStaked` | That token id is already staked. |
| `NotStaked` | `unstake` caller is not `stakedBy[tokenId]`. |
| `Nonexistent` | `ownerOf`, `tokenURI`, `approve`, or `getApproved` for an unminted id. |
| `Unauthorized` | Transfer or approve without being holder, approved address, or operator. |
| `UnsafeReceiver` | Safe transfer receiver rejected the token. |
| `PayFailed` | Payout or `pull` recipient rejected the ether. |

## When a check fails

| Failure | What to fix |
| --- | --- |
| `git diff` on `contracts/compiler-input.json` | The Solidity source and the committed compiler input diverged. `bash scripts/compile_proof.sh` rewrites the input. Commit that file only when the source change is intentional. |
| `solc` download or exec format error | The script fetches a linux-amd64 binary. Point `SOLC` at a local 0.8.24+commit.e11b9ed9 binary and rerun. |
| `base URI must end with /` | `encode_set_base_uri.py` rejects a base with no trailing slash. The contract reverts `BadBase` for the same shape. |
| `supply/catalog.json does not match the generator` or `token N has invented art fields` | Regenerate with `python3 scripts/supply.py --write`, or put the file back. Tokens 8–777 stay unpainted. |
| PNG `sha256` or `is not a PNG` | `proofs/art/SHA256SUMS` is the approval set copied from `reynard-soft7-sepolia` commit `d419dcef`. Restore the file. Do not redraw it. |
| `missing MAX_SUPPLY = 777` (or a sibling constant) | `check_contract.py` matches the source text against the brief. Constants and `block.chainid != 4663` stay as written. |

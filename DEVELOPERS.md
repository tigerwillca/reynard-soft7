# Developers

Product rules live in `BRIEF.md`. This page is the 2026-09-30 acceptance of the seven proofs, and the mint gate in `contracts/Soft7MascotCards.sol` that acceptance leaves closed.

Nothing here deploys, mints, or sends `approveProofs()` or `openWaves()`. The live supply-7 contract `0x73D7b2611509C14078e16f572bE5aC7D91879DC2` is a different bytecode. `scripts/encode_set_base_uri.py` only prints calldata for that contract.

## Two records

The catalog and the proof page store the acceptance. A fresh deployment of this contract still has the mint gate shut.

| Record | Where | Value in this tree |
| --- | --- | --- |
| `proofs` | `supply/catalog.json`, from `catalog()` in `scripts/supply.py` | `"approved"` |
| `accepted` | same object | `"2026-09-30"` |
| `mint` | same object | `"closed"` |
| Proof page | `proofs/index.html`, from `render_page()` | `These proofs were accepted on 2026-09-30. Mint stays closed.` |
| `proofsApproved` | public `bool` on `Soft7MascotCards` | `false` until the owner calls `approveProofs()` |
| `opening` | public `uint64` | `0` until the owner calls `openWaves()` |
| `waveCap()` | view | `0` while `opening` is `0` |

`proofs/collection.json` carries the name, the canon description, royalty `750`, and the payout address. It has no `proofs` or `accepted` field. Tokens 1–7 stay `status: "proof"` with the five traits in `LOCKED`. Tokens 8–777 stay `{ "id", "wave", "status": "unpainted" }`.

The contract NatSpec still says mint stays closed until the owner marks the proofs approved and then opens the waves. That sentence describes `approveProofs()` and `openWaves()`. Writing the catalog date leaves the Solidity as it is.

## Owner calls that follow acceptance

Both calls are `onlyOwner`. The deployer is `owner`. Any other caller reverts `NotOwner`.

`approveProofs()` assigns `proofsApproved = true` and emits `ProofsApproved`. The body has no second-call guard, so a later call assigns true again and emits again.

`openWaves()` reverts `ProofsPending` while `proofsApproved` is false. It reverts `AlreadyOpen` when `opening` is already non-zero. The successful call stores `uint64(block.timestamp)` and emits `WavesOpened(opening)`.

`mint()` reverts `ProofsPending` unless `proofsApproved` is true and `opening` is non-zero. `approveProofs()` by itself leaves `waveCap()` at 0, so a mint still reverts. After `openWaves()`, week 0 allows 7 tokens. The mint also requires chain id 4663 (`WrongChain`) and `msg.value == mintPrice` (`WrongPrice`).

No file under `scripts/` broadcasts these calls. `test/Soft7MascotCards.t.sol` constructs the contract in-process. `setUp` deploys with base `https://example.com/meta/`, sets `mintPrice` to 10 ether, and sets chain id 4663. It leaves `proofsApproved` false and `opening` at 0.

| Test | What it locks |
| --- | --- |
| `test_waveCapStaysShutUntilWavesOpen` | `waveCap()` is 0, `proofsApproved()` is false, `opening()` is 0. |
| `test_mintRevertsUntilProofsAreApprovedAndWavesOpen` | `mint` reverts `ProofsPending` before `approveProofs`, and again after that call until `openWaves`. |
| `test_strangerCannotApproveOrOpen` | A non-owner reverts `NotOwner` on both calls. |
| `test_openWavesRequiresProofsAndOpensOnce` | `openWaves` before approval reverts `ProofsPending`. A second open reverts `AlreadyOpen`. |

Sixteen further tests call `_open()` before they mint. `test_baseMustEndInSlash` and `test_ownerCanHandOffThePriceAndTheRole` do not. The file declares 22 tests. `_open()` calls `approveProofs()` and then `openWaves()` on that in-process instance. It does not deploy and it does not send a transaction.

## What the check runs

`bash scripts/ci.sh` runs `python3 scripts/supply.py --check` after `scripts/check_waves.py` and `scripts/check_contract.py`, and before the compiler and `forge test`.

`check_contract.py` requires the source text to contain `proofsApproved` and `openWaves`. It prints `PASSED: Soft7MascotCards constants match the brief`. It does not read `supply/catalog.json`, so a catalog of `"approved"` still leaves a fresh deployment with `proofsApproved == false`.

A clean supply check prints:

```text
PASSED: 777 slots, 7 proofs, 770 unpainted, week 10 closes the supply
```

That line does not mention the date. The date is locked by the failures below. `check_outputs()` compares the files to the generator, then applies three acceptance checks:

| Condition | Failure printed as `FAIL …` |
| --- | --- |
| `catalog()` has `proofs` other than `"approved"`, or `accepted` other than `"2026-09-30"` | `the seven proofs must stay accepted on 2026-09-30` |
| `catalog()` has `mint` other than `"closed"` | `mint must stay closed` |
| `proofs/index.html` lacks `accepted on 2026-09-30` or `Mint stays closed` | `proof page must record the acceptance and keep mint closed` |
| `supply/catalog.json` differs from `catalog()` | `supply/catalog.json does not match the generator` |
| `proofs/index.html` differs from `render_page()` | `proofs/index.html does not match the generator` |

The catalog date check calls `catalog()` in `scripts/supply.py`. The page phrase check reads the file on disk. The generator and the page both have to keep 2026-09-30.

```bash
python3 scripts/supply.py --check
python3 scripts/supply.py --write
```

`--write` rewrites `supply/catalog.json`, `proofs/collection.json`, `proofs/meta/1.json` through `7.json`, and `proofs/index.html` from the generator. The generator hardcodes `"proofs": "approved"` and `"accepted": "2026-09-30"`. `--write` copies those fields. It does not call the contract.

## Constraints

- Hand-editing `proofs` or `accepted` in `supply/catalog.json` fails with `supply/catalog.json does not match the generator`. The explicit date failure fires when `catalog()` itself changes, because that check reads the function, not the file.
- Hand-editing the acceptance sentence in `proofs/index.html` fails the generator match. Removing `accepted on 2026-09-30` or `Mint stays closed` from the file also fails the phrase check.
- `proofs/art/SHA256SUMS` is still the copied approval set. Acceptance does not replace those digests.
- On this bytecode, `pull()` copies `accrued[msg.sender]`, sets that entry to 0, then pays the copied amount. A zero amount skips the call and still emits `Pulled` with amount 0. A recipient that rejects ether reverts `PayFailed`, which reverts the zeroing with it. `scripts/check_waves.py` zeroes its mirrored accrued amount the same way. This `pull` pays the stored amount with no balance cap, and this suite has no test that caps a short payment.

## When a check fails

| Failure | What to fix |
| --- | --- |
| `the seven proofs must stay accepted on 2026-09-30` | Put `"proofs": "approved"` and `"accepted": "2026-09-30"` back in `catalog()`, then `python3 scripts/supply.py --write`. |
| `mint must stay closed` | Keep `"mint": "closed"` in `catalog()`, then `--write` so the JSON matches. |
| `proof page must record the acceptance and keep mint closed` | Keep both phrases in `render_page()`. `--write` refreshes `proofs/index.html`. |
| `supply/catalog.json does not match the generator` or `proofs/index.html does not match the generator` | Regenerate with `--write`, or restore the file. The acceptance fields are owned by `scripts/supply.py`. |
| `proof gate is missing` | `scripts/check_contract.py` wants the identifiers `proofsApproved` and `openWaves` in `contracts/Soft7MascotCards.sol`. |
| `test_mintRevertsUntilProofsAreApprovedAndWavesOpen` | `mint` must revert `ProofsPending` until both `approveProofs()` and `openWaves()` have run on that instance. A catalog of `"approved"` does not satisfy this test. |

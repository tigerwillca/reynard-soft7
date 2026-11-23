# Developers

This branch is the 16 Nov 2026 read of the live supply-7 collection and the unpainted metadata for the next 77 token ids. There is no contract source, no landing page, and no generator script. `reports/2026-11-16-onchain-status.md` is the chain snapshot. `metadata/wave-02/` is the file set that snapshot refreshed.

As of 23 Nov 2026, commit `9df7a94` (16 Nov 2026) is still the newest commit in the repository.

## Files

| Path | What it is |
| --- | --- |
| `reports/2026-11-16-onchain-status.md` | Read at Robinhood Chain block 115,888,313 (2026-11-16 16:05 UTC), chain ID 4663. |
| `metadata/wave-02/manifest.json` | Bounds, mint lock, and the block the shells were refreshed against. |
| `metadata/wave-02/8.json`–`84.json` | One shell per token id. 77 files. Ids 0–7 and 85 onward are absent. |

The live collection is `0x73D7b2611509C14078e16f572bE5aC7D91879DC2` (Reynard Soft7, SOFT7). The report records verified source `SoftReynard7RH`, solc 0.8.24, verified 8 Oct 2026. A simulated `mintSoft7` from the owner reverts with `MaxSupply()`. `MAX_SUPPLY` is 7. The 777-card contract is not deployed.

## Shells

Every file from `8.json` through `84.json` is the same document, with the id in the name. Keys are `name`, `description`, `external_url`, in that order, two-space indent, and a trailing newline. `image` and `attributes` are absent. `manifest.json` lists those two keys under `missing`.

```json
{
  "name": "Reynard Soft7 #8",
  "description": "reynard-soft7 mascot cards on robinhood chain. ten percent of every mint routes back to soft7 holders proportional to what they hold. stake your card, feed the treasury, pull when you're ready.",
  "external_url": "https://tigerwillca.github.io/"
}
```

`84.json` changes only the name, to `Reynard Soft7 #84`. The description is the same 77 times. That lowercase mint sentence is the shell copy. The live pin, in the next section, serves a different description for tokens 1–7.

The 77 shell bodies on this commit match the 9 Nov tree byte for byte, including each `name`. The 16 Nov commit does not repaint them.

## Manifest

| Field | Value on this read | Use |
| --- | --- | --- |
| `wave` | `2` | The directory is `metadata/wave-02/`. |
| `weekIndex` | `1` | The status report calls ids 8–84 week index 1. |
| `tokenIdFrom` / `tokenIdTo` | `8` / `84` | Inclusive. `count` is 77. |
| `chainId` | `4663` | Robinhood Chain. |
| `mint` | `"closed"` | |
| `deploy` | `false` | Leave this false. This folder is not a base URI. |
| `prepared` | `"2026-11-16"` | Date this manifest was stamped. |
| `liveContract` | `0x73D7b2611509C14078e16f572bE5aC7D91879DC2` | The supply-7 contract. |
| `liveMaxSupply` | `7` | |
| `observedBlock` | `115888313` | Same block as the status report. |
| `missing` | `image`, `attributes` | Left out of every shell on purpose. |

The manifest note is the working rule: shells only, images and the five card traits stay unpainted, do not mint, and do not point the live supply-7 contract at this folder. This branch names the five traits only as missing. It does not list their names.

`wave` is 2 and `weekIndex` is 1 on the same object. The directory name follows `wave`. The status report's "week index 1" follows `weekIndex`. The token range is 8–84 in both fields. Keep both numbers when you edit the manifest.

## Live pin

The 16 Nov report records this `tokenURI` pattern, and a fetch of the pin on 23 Nov 2026 still returned it for tokens 1–7:

`https://cdn.jsdelivr.net/gh/tigerwillca/reynard-soft7-sepolia@bc36925184867284c4b82bb47ded26b802aae1b6/meta/{id}.json`

Tokens 1–7 returned 200. Token 8 returned 404, body `Couldn't find the requested file /meta/8.json in tigerwillca/reynard-soft7-sepolia.` Token 1 on that pin:

```json
{
  "name": "Reynard Soft7 #1 (Art 033)",
  "description": "Reynard Soft7 on Robinhood Chain mainnet. SoftReynard7 card from The Seventh Gate. Art slot 033. Supply 7. Secondary sales pay a 7.5% creator fee; 1.5% of the sale price is paid quarterly on-chain to holders of Soft7 tokens 1-7.",
  "image": "https://cdn.jsdelivr.net/gh/tigerwillca/reynard-soft7-sepolia@ae7d304699989b945bfe8c0f4225f3a7fc952f83/images/033.jpg",
  "external_url": "https://tigerwillca.github.io/",
  "attributes": [
    { "trait_type": "Art Slot", "value": "033" },
    { "trait_type": "Species", "value": "Tiger" },
    { "trait_type": "Network", "value": "Robinhood Chain" },
    { "trait_type": "Chain ID", "value": "4663" },
    { "trait_type": "Drop", "value": "Soft7" }
  ]
}
```

Art slots on the pin are 033–039 for tokens 1–7. Species is Tiger for 1, 3, 5, and 7, and Fox / Reynard for 2, 4, and 6. Each `image` is a jpg on commit `ae7d304699989b945bfe8c0f4225f3a7fc952f83`, a separate pin from the metadata commit. `external_url` is the field the shells share with that document.

```bash
curl -sS -o /dev/null -w '%{http_code}\n' \
  https://cdn.jsdelivr.net/gh/tigerwillca/reynard-soft7-sepolia@bc36925184867284c4b82bb47ded26b802aae1b6/meta/1.json
curl -sS -o /dev/null -w '%{http_code}\n' \
  https://cdn.jsdelivr.net/gh/tigerwillca/reynard-soft7-sepolia@bc36925184867284c4b82bb47ded26b802aae1b6/meta/8.json
```

A base URI pointed at `metadata/wave-02/` would publish shells for 8–84 and would have no file for tokens 1–7. `deploy` stays `false`.

The 23 Nov check was the jsDelivr pin only. Holder and transaction figures below are the 16 Nov report, at block 115,888,313. They were not re-read on 23 Nov.

## What the 16 Nov refresh changed

Against the 9 Nov tree, the 77 shell bodies are unchanged. The 16 Nov commit stamps `prepared` to `2026-11-16` and `observedBlock` to `115888313`, and replaces `reports/2026-11-09-onchain-status.md` with `reports/2026-11-16-onchain-status.md`.

The report text moves the comparison point from the 2 Nov read (block 104,343,971) to the 9 Nov read (block 110,185,332). Supply, holders, royalty, and the transaction list are the same sentences otherwise.

Sentences the 16 Nov report keeps from the 9 Nov report:

- Verified source is `SoftReynard7RH`, solc 0.8.24, verified 8 Oct 2026. The 777-card contract is not deployed.
- A simulated `mintSoft7` from the owner reverts with `MaxSupply()`.
- The token 2 wallet's code is empty. On 2 Nov that wallet was delegated to EIP7702StatelessDeleGator `0x63c0c19a282a1B52b07dD5a65b58948A07DAE32B`. Token 2 has not moved. The report's RPC does not serve state at block 110,185,332, so the block that cleared the delegation is not in the report. The report places that change outside the Soft7 contract.

A separate weekly note the same afternoon, on branch `cursor/soft7-weekly-status-report-d4a7`, used block 115,886,769 (16:03 UTC) and compared with the 9 Nov weekly note at block 110,181,922. That note is not in this tree. It records the same supply of 7, the same six holders, and the same newest call. It also names the giveback vault `0x6B0E22d322c967DFBDB57D027cE53D1D32F7711A`, which this status report does not.

## Snapshot the report locks

| | |
| --- | --- |
| Minted / `MAX_SUPPLY` | 7 / 7 |
| Owner | `0xe53bdb2118585d5B2cD06a117d3A036AFA70677a` |
| Royalty | 750 bps to `0x64c00a1c2d354F66aD5660548098F7cA25CEeb38` |
| `royaltyInfo` of 1 ETH | 0.075 ETH |
| Royalty receiver balance | 0 ETH |
| `ownerOf` 1–7 | succeeds |
| `ownerOf` 0 and 8 | revert |
| Last contract call | `setBaseURI`, 30 Sep 2026 19:44 UTC, block 76,775,848 |
| Transactions | 14, all successful. Logs since block 110,185,332 are empty. |

The owner is an EIP-7702 account delegated to SemiModularAccount7702 `0x77021100bD87b7008E5E1989d0eB38555d0d0000`. The owner holds no cards. The deployer holds none.

| Holder | Cards | Count |
| --- | --- | --- |
| `0x7c440909184FF4b45d96175ecCCdE4BD21901ab1` | 1, 7 | 2 |
| `0xd84E69Fa5a0975da11eDc9a9721CF893f7784BC6` | 2 | 1 |
| `0x49C1408183749BE16D3373a001FfB217B8e599d6` | 3 | 1 |
| `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` (vitalik.eth) | 4 | 1 |
| `0x8D00caE604984076a09218B854686549663Fb427` | 5 | 1 |
| `0x76443F52feb3561aaA71A01300602eB0b052bd45` | 6 | 1 |

The two-card wallet is delegated to the same SemiModularAccount7702. `balanceOf` across the six wallets sums to 7. No transfer since the deployer sent the cards out on 25 Sep 2026.

## When the counts disagree

| What you see | What the 16 Nov report recorded |
| --- | --- |
| Blockscout token counter says 10 holders | The holder list has no next page and names the six wallets above. `ownerOf` matches that list. |
| Blockscout address counter says 13 transactions | The transaction list is complete (`next_page_params` empty) at 14. The address counter leaves out the creation transaction. None reverted. None of the three internal calls failed. |
| Token 2 looks like an ordinary account | Its code is empty on this read. The 2 Nov report had it delegated to EIP7702StatelessDeleGator `0x63c0c19a282a1B52b07dD5a65b58948A07DAE32B`. The card did not move. |
| A shell contains `image` or `attributes` | `missing` names those keys. The 77 bodies on this commit leave them out. |
| `wave` is 2 while `weekIndex` is 1 | Both are stored. Directory `wave-02` follows `wave`. The report's week index follows `weekIndex`. The id range is 8–84 either way. |
| The pin description mentions a 7.5% creator fee | That sentence is on the painted pin for tokens 1–7. The shells in this folder use the lowercase mint sentence and have no `image`. |

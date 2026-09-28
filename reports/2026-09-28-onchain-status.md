# Soft7 status — 28 Sep 2026

Read at Robinhood Chain block **74,933,922** (2026-09-28 16:16 UTC), chain ID **4663**.

The live collection is `0x73D7b2611509C14078e16f572bE5aC7D91879DC2` (Reynard Soft7, SOFT7). It is not the 777-card contract. That contract is not deployed. This one is capped at 7 and cannot mint the next wave.

## Supply

| | |
| --- | --- |
| Minted | 7 |
| `MAX_SUPPLY` | 7 |
| Contract owner | `0x86dF4D2fAA9aC25D408AA4E4Fb890B9918c5f066` |
| Token URI | `https://cdn.jsdelivr.net/gh/tigerwillca/reynard-soft7-sepolia@3a049e2b1635d41066efa0a6f9990548baf57e40/meta/{id}.json` |
| Royalty | 750 bps (7.5%) to `0x64c00a1c2d354F66aD5660548098F7cA25CEeb38` |

Tokens 1–7 are Art slots 033–039. Each metadata file names the species Fox / Reynard.

## Holders

Six wallets hold the seven cards. The deployer no longer holds any.

| Holder | Cards | Count |
| --- | --- | --- |
| `0x7c440909184FF4b45d96175ecCCdE4BD21901ab1` | 1, 7 | 2 |
| `0xd84E69Fa5a0975da11eDc9a9721CF893f7784BC6` | 2 | 1 |
| `0x49C1408183749BE16D3373a001FfB217B8e599d6` | 3 | 1 |
| `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` (vitalik.eth) | 4 | 1 |
| `0x8D00caE604984076a09218B854686549663Fb427` | 5 | 1 |
| `0x76443F52feb3561aaA71A01300602eB0b052bd45` | 6 | 1 |

The two-card wallet is an EIP-7702 account. No transfers have happened since the deployer sent the cards out on 25 Sep 2026.

## Transactions

Blockscout returns the full history for this contract (`next_page_params` is empty): **12 transactions, all successful**. None reverted, and none report an internal-transaction error.

All twelve were sent by the deployer on 25 Sep 2026:

1. **09:19:36** — deployed the contract (`0xb923feac…`).
2. **09:19:37** — minted tokens 1–7 to the deployer (`0x4ec2e2d3…`).
3. **09:31–11:59** — `safeTransferFrom` of tokens 1 through 7 to the holders above.
4. **09:33:26** — set the base URI to the jsDelivr `meta/` pin above (`0xfbd4dc47…`).
5. **10:41:55** — pointed the royalty receiver at `0xe53bdb2118585d5B2cD06a117d3A036AFA70677a` (`0xd776ce3f…`).
6. **11:08:32** — moved the royalty receiver to `0x64c00a1c2d354F66aD5660548098F7cA25CEeb38` (`0x18075383…`). That is the receiver `royaltyInfo` returns now.

## Next 77

The week after the opening 7 adds 77 cards: token ids **8–84**. Shells for that wave are in `metadata/wave-02/`. They have the collection description and an external URL, and they do not invent images or the five card traits. Mint stays closed. These files are not a base URI for the live supply-7 contract.

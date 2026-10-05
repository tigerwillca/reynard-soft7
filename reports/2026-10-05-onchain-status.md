# Soft7 status — 5 Oct 2026

Read at Robinhood Chain block **80,916,059** (2026-10-05 16:10 UTC), chain ID **4663**.

The live collection is `0x73D7b2611509C14078e16f572bE5aC7D91879DC2` (Reynard Soft7, SOFT7). The 777-card contract is not deployed. This one is capped at 7 and cannot mint the next wave.

## Supply

| | |
| --- | --- |
| Minted | 7 |
| `MAX_SUPPLY` | 7 |
| Contract owner | `0xe53bdb2118585d5B2cD06a117d3A036AFA70677a` |
| Token URI | `https://cdn.jsdelivr.net/gh/tigerwillca/reynard-soft7-sepolia@bc36925184867284c4b82bb47ded26b802aae1b6/meta/{id}.json` |
| Royalty | 750 bps (7.5%) to `0x64c00a1c2d354F66aD5660548098F7cA25CEeb38` |

`ownerOf` for tokens 1–7 succeeds. Token 0 and token 8 revert. No mint since the opening mint on 25 Sep 2026.

Since the 28 Sep report the deployer transferred ownership, and the new owner set the base URI above. Both calls succeeded. Tokens 1–7 still resolve. They are Art slots 033–039. Species on the new pin is Tiger for 1, 3, 5, and 7, and Fox / Reynard for 2, 4, and 6.

The royalty receiver holds 0 ETH. `royaltyInfo` for a 1 ETH sale returns 0.075 ETH.

## Holders

Six wallets hold the seven cards. The deployer holds none.

| Holder | Cards | Count |
| --- | --- | --- |
| `0x7c440909184FF4b45d96175ecCCdE4BD21901ab1` | 1, 7 | 2 |
| `0xd84E69Fa5a0975da11eDc9a9721CF893f7784BC6` | 2 | 1 |
| `0x49C1408183749BE16D3373a001FfB217B8e599d6` | 3 | 1 |
| `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` (vitalik.eth) | 4 | 1 |
| `0x8D00caE604984076a09218B854686549663Fb427` | 5 | 1 |
| `0x76443F52feb3561aaA71A01300602eB0b052bd45` | 6 | 1 |

The two-card wallet is an EIP-7702 account. That wallet holds 2 of 7. Each of the other five holds 1 of 7. No transfers since the deployer sent the cards out on 25 Sep 2026.

## Transactions

Blockscout returns the full history for this contract (`next_page_params` is empty): **14 transactions, all successful**. None reverted, and none of the three internal calls failed.

Twelve are the 25 Sep deploy, mint, seven `safeTransferFrom` sends, the first `setBaseURI`, and the two `setRoyaltyReceiver` calls. Two landed after the 28 Sep report. Both sent 0 ETH and succeeded:

1. **30 Sep 2026 16:34 UTC**, block 76,662,599 — deployer `0x86dF4D2fAA9aC25D408AA4E4Fb890B9918c5f066` called `transferOwnership` (`0x8a83841a…`). `owner` is now `0xe53bdb2118585d5B2cD06a117d3A036AFA70677a`.
2. **30 Sep 2026 19:44 UTC**, block 76,775,848 — that owner called `setBaseURI` (`0xf8958b97…`) to the jsDelivr pin in the table above.

Logs on the contract since block 74,933,922 are those two calls.

## Next 77

The week after the opening 7 adds 77 cards: token ids **8–84**. Shells for that wave are in `metadata/wave-02/`. They have the collection description and an external URL, and they do not invent images or the five card traits. Mint stays closed (`deploy: false`). These files are not a base URI for the live supply-7 contract. The live pin still has metadata only for tokens 1–7.

# Soft7 status — 26 Oct 2026

Read at Robinhood Chain block **98,537,681** (2026-10-26 16:02 UTC), chain ID **4663**.

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

Nothing in the supply table changed since the 19 Oct read at block 92,743,885. Tokens 1–7 still resolve on that pin. They are Art slots 033–039. Species is Tiger for 1, 3, 5, and 7, and Fox / Reynard for 2, 4, and 6. Token 8 on that pin is still a 404.

The royalty receiver holds 0 ETH. `royaltyInfo` for a 1 ETH sale returns 0.075 ETH. `ROYALTY_BPS` is 750.

## Holders

Six wallets hold the seven cards. `balanceOf` across those wallets sums to 7. The deployer and the contract owner hold none.

| Holder | Cards | Count |
| --- | --- | --- |
| `0x7c440909184FF4b45d96175ecCCdE4BD21901ab1` | 1, 7 | 2 |
| `0xd84E69Fa5a0975da11eDc9a9721CF893f7784BC6` | 2 | 1 |
| `0x49C1408183749BE16D3373a001FfB217B8e599d6` | 3 | 1 |
| `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` (vitalik.eth) | 4 | 1 |
| `0x8D00caE604984076a09218B854686549663Fb427` | 5 | 1 |
| `0x76443F52feb3561aaA71A01300602eB0b052bd45` | 6 | 1 |

The two-card wallet is an EIP-7702 account delegated to SemiModularAccount7702 `0x77021100bD87b7008E5E1989d0eB38555d0d0000`. That wallet holds 2 of 7. Each of the other five holds 1 of 7.

The token 2 wallet is also an EIP-7702 account, delegated to EIP7702StatelessDeleGator `0x63c0c19a282a1B52b07dD5a65b58948A07DAE32B`. The 19 Oct report did not record that delegation. This RPC does not serve state at block 92,743,885, so the block where the delegation was set is unknown. Token 2 has not moved.

Blockscout's token counter reads 10 holders. Its holder list has no next page and names these same six wallets. `ownerOf` matches that list.

No transfers since the deployer sent the cards out on 25 Sep 2026.

## Transactions

Blockscout's transaction list is complete (`next_page_params` is empty): **14 transactions, all successful**. The address counter reads 13 because it leaves out the creation transaction. None reverted, and none of the three internal calls failed.

No transaction has landed since the 19 Oct report. The newest call is still the 30 Sep 2026 19:44 UTC `setBaseURI` at block 76,775,848. Logs on the contract since block 92,743,885 are empty.

## Next 77

The next wave is still week index 1: token ids **8–84**. Shells for that wave are in `metadata/wave-02/`. They have the collection description and an external URL, and they do not invent images or the five card traits. Mint stays closed (`deploy: false`). These files are not a base URI for the live supply-7 contract. The live pin still has metadata only for tokens 1–7.

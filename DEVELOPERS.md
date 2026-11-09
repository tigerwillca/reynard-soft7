# Developers

This page is `index.html`, the phone-first Soft7 landing. The forest loop, the header Share menu, and the seven card links are all in that file. There is no build step and no contract source on this branch. Staking and dividend sentences below are the copy the page shows.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The page, its CSS, and two scripts. |
| `cursor.png` | Lime pointer. Hotspot is pixel `1, 1`. |
| `soft7-bg-loop.webm`, `soft7-bg-loop.mp4` | Forest loop. WebM is the first `<source>`. |
| `soft7-bg-key-01.png` | Video poster. |
| `images/phoenix-banner.webp`, `images/phoenix-banner-sm.webp` | On-page banner. The small file is the preload. |
| `images/display/033.webp`–`039.webp` | Cards 1–7. Art numbers are 033 through 039. |

Paths are relative to `index.html`. Opening the file, or serving this directory, is the whole preview.

Link-preview `og:image` and `twitter:image` point at the phoenix banner pinned on jsDelivr (`reynard-soft7-sepolia@74d0012480da26997a6b527e031fcd3ae0a5c699`), 960×540. The banner drawn on the page is the local WebP.

## Background and cursor

The loop is a fixed `<video class="bg">`: `autoplay`, `muted`, `loop`, `playsinline`, `aria-hidden="true"`, and `pointer-events: none`. A `.veil` gradient sits above it. The script under the video calls `play()` immediately and again on `canplay`. A rejected `play()` is ignored.

`prefers-reduced-motion: reduce` leaves `autoplay` set. In headless Chrome the video was still playing after that preference was applied.

`cursor.png` is the cursor on `html`, `body`, and every element under `body`, including links and buttons. `html` and `body` set `overflow-x: hidden`.

## Share

Share is a `<details class="share">` at the end of the header links. The summary reads `Share`. Copy and the device share sheet use `link[rel=canonical]`, which is `https://tigerwillca.github.io/`. That absolute href is what `canonical.href` returns when the file is opened from disk. If the canonical element is missing, the script falls back to the same URL.

| Control | When it shows | What it does |
| --- | --- | --- |
| Share… | `navigator.share` exists, and `canShare` is missing or returns true for the payload. A throw from `canShare` keeps it hidden. | Calls `navigator.share` with title `Reynard Soft7 · Robinhood Chain`, the dividend sentence below, and the canonical URL. Success writes `Shared` on this button. `AbortError`, or a missing error, leaves the button alone. Any other failure writes `Share did not open. Copy the link instead.` |
| Post on X | Always, including with JavaScript off. | A link to `https://x.com/intent/tweet` with the dividend sentence and `https://tigerwillca.github.io/`. `target="_blank"`. The href is fixed in the markup. It does not read the canonical element, and it does not write a status. |
| Copy link | Always. | `navigator.clipboard.writeText` of the canonical URL, then a hidden textarea and `document.execCommand("copy")` if that rejects or is missing. Success writes `Link copied` on this button. Failure writes `Could not copy the link`. |

The dividend sentence in the payload and in the X intent is: `Reynard Soft7 on Robinhood Chain. Seven cards. Holders stake by holding and receive a 1.5% quarterly on-chain dividend.`

The words a person sees are the button label. `#share-status` (`role="status"`, `aria-live="polite"`) receives the same string and is clipped to a 1×1 pixel box. Success adds `is-copied` (lime). Failure adds `is-error` (salmon, `#ffb4a8`). Closing the menu sets the status to empty, puts `Copy link` and `Share…` back, and removes both classes.

The menu stays open after a copy, a failed copy, and a native share. Escape closes it and focuses the summary. A click whose target is outside the `<details>` closes it. Both of those paths restore `Copy link`. Arrow keys do not move between the menu items. Tab still follows DOM order: Share… when it is shown, then Post on X, then Copy link.

### Where the menu sits

CSS lays `.share-menu` out as one nowrap row, `width: max-content`, `max-width: calc(100vw - 16px)`, absolutely just under the summary (`top: calc(100% + .25rem)`, `left: 0`). On open, on `resize`, and after every status change, `place()` clears the inline `top`, `bottom`, `left`, `right`, and `maxHeight`, then scores a new position. `maxHeight` is only cleared. Nothing assigns it.

`place()` skips elements inside `.share`, and it skips a box whose width and height are both under 1px. Everything else on this list is an obstacle. The number is the cost added when a candidate overlaps it.

| Obstacle | Cost |
| --- | --- |
| `#the-seven h2`, each `.grid img` | 100 |
| Each `.links a` outside Share, `header .mint`, `h1` | 50 for a link, 40 for the mint button and the title |
| `.banner`, `.lede`, `.eyebrow`, `.hint` | 25, 20, 15, 12 |
| `.dock`, only when its computed `display` is not `none` | 8 |

A candidate also takes 80 when its left or top is under 8px, or when its right or bottom passes `innerWidth - 8` or `innerHeight - 8`. Two small terms pull the row toward Share: `|left - summary.left| / 40` and `|top - (summary.bottom + 4)| / 40`. The lowest score wins. An equal score keeps the earlier candidate.

Left is clamped into `[8, max(8, innerWidth - 8 - width)]` before scoring. Top is only floored at 8. A candidate that hangs off the bottom or the right stays in the list and pays 80. Overlap uses the usual box test (`left < other.right` and the three matching edges). Touching an edge is not an overlap.

The first four candidates are below the summary, above it, to its right, and to its left, each with a 4px gap. Every obstacle whose cost is at least 40 adds two more, both at the summary's left: 8px above that obstacle, and 8px below it. The heading, the card images, the mint button, the title, and the five header links spawn those extra slots. The banner, the lede, the eyebrow, the hint, and the dock do not.

The inline `top` and `left` are offsets from the `<details>` box, and they are written only when they differ from the menu's current rect by more than half a pixel. The summary is inside `.share`, so the menu is allowed to cover Share.

Checked in headless Chrome:

| Viewport | Short row (`Post on X` and `Copy link`, about 200×57) | After `Could not copy the link` (about 303px wide) |
| --- | --- | --- |
| 1280×800 and 1280×900 | Sits on Share's left edge, bottom about 509, 8px above `#the-seven` (top about 517). Clear of the heading, the card images, the mint button, and the hint. A hit-test in the middle of Share returns Post on X. `Link copied` widens the row to about 217px and keeps that slot. | Same slot. Right edge about 929. Still clear of the heading and the cards. |
| 390×844 | Same slot: bottom about 617, heading top about 625. The dock is on screen (top about 774) and the row clears it. Share's middle still hits Post on X. | Moves up over the hint (top about 442). Right edge stays on the 8px inset (382). Heading and card images stay clear. |
| 390×667 | Same left and top as 390×844, so the row overlaps the dock (dock top about 597, menu bottom about 617) and stays 8px above the heading. Card images start at about 663 and stay clear. | Same upward move as 390×844, over the hint and clear of the dock. |
| 320×700 | Winner is the slot 8px under the header mint button (top about 427), overlapping the hint. Left is clamped so the right edge is 312. Share itself still receives a hit-test. Heading top is about 610. | Right edge is the viewport edge (320), so the 8px inset is missed. The row still overlaps the hint and stays clear of the heading and the cards. |

Below 720px the grid is two columns and card 7 is centered under the other six. The fixed mint dock is on screen. At `min-width: 720px` the grid is four columns, card 7 is a normal cell, and the dock is `display: none` (its box is empty, so it is not an obstacle). Both Mint links go to `https://opensea.io/collection/reynard-soft7`. The line under the header Mint link says the primary mint is closed and supply is 7.

## Cards

`#the-seven` is seven links. Token 1 uses `images/display/033.webp` and token 7 uses `images/display/039.webp`, in order. Each link points at `https://opensea.io/assets/robinhood/0x73D7b2611509C14078e16f572bE5aC7D91879DC2/{n}`. A click follows that link. The images are `loading="lazy"`.

## Copy the page states

These lines are in the staking and dividend sections. This branch does not include the contracts that would enforce them.

| Line on the page | Address or figure |
| --- | --- |
| Holding a card is the stake. Tokens 1–7 are the only position that earns. One share per card. | Vault `0x6B0E22d322c967DFBDB57D027cE53D1D32F7711A` |
| Secondary sales pay a 7.5% creator fee. 1.5% of the sale price, one fifth of that fee, is the holder dividend. | Router sends 80% to the creator and 20% to the vault |
| Router | `0x64c00a1c2d354F66aD5660548098F7cA25CEeb38` |
| Creator, as printed (lowercase) | `0xe53bdb2118585d5b2cd06a117d3a036afa70677a` |
| Contract | `0x73D7b2611509C14078e16f572bE5aC7D91879DC2` on Robinhood Chain 4663 |

## When the menu covers the wrong thing

| What you see | What `place()` did |
| --- | --- |
| The row lies on top of the word Share | The summary is not an obstacle. On a wide window and on a 390×844 phone the winning slot is 8px above `#the-seven`, which is also across the summary. Escape, or a click outside the `<details>`, still closes it. |
| The row sits on the mint dock on a short phone | The dock costs 8. Covering it scores less than covering the heading or a card, which cost 100. |
| The row covers the hint line | The hint costs 12. That happens at 320px wide with the short labels, and at 390px once the button reads `Could not copy the link`. |
| A long error label reaches the screen edge at 320px | Left is clamped, and top is only floored. A row wider than `innerWidth - 16` can still end on the viewport edge. The heading and the card images stayed clear in the check above. |
| Changing the button text leaves the row in a stale corner | `setStatus` calls `place()` after it changes the label. A resize does the same. Closing clears the inline position, so the next open starts from the CSS slot under the summary and scores again. |

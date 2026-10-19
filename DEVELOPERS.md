# Developers

This page is `index.html`, the phone-first Soft7 landing. The forest loop, the Share menu, and the card viewer are all in that file. There is no build step and no contract source on this branch. Staking and dividend sentences below are the copy the page shows.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The page, its CSS, and the three scripts. |
| `cursor.png` | Lime pointer. Hotspot is pixel `1, 1`. |
| `soft7-bg-loop.webm`, `soft7-bg-loop.mp4` | Forest loop. WebM is the first `<source>`. |
| `soft7-bg-key-01.png` | Video poster. |
| `images/phoenix-banner.webp`, `images/phoenix-banner-sm.webp` | On-page banner. The small file is also the favicon. |
| `images/display/033.webp`–`039.webp` | Cards 1–7. Art numbers are 033 through 039. |

Paths are relative to `index.html`. Opening the file, or serving this directory, is the whole preview.

## Background and cursor

The loop is a fixed `<video class="bg">`: `autoplay`, `muted`, `loop`, `playsinline`, `aria-hidden="true"`, and `pointer-events: none`. A `.veil` gradient sits above it. A script directly under the video pauses it when `prefers-reduced-motion: reduce` matches, before the toggle script runs.

`#bg-toggle` sits in the header links. Its label is `Pause video` while the video is playing and `Play video` while it is paused. The button is hidden if the video element is missing.

Reduced motion starts the page paused (`userPaused` begins true) and sets `autoplay` to false. Turning reduced motion on later pauses the video. Turning it off does not start playback; the label updates and the video stays paused until Play. Play from the button sets `userPaused` to false and calls `play()` even when reduced motion still matches, so a person can override the pause. If `play()` rejects, the label falls back to `Play video`. A later `canplay` calls `play()` only when the user has not paused and reduced motion does not match.

`cursor.png` is the cursor on `html`, `body`, and every element under `body`, including links and buttons.

## Share

Share is a `<details class="share">` in the header links. The summary reads `Share`. The canonical URL is the `link[rel=canonical]` href, which is `https://tigerwillca.github.io/`. Copy and the device share sheet use that URL, including when the file was opened from disk.

| Control | When it shows | What it does |
| --- | --- | --- |
| Share… | `navigator.share` exists, and `canShare` is missing or returns true for the payload. A throw from `canShare` keeps it hidden. | Calls `navigator.share` with title `Reynard Soft7 · Robinhood Chain`, the dividend sentence, and the canonical URL. Success sets status `Shared`. `AbortError`, or a missing error, leaves the status alone. Any other failure sets `Share did not open. Copy the link instead.` |
| Post on X | Always. | A link to `https://x.com/intent/tweet` with that sentence and the canonical URL. `target="_blank"`. It does not write a status. |
| Copy link | Always. | `navigator.clipboard.writeText` of the canonical URL, then a hidden textarea and `document.execCommand("copy")` if that rejects or is missing. Success sets `Link copied`. Failure sets `Could not copy the link`. |

Status text is `#share-status` (`role="status"`, `aria-live="polite"`). Errors add `is-error` (the salmon color). An empty status is `display: none`. Closing the menu clears the status and the inline position. The menu does not close itself after a copy or a native share.

Keyboard, while the menu is open: Escape closes it and focuses the summary. ArrowUp, ArrowDown, Home, and End move through `[role=menuitem]` elements that are not `hidden`, so a hidden Share… is skipped. A click outside the `<details>` closes the menu.

### Where the menu sits

CSS first places `.share-pop` absolutely just under the summary. On open, the script hides it, then on the next frame sets `position: fixed` and picks a rect. The inset is 8px. Below 720px the fixed mint dock is on screen, and the menu may not extend past the dock's top. At `min-width: 720px` the dock is `display: none` and the limit is the viewport.

A candidate is rejected when it:

- crosses the 8px inset, or the dock top when the dock is visible
- overlaps `#the-seven` on the vertical axis, at any horizontal position
- overlaps the header Mint button on both axes

The first candidate that fits wins, from this list. Left is clamped into the viewport before the test.

1. Above the summary, same left edge, 4px gap.
2. Below the summary, same left edge, 4px gap.
3. Under the header Mint button, to the right of the summary.
4. Under the header Mint button, to the left of the summary.
5. Just above the cards, same left edge, only when the band between the mint button and the cards is at least as tall as the menu.
6. The bottom of the allowed area.

If every candidate is rejected, the menu still opens, clamped to that bottom edge and the summary's left. That fallback is not checked against the cards, so it can cover them. `resize` runs the same placement. Changing the status text does not. `Link copied`, and the longer error lines, grow the menu after it has been placed.

## Card viewer

`#the-seven` is seven links. Token 1 uses `images/display/033.webp` and token 7 uses `images/display/039.webp`, in order. Each link points at `https://opensea.io/assets/robinhood/0x73D7b2611509C14078e16f572bE5aC7D91879DC2/{n}`.

A primary click with no Shift, Alt, Ctrl, or Meta opens `<dialog id="card-view">` and does not follow the link. Any other click, including a modified click, leaves the link alone so the browser can open that card on OpenSea. The hint above the grid is "Tap a card to look at it here."

The dialog copies the card's `currentSrc` (or `src`), `alt`, figcaption, and `href`. Previous and Next wrap: from card 1, Previous shows card 7. The OpenSea control in the dialog is that same per-card URL, in a new tab.

Close stays on the dialog, outside the scrolling `.card-sheet`, so it remains in the top-right while the sheet scrolls. Close, a click whose target is the dialog element itself, and Escape all close it. `html.card-open` sets `overflow: hidden` on the page. On close, focus returns to the link that opened the viewer.

ArrowLeft and ArrowRight move one card while the dialog is open. A horizontal swipe of at least 48px does the same: a swipe toward the left shows the next card. A swipe that starts within 24px of either screen edge is ignored.

The grid is two columns, with card 7 centered under the other six. At 720px and wider it is four columns and card 7 is a normal cell. The bottom mint dock shows only below 720px. The header Mint link shows at every width. Both Mint links go to `https://opensea.io/collection/reynard-soft7`. The line under the header Mint link says the primary mint is closed and supply is 7.

## Copy the page states

These lines are in the staking and dividend sections. This branch does not include the contracts that would enforce them.

| Line | What the page says |
| --- | --- |
| Stake | Holding a card is the stake. No lockup and no advertised rate. Tokens 1–7 earn. One share per card. |
| Fee | Secondary sales pay a 7.5% creator fee. 1.5% of the sale price, one fifth of that fee, is the holder dividend. |
| Split | Soft7RoyaltyRouter sends 80% to the creator and 20% to the vault. The vault pays holders of tokens 1–7 quarterly. |
| Vault | `0x6B0E22d322c967DFBDB57D027cE53D1D32F7711A` |
| Router | `0x64c00a1c2d354F66aD5660548098F7cA25CEeb38` |
| Creator | `0xe53bdb2118585d5b2cd06a117d3a036afa70677a` |
| Contract | `0x73D7b2611509C14078e16f572bE5aC7D91879DC2` on Robinhood Chain 4663 |

Link previews do not use the local banner. `og:image` and `twitter:image` are pinned to `images/phoenix-banner.webp` in `tigerwillca/reynard-soft7-sepolia` at commit `74d0012480da26997a6b527e031fcd3ae0a5c699`, served from `cdn.jsdelivr.net`. The on-page `<img>` uses the local WebP files.

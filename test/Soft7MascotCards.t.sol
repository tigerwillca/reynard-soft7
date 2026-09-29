// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import {Soft7MascotCards} from "../contracts/Soft7MascotCards.sol";

interface Vm {
    function warp(uint256 newTimestamp) external;
    function deal(address account, uint256 newBalance) external;
    function prank(address msgSender) external;
    function chainId(uint256 newChainId) external;
    function expectRevert(bytes4 revertData) external;
    function addr(uint256 privateKey) external returns (address);
}

/// @notice Runs Soft7MascotCards. Mint stays a local fork of the bytecode.
contract Soft7MascotCardsTest {
    bool public IS_TEST = true;

    Vm internal constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    uint256 internal constant PRICE = 10 ether;

    Soft7MascotCards internal cards;
    address internal holder;
    address internal other;
    address internal third;

    function setUp() public {
        holder = vm.addr(1);
        other = vm.addr(2);
        third = vm.addr(3);
        cards = new Soft7MascotCards("https://example.com/meta/");
        cards.setMintPrice(PRICE);
        vm.chainId(4663);
    }

    function test_waveCapStaysShutUntilWavesOpen() public {
        if (cards.waveCap() != 0) revert("closed");
        if (cards.proofsApproved()) revert("proofs");
        if (cards.opening() != 0) revert("opening");
    }

    function test_mintRevertsUntilProofsAreApprovedAndWavesOpen() public {
        _pay(holder);
        vm.prank(holder);
        vm.expectRevert(Soft7MascotCards.ProofsPending.selector);
        cards.mint{value: PRICE}();

        cards.approveProofs();
        _pay(holder);
        vm.prank(holder);
        vm.expectRevert(Soft7MascotCards.ProofsPending.selector);
        cards.mint{value: PRICE}();
    }

    function test_strangerCannotApproveOrOpen() public {
        vm.prank(holder);
        vm.expectRevert(Soft7MascotCards.NotOwner.selector);
        cards.approveProofs();

        cards.approveProofs();
        vm.prank(holder);
        vm.expectRevert(Soft7MascotCards.NotOwner.selector);
        cards.openWaves();
    }

    function test_openWavesRequiresProofsAndOpensOnce() public {
        vm.expectRevert(Soft7MascotCards.ProofsPending.selector);
        cards.openWaves();

        cards.approveProofs();
        cards.openWaves();
        vm.expectRevert(Soft7MascotCards.AlreadyOpen.selector);
        cards.openWaves();
    }

    function test_baseMustEndInSlash() public {
        vm.expectRevert(Soft7MascotCards.BadBase.selector);
        new Soft7MascotCards("https://example.com/meta");
    }

    function test_wrongChainAndWrongPriceRevert() public {
        _open();
        vm.chainId(1);
        _pay(holder);
        vm.prank(holder);
        vm.expectRevert(Soft7MascotCards.WrongChain.selector);
        cards.mint{value: PRICE}();

        vm.chainId(4663);
        vm.deal(holder, 1);
        vm.prank(holder);
        vm.expectRevert(Soft7MascotCards.WrongPrice.selector);
        cards.mint{value: 1}();
    }

    function test_weekZeroMintsSevenAndTheEighthWaits() public {
        _open();
        if (cards.waveCap() != 7) revert("week0");
        for (uint256 i = 0; i < 7; i++) {
            uint256 tokenId = _mint(holder);
            if (tokenId != i + 1) revert("id");
        }
        if (cards.totalSupply() != 7) revert("supply");
        _pay(holder);
        vm.prank(holder);
        vm.expectRevert(Soft7MascotCards.WaveFull.selector);
        cards.mint{value: PRICE}();

        vm.warp(uint256(cards.opening()) + 7 days);
        if (cards.waveCap() != 84) revert("week1");
        _mint(holder);
        if (cards.totalSupply() != 8) revert("week1 mint");
    }

    function test_weekTenReaches777AndStops() public {
        _open();
        uint256 opening = cards.opening();
        vm.warp(opening + 63 days);
        if (cards.waveCap() != 700) revert("week9");
        vm.warp(opening + 70 days);
        if (cards.waveCap() != 777) revert("week10");
        vm.warp(opening + 77 days);
        if (cards.waveCap() != 777) revert("week11");
    }

    function test_unstakedMintPaysTheFullAmountTo77a() public {
        _open();
        address payout = cards.PAYOUT();
        uint256 before = payout.balance;
        _mint(holder);
        if (payout.balance - before != PRICE) revert("full payout");
        if (cards.pending(holder) != 0) revert("no stake");
        if (address(cards).balance != 0) revert("left in contract");
    }

    function test_stakedHolderPullsTenPercent() public {
        _open();
        uint256 tokenId = _mint(holder);
        vm.prank(holder);
        cards.stake(tokenId);

        address payout = cards.PAYOUT();
        uint256 before = payout.balance;
        _mint(other);
        if (payout.balance - before != (PRICE * 9) / 10) revert("ninety");
        if (cards.pending(holder) != PRICE / 10) revert("ten");

        uint256 held = holder.balance;
        vm.prank(holder);
        cards.pull();
        if (holder.balance - held != PRICE / 10) revert("pulled");
        if (cards.pending(holder) != 0) revert("cleared");
    }

    function test_twoStakersSplitTheTenPercent() public {
        _open();
        uint256 first = _mint(holder);
        vm.prank(holder);
        cards.stake(first);
        uint256 second = _mint(other);
        vm.prank(other);
        cards.stake(second);

        _mint(third);
        uint256 half = (PRICE / 10) / 2;
        if (cards.pending(holder) != half) revert("holder half");
        if (cards.pending(other) != half) revert("other half");
    }

    function test_threeStakersLeaveDustInTheContract() public {
        _open();
        uint256 a = _mint(holder);
        vm.prank(holder);
        cards.stake(a);
        uint256 b = _mint(other);
        vm.prank(other);
        cards.stake(b);
        uint256 c = _mint(third);
        vm.prank(third);
        cards.stake(c);

        vm.prank(holder);
        cards.pull();
        vm.prank(other);
        cards.pull();

        _mint(vm.addr(4));
        uint256 share = (PRICE / 10) / 3;
        if (cards.pending(holder) != share) revert("a");
        if (cards.pending(other) != share) revert("b");
        if (cards.pending(third) != share) revert("c");

        vm.prank(holder);
        cards.pull();
        vm.prank(other);
        cards.pull();
        vm.prank(third);
        cards.pull();
        if (address(cards).balance != (PRICE / 10) - (share * 3)) revert("dust");
        if (address(cards).balance == 0) revert("dust gone");
    }

    function test_transferOfAStakedCardClearsTheStake() public {
        _open();
        uint256 tokenId = _mint(holder);
        vm.prank(holder);
        cards.stake(tokenId);
        _mint(other);

        if (cards.pending(holder) != PRICE / 10) revert("owed");
        vm.prank(holder);
        cards.transferFrom(holder, other, tokenId);

        if (cards.stakedBy(tokenId) != address(0)) revert("still staked");
        if (cards.stakedCount(holder) != 0) revert("count");
        if (cards.ownerOf(tokenId) != other) revert("owner");
        if (cards.pending(holder) != PRICE / 10) revert("kept");
        if (cards.pending(other) != 0) revert("receiver stake");

        uint256 held = holder.balance;
        vm.prank(holder);
        cards.pull();
        if (holder.balance - held != PRICE / 10) revert("still pullable");
    }

    function test_movingStakeDoesNotGiveTheNextHolderThePreviousCut() public {
        _open();
        uint256 tokenId = _mint(holder);
        vm.prank(holder);
        cards.stake(tokenId);
        _mint(other);
        vm.prank(holder);
        cards.unstake(tokenId);

        uint256 next = _mint(other);
        vm.prank(other);
        cards.stake(next);
        _mint(third);

        if (cards.pending(holder) != PRICE / 10) revert("first cut");
        if (cards.pending(other) != PRICE / 10) revert("second cut");
    }

    function test_tokenUriAndRoyalty() public {
        _open();
        uint256 tokenId = _mint(holder);
        if (keccak256(bytes(cards.tokenURI(tokenId))) != keccak256(bytes("https://example.com/meta/1.json"))) {
            revert("uri");
        }
        (address receiver, uint256 royalty) = cards.royaltyInfo(tokenId, 10_000);
        if (receiver != cards.PAYOUT()) revert("receiver");
        if (royalty != 750) revert("royalty");
    }

    function _open() internal {
        cards.approveProofs();
        cards.openWaves();
        vm.chainId(4663);
    }

    function _pay(address account) internal {
        vm.deal(account, account.balance + PRICE);
    }

    function _mint(address account) internal returns (uint256 tokenId) {
        _pay(account);
        vm.prank(account);
        tokenId = cards.mint{value: PRICE}();
    }
}

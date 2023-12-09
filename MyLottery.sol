// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.6.0;

contract MyLottery {
    address public owner;
    address payable[] public players;

    event WinnerPicked(address winner);

    constructor() public {
        owner = msg.sender;
    }

    function enter() public payable {
        require(msg.value > .01 ether, "Not enough ETH sent.");
        players.push(payable(msg.sender));
    }

    function random() private view returns (uint) {
        return uint(keccak256(abi.encodePacked(block.difficulty, block.timestamp, players)));
    }

    function pickWinner() public restricted {
        require(players.length > 0, "No players to pick from.");
        uint index = random() % players.length;
        address payable winner = players[index];
        winner.transfer(address(this).balance);
        emit WinnerPicked(winner);
        players = new address payable[](0);
    }

    function getPlayers() public view returns (address payable[] memory) {
    	return players;
	}

    modifier restricted() {
        require(msg.sender == owner, "This function is restricted to the contract's owner");
        _;
    }
}

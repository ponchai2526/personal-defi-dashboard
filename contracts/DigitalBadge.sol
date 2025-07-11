// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract DigitalBadge is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    string private _baseURI;

    constructor(string memory name_, string memory symbol_, string memory baseURI_) ERC721(name_, symbol_) {
        _baseURI = baseURI_;
    }

    function safeMint(address to) public {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseURI;
    }

    // ฟังก์ชันสำหรับกำหนด Base URI ในภายหลัง (ถ้าต้องการ)
    function setBaseURI(string memory baseURI_) public {
        _baseURI = baseURI_;
    }
}

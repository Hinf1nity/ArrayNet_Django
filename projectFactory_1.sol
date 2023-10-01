// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;
import "@openzeppelin/contracts@4.5.0/token/ERC20/ERC20.sol";

contract ProjectsPadre {
    address oficialOwner;
    mapping (address => address) public projectsContracts;

    function createProject(
        string memory _name,
        string memory _symbol,
        string memory _description,
        string memory _photos,
        string memory _links,
        uint _goal,
        uint _actionTokensNum,
        uint _tokenPrice,
        uint _percentage
    ) public {
        require(_percentage<50,"Incorrect percentage value");
        address addrprojectsContracts = address(
            new ProjectHijo(
                msg.sender,
                address(this),
                _name,
                _symbol,
                _description,
                _photos,
                _links,
                _goal,
                _actionTokensNum,
                _tokenPrice,
                _percentage
            )
        );
        projectsContracts[msg.sender] = addrprojectsContracts;
    }
}

contract ProjectHijo {
    string public name;
    string public symbol;
    string public description;
    string public photos;
    string public links;
    uint public goal;
    uint public totalFunds;
    uint public actionTokensNum;
    ERC20 companyToken;
    uint public tokenPrice;
    bool public fundingGoalReached;
    bool public campaignEnded;
    uint public percentage;
    //address investor, token project
    mapping(address=>uint) public inversiones;
    Owner public propietario;
    mapping (address => address) public tokensContracts;


    
    struct Owner {
        address _ownerProject;
        address _smartContractPadre;
    }

    event TokensPurchased(address indexed purchaser, address indexed beneficiary, uint256 value, uint256 amount);

    constructor(
        address _account,
        address _accountSC,
        string memory _name,
        string memory _symbol,
        string memory _description,
        string memory _photos,
        string memory _links,
        uint _goal,
        uint _actionTokensNum,
        uint _tokenPrice,
        uint _percentage
    ) {
        propietario._ownerProject = _account;
        propietario._smartContractPadre = _accountSC;
        name = _name;
        symbol = _symbol;
        description = _description;
        photos = _photos;
        links = _links;
        goal = _goal;
        totalFunds = 0;
        actionTokensNum = _actionTokensNum;
        companyToken = new TokenHijo(_name,_symbol,actionTokensNum);
        companyToken.transfer(propietario._smartContractPadre, 1);
        tokensContracts[msg.sender] = address(companyToken);
        tokenPrice = _tokenPrice;
        percentage=_percentage;
        fundingGoalReached = false;
        campaignEnded = false;
    }

    function buyTokens(uint256 amount) external payable {
        require(msg.value > 0, "Amount must be greater than zero");

        require(msg.value == amount * tokenPrice, "Incorrect ether amount sent");

        payable(propietario._ownerProject).transfer(msg.value);

        companyToken.transfer(msg.sender, amount);

        inversiones[msg.sender]=companyToken.balanceOf(msg.sender);

        emit TokensPurchased(msg.sender, propietario._ownerProject, msg.value, amount);
    }
}


contract TokenHijo is ERC20 {
    address public tokenAddress;

    event TokenDeployed(address indexed tokenAddress);

    
    constructor(string memory _name, string memory _symbol, uint256 _totalSuply) ERC20(_name, _symbol) {
        _mint(msg.sender, _totalSuply);
        tokenAddress = address(this);
        emit TokenDeployed(tokenAddress);
    }

    
}

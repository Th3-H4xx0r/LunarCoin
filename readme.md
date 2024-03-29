[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Lunar Coin</h3>

  <p align="center">
     Lunar Coin is a digital payment method that involves transactions with zero transaction fees. An important aspect of Lunar Coin is being eco-friendly due to the decreased amount of energy required, as well as requiring fewer validator nodes. Lunar coins, being energy efficient as well as having minimal environmental impact, will be the digital currency that you can use whenever and wherever you want.
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://lunarcoin.network)

Fill out

### Built With

Here are a list of major frameworks or languages used to build LunarCoin.
* [Python](https://www.python.org)
* [Socket.io](https://socket.io/)
* [Ngrok](https://ngrok.com/)
* [Cryptography](https://cryptography.io)



<!-- GETTING STARTED -->
## Getting Started

To get started with running a validator node for the Lunar Coin network, follow the steps below to get started. If at any point, you need help, please contact our developers at dev@lunarcoin.network

### Prerequisites

These are some prerequisites that are required to run a LunarCoin validator node.
* Python (Linux)
  ```sh
  $ sudo apt-get update
  $ sudo apt-get install python3.8
  ```
  
  or 
  
* Python Windows: https://www.python.org/downloads/

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Th3-H4xx0r/LunarCoin
   ```
2. Install python dependencies
   ```sh
   pip install -r requirements.txt
   ```
   
   or 
   
   ```sh
   python -m pip install -r requirements.txt
   ```
   
3. Generate your miner wallet
   ```sh
   python GenerateWallet.py
   ```
   
4. Make an ngrok account: https://ngrok.io

6. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
   
4. Configure your config.json file

 ```sh
 {
    "minerID": Add your validator ID that we will provide you with,
    "ngrokAuthToken": Replace the default auth token with your ngrok auth token,
    "network": "mainnet" or "testnet"
}
 ```
 
 Need an minerID? Vist: https://lunarcoin.network/validator



<!-- USAGE EXAMPLES -->
## Usage

After you have completed all the steps in the installation section above. Follow the steps below to get started with running your validator node.

 ```sh
  python validatorNode.py
 ```

<!--
_For more examples, please refer to the [Documentation](https://example.com)_
-->


<!-- ROADMAP -->
## Roadmap

See the [roadmap](https://lunarcoin.network/roadmap) for our official roadmap.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**. Follow the steps below to contribute to our project. Please also feel free to share and explain your changes by creating a post on the contributions section on our website: https://lunarcoin.network/contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

LunarCoin Dev Team - dev@lunarcoin.network

Project Website: [Lunar Coin Website](https://lunarcoin.network)

Project Whitepaper: [Whitepaper](https://lunarcoin.network/whitepaper)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png

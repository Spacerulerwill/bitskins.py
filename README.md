# bitskins.py
A basic WIP API wrapper for the BitSkins website in Python, mapping the API Commands to corresponding functions.

Features support for all BitSkins supported games:
* PUBG
* PAYDAY2,
* KILLING FLOOR 2
* RUST
* DEPTH 
* UNTURNED
* CSGO
* DOTA2
* TF2

Example Usage:

Installation

```
pip install bitskins
```

```python
from bitskins import BitSkins, RUST

wrapper = BitSkins("api key here", "secret here")

print(wrapper.getAccountInventory(game=RUST, page=10))
```

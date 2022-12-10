# SMILES-display


[![developer](https://img.shields.io/badge/Dev-grillazz-green?style)](https://github.com/grillazz)

### Project Description
Purpose of this showcase is integrate Oracle SQL backend with FastAPI Python ASGI Framework
as API for chemical compounds extended analyze with [RDKit](https://github.com/rdkit/rdkit) Library.

Act as a backend to render SVG chemical structures delivered as an api. Designed
to be integrated within Dotmatics to view Virtual Compound database.


### How to Setup
To build:
1. `python3 -m pipenv sync`
2. `python3 -m pipenv shell`
3. `python app.py`


### How to Play
1. Enter VK/FT compound ID and integer size of image as parameters.
   
2. Using the endpoint: `/v1/draw-smiles` endpoint
    ```shell
    curl --location --request GET 'http://0.0.0.0:8000/v1/draw-smiles?compound_id=${FT||VK}&size=${SIZE} \
    ```

3. And get response like below with `200 OK`
   ```json
   ```

### Change Log
- 16 APR 2022 aioredis replaced with redis.asyncio

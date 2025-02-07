# POE Character Log

## Path of Exile Character Log - track any PoE character as it's played

This is still work-in-progess, but feel free to tinker with it.

## How to use

1. Install requirements

```bash
pip install -r requirements.txt
```

2. Start one instance of POECLog

```bash
python -m POEClog
```

3. Start one instance of POECLogApi

```bash
python -m POEClogApi
```

4. Install Website

```bash
cd website && npm i
```

5. Start Website

```bash
npm run dev
```

Goto http://localhost:3000 and look at your website!

## Easier use

Use docker-compose to start up everything.

```bash
docker-compose -f docker-compose.yml up -d
```

Goto http://localhost:8080 and look at your website!

## Configure

Change the config file in config/settings.json

Accounts: - List of every account which should be logged. - Cannot be empty

Character: - List of all logged characters within the aboved listed accounts - When empty every character will be logged

Shortsleep: - Waiting time when connection failed ( in seconds )

Longsleep: - Waiting time between character logs ( in seconds )

MaxLevel: - Maximum level of characters to get logged

MinLevel: - Minimum level of characters to get logged

Levelstep: - Minimum level differentce of characters to get logged

## Tech Stack

- Python
- FastApi
- SQLite
- SQLAlchemy
- Sveltekit
- Docker

## Screenshots

![Landing Page](/assets/Screenshot.png)

![Character Screen](/assets/Screenshot2.png)

## Known Issues

If someone creates multiple characters with the same name, data from all those characters will be gathered into a single histroy.
This means PoB output etc. will be nonsensical - but I'm also not really sure what to do with this right now so... The only person who really does this is Zizaran - try to die less than he does perhaps?

Also Cluster Jewel are not supported yet!

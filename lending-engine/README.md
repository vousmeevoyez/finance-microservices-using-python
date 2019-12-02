# LENDING Engine

Lending Engine is a high level services that orchestrate transaction engine and other services like BNI RDL gRPC and Notif gRPC.

Lending Engine: currently handle functionality like creating rdl, process virtual account callback, disburse money and collect repayment

## Installation

running locally: 
1. Make sure have at least python3 installed
2. Install dependency (pip install -r requirements.txt)
3. start services (make run)
4. start investor worker (make investor-worker) more details can be checked on Makefile

running via container: 
1. Make sure have docker installed
2. Build image (make build)
3. Run image (make run)

## Usage

run unittest: 
unittest is configured to be run using pytest
1. all fixture can be found on conftest.py
2. run all unittest (pytest)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

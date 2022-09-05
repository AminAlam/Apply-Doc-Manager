# Apply-Doc-Manager

I am not a fan of Excel or Google Docs for storing search-needing information, so I made this app to manage my documents while applying for scientific positions. Please note that it is not a commercial program and may face some bugs. If you face any bugs, please feel free to open an issue about it.

## Requirements
You can install the dependencies by running:  `pip install -r requirements.txt`.

## How to use
Clone the repository and run `python3 apply_doc_manager.py --help` from its directory to see the featured options. You can set the IP and Port on which the program runs. Then run the program (`python3 apply_doc_manager.py` runs the program on the default IP and Port) then go to this URL in a browser (if '--server_ip' and '--port' are not specified): [http://localhost:8080](http://localhost:8080).

Note that a .db file in the cloned directory stores all the information of the supervisors, so DO NOT delete this folder unless you do not need the supervisors' information anymore.

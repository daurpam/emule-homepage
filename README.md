## Emule Homepage widget
This docker container expose in a web browser the statistics of the Emule client.

Main statistics exposed:
* Total bytes uploaded
* Total bytes downloaded
* Total ratio
* Time from last reset of statistics

## Files
- Dockerfile: to create the docker image
- api.py: main program
- requirements.txt: python packages required to build image
- docker-compose.yml: file to build and launch container
- services.yaml: code to include on homepage config file
- emule.png: image icon for homepage widget
- statistics.ini: example of stats file from eMule


## Run
1. clone this repo: ```git clone https://github.com/daurpam/emule-homepage.git```
2. Copy file **statistics.ini** from your eMule or aMule client
1. Run command ```docker-compose up --build -d```
2. Test if info shows in browser with command ```curl http://localhost:5000/api/emule```
3. Add code of services.yaml in the file of Homepage **services.yaml**
4. Modify **[SERVER]** in services.yaml with your IP or FDQN in which you are running this image
5. Check if widget load with data

## Example
<img width="301" height="108" alt="image" src="https://github.com/user-attachments/assets/77b4a93b-0b86-4288-8869-b996a9f85337" />

## Update info
You can run a schedule program to overwrite statistics.ini file, with a newer version to update data in Homepage widget. There's no need to restart container.

## Roadmap
I'll try to add another version to add session stats.

### Configure Git

#### Initialize a repo and then push to github
	git init

#### Clone a Github repo to local
	git clone https://github.com/jerinsam/SQL_SERVER_TO_REDIS_KAFKA_CONNECT

##### Git Config
	git config --global user.email "xxxx@gmail.com"
	git config --global user.name "xxxx"
	git add README.md
	git commit -m "first commit"
	git branch #To check which branch you are in
	git branch -M main

##### Show Git origin details 
	git remote show origin

##### Add Git origin 
	git remote add origin https://github.com/jerinsam/SQL_SERVER_TO_REDIS_KAFKA_CONNECT.git

##### Track changes of Remote Repor dev branch 
	git push --set-upstream origin dev

	git push -u origin main
		token : XXXXXXXXXX-XXXXXXXXXXXXX-XXXXXXXXX

#### Create new branch 

##### Identify new changes in the Origin i.e. remote (github) repo
	git fetch origin
##### Update local repo with any change in remote repo
	git pull origin main
##### Checkout to create new dev branch 
	git checkout -b dev

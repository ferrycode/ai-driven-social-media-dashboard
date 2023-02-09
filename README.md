# ai-driven-social-media-dashboard
## The git repo contains the following: 
1. A cloudFormation Template, which directly creates all required cloud resources, i.e servers, serverless apps, roles, ..and environmetronment variables 
2. Source code for two Lambda function, one for ingesting Twitter through twitter API, 
3. The other one is a Trigger function on S3 once raw/ folder filled willed with raw json, iterate records and invoke required translate and comprehend services 
4. A shell script takes two arguments: the base S3 bucket name, and the version (v1.0)
5. A Python script to read an array JSON file, convert into "json line delimited" file to be red by AWS Kinesis agent for Windows 

## Requirements:
1. Create a "unique" S3 bucket (BASENAME-[regionname]), example: ai-dahboard-us-east-1, the BASENAME "ai-dashboard" will be passed to the shell script 
2. Create a new Ubuntu EC2 machine, if necessary,  to compile the code, update it or use your local machine 
3. Create a new Windows EC2 machine, if necessary, to install AWS Kinesis agent for Windows

## Build the source code: 
1. initiate a shell session in the EC2 or local linux box
2. Update the EC2 or local linux box:
	sudo apt-get update
	sudo apt-get install zip sed wget -y
	sudo apt-get install npm 
3. Clone the git repo locally 
	git clone https://github.com/amazon-archives/ai-driven-social-media-dashboard.git (not working anymore, please clone the forked source as following)
	git https://github.com/ferrycode/ai-driven-social-media-dashboard-original-updated-to-meet-current-requiremt-.git

4. Switch to the "deployment" directory 
	cd deployment

5. Run the shell script, to generate the dist of AWS CloudFormation template and Lambda packages, with "S3 Bucket BASENAME" and version, i.e:
	./build-s3-dist.sh ai-dahboard v1.0 

6. After completion, switch to the "dist" directory, the following files are created 
	addtriggerfunction.zip, ec2_twitter_reader.tar, socialmediafunction.zip and ai-driven-social-media-dashboard.template (AWS CF Template)
7. Download the whole directory locally 

## Configure AWS 

1. In the AWS Management Console, switch to S3 
2. Go to the source bucket, (BASENAME), i,e ai-dahboard
3. Create directory "ai-driven-social-media-dashboard", then switch into it
4. Create "version" directory as provided the second argument in build-s3-dist.sh, i.e "v1.0" 
5. Upload the compiled and downloaded Lambda packages, addtriggerfunction.zip, ec2_twitter_reader.tar, socialmediafunction.zip
6. Now, create the entire AWS solution through AWS CloudFormation CF, as following 
7. In the AWS Management Console, switch to CloudFormation 
8. Create stack, follow the instructions, give it a name,
9. In the "Template source", select "Upload a template file" and chose the downloaded template earlier, upload
10. Select next, the wizard will ask for environment variables 
11. If you intended to ingest real Twitter posts and you have the required Twitter API, provide the associated required variables
12. Otherwise, provide any dummy data, do not leave blank the required four Twitter API Variables 
13. AWS will create everything for you in minutes, be sure the action is completed successfully without any error 

## For using example JSON array tweets data, instead of real Twitter ingestion
1. AWS Kinesis agent for Windows is preferred, download it (https://s3-us-west-2.amazonaws.com/kinesis-agent-windows/downloads/index.html) and install 
2. Getting start link https://docs.aws.amazon.com/kinesis-agent-windows/latest/userguide/getting-started.html  
3. User guide download https://s3-us-west-2.amazonaws.com/kinesis-agent-windows/downloads/Kinesis-Agent-for-Windows-User-Guide.pdf
4. Switch into the installation directory C:\Program Files\Amazon\AWSKinesisTap
5. Find the configuration file "appsettings.json", to configure the sources, sinks and pipes, you can find a template example one on the git repo
6. Now we create the required AWS user to provide with “Kinesis Full Access” permission 
7. In the AWS Management Console, switch to IAM 
8. Select "Add user"
9. Provide new name i.e "kinesis-windows-agent"
10. Select Select AWS credential type : Access key - Programmatic access, leave "Password - AWS Management Console access" unchecked 
11. Click Next: Permissions 
12. In "Set Permissions", click "Attach existing policies directly"  and select required policy "AmazonKinesisFirehoseFullAccess"
13. Follow the rest wizard without changes, complete and add the user 
14. Keep and save the values of "User", "Access key ID" and "Secret access key"
15. Update those values in "appsettings.json" "Sinks" section
16. Create the "Sources" directory. i.e C:\tweets, update it in "appsettings.json" "Sinks" section
17. Now, start the agent, open PowerShell prompt with Administrator privilege, run 
	Start-Service -Name AWSKinesisTap
18. The agent now ready and listen to any created json files, "json line delimited" files

## Simulate Twitter posts 
1. Find python script generate_tweets.py update if require
2. Find sample tweets.json (or tweets.log ) file
3. Update Python script with appropriate values
	json_from_filepath = "c:\\tweets\\tweets.log"
	json_to_filepath = "c:\\tweets\\tweets_to.json"
4. Run the script


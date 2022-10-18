# Python sample app using pipenv package manager


See Ben's video [here](https://www.youtube.com/watch?v=Nq-F0VWwRYg)

A basic sample which began life as part of the [Packeto Buildpack](https://github.com/paketo-buildpacks/samples) samples. Designed to illustrate how buildpacks and supply chains work to build and deploy an application. Should work just fine with VMware Tanzu Application Platform and VMware Tanzu Application Service.


# App Basics
* Connects to Rabbit MQ using teh info provided via Environment variables
* Home page shows the number of items in the queue
* /loadset populates a dropdown list of Magic: The Gathering set names from https://api.scryfall.com
* When a user selects a set and clicks "Fetch Data" button, the app retrieves data for each card in teh set and parses each card record as a message into the queue
* Works in conjunction with a worker to process the items in the work queue



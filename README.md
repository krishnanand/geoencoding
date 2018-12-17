# Geo Encoding Service.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
  * [Get Latitude Longitude](#get-latitude-longitude)
    1. [Request Query Parameter](#request-query-parameter)

# Requirements

* Python 3.6.5
* Django framework
* Django Rest Framework

# Setup

* Clone the repository.

* Install Python 3.6.5 and above. You can use your favourite tool to install the software (HomeBrew, pyenv)

* Set up virtualenv with the following command ``virtualenv -p `which python3` env``

* Install the python packages required by the project by executing `pip install -r requirements.txt`.

* Run the migration scripts by executing the following commands from the home directory `cd geoencoding`

* Run the command `python manage.py runserver` to start the server.

# API Endpoints

To fetch the latitude and longitude response, you need the API Keys for both [Here](https://developer.here.com/documentation/geocoder/topics/quick-start-geocode.html) and [Google Maps](https://developers.google.com/maps/documentation/geocoding/start).

Make sure that you have a module named `api_keys` in your django app. Module should define the following variables.

```
HERE_APP_ID=<HERE_APP_ID>
HERE_APP_CODE=<HERE_APP_CODE>
GOOGLE_APP_KEY=<GOOGLE_APP_KEY>
```

## Get Latitude Longitude

`GET /encoding/lat_long?address=<address>`

Returns the latitude and longitude

### Request Query Parameter ###

| Name | Type | Description | Required  |
| :---         |     :---:      |          :--- |      :---:      |
| address  | string | Addressed to be looked up |true

The sample request is given below:

`/encoding/lat_long?address=1600+Amphitheatre+Parkway+Mountain+View`

### Response Body

A response status code will be 200 OK and will have the following characteristics.

| Name | Type | Description | Required  |
| :---         |     :---:      |          :--- |      :---:      |
| latitude  | decimal | Unique latitude |true
| longitude | decimal | Unique longitude |true


### Error Response Body

The error response body represents an error of errors returned as 200 OK

| Name | Type | Description | Read only |
| :---         |     :---:      |          :--- |      :---:      |
| errors  | array | array of error objects |true |

where each error object consists of the following fields

| Name | Type | Description | Read only |
| :---         |     :---:      |          :--- |      :---:      |
| error code  | number | error code indicating the kind of error|true |
| error message  | string | user friendly message |true |

Some of the sample responses are given below

```
 {
   'errors': [
       {
         'error_code': 400,
         'error_message': 'No Data Found'
       }
   ]
 }
```

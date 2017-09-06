.. Kicking page rebuild 2014-10-30 20:55:46
.. _assets:

Retrieving Asset Information
=============================

Getting list of all assets
--------------------------

.. http:get:: /assets

   Getting list of all assets.

   **Example request**:

   .. sourcecode:: http

      GET api/0/assets HTTP/1.1
      Host: lb.api-sandbox.registry.ea.openprocurement.net

   **Example response**:

   .. sourcecode:: http

      200 OK
      Content-Type: application/json
      X-Content-Type-Options: nosniff

      {
        "next_page": {
          "path": "/api/0.1/assets?offset=2017-08-14T13%3A35%3A31.474578%2B03%3A00",
          "uri": "http://lb.api-sandbox.registry.ea.openprocurement.net/api/0.1/assets?offset=2017-08-14T13%3A35%3A31.474578%2B03%3A00",
          "offset": "2017-08-14T13:35:31.474578+03:00"
        },
        "data": [
          {
            "id": "2f684c8a57f447768a5a451e2e8e5892",
            "dateModified": "2017-08-14T13:35:31.474578+03:00"
          },
          {
            "id": "1f28428a37f457768a5a451e2e8e5892",
            "dateModified": "2017-08-15T13:35:31.474578+03:00"
          }
        ]
      }



   :query offset: offset number
   :query limit: limit number. default is 100
   :reqheader Authorization: optional OAuth token to authenticate
   :statuscode 200: no error
   :statuscode 404: endpoint not found

Sorting
~~~~~~~
Assets returned are sorted by modification time.

Limiting number of Assets returned
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can control the number of `data` entries in the assets feed (batch
size) with `limit` parameter. If not specified, data is being returned in
batches of 100 elements.

Batching
~~~~~~~~

The response contains `next_page` element with the following properties:

:offset:
    This is the parameter you have to add to the original request you made
    to get next page.

:path:
    This is path section of URL with original parameters and `offset`
    parameter added/replaced above.

:uri:
    The full version of URL for next page.

If next page request returns no data (i.e. empty array) then there is little
sense in fetching further pages.

Synchronizing
~~~~~~~~~~~~~

It is often necessary to be able to syncronize central database changes with
other database (we'll call it "local").  The default sorting "by
modification date" together with Batching mechanism allows one to implement
synchronization effectively.  The synchronization process can go page by
page until there is no new data returned.  Then the synchronizer has to
pause for a while to let central database register some changes and attempt
fetching subsequent page.  The `next_page` guarantees that all changes
from the last request are included in the new batch.

The safe frequency of synchronization requests is once per 5 minutes.
 
Reading the individual asset information
-----------------------------------------

.. http:get:: /assets/{uuid4:id}

   Getting asset details.

   **Example request**:

   .. sourcecode:: http

      GET /api/0.1/assets/2f684c8a57f447768a5a451e2e8e5892 HTTP/1.0
      Host: lb.api-sandbox.registry.ea.openprocurement.net

   **Example response**:

   .. sourcecode:: http


      200 OK
      Content-Type: application/json

      {
        "data": {
          "status": "pending",
          "assetType": "basic",
          "classification": {
            "scheme": "CAV",
            "description": "Земельні ділянки",
            "id": "39513200-3"
          },
          "title": "Земля для космодрому",
          "assetID": "UA-2017-08-14-000001",
          "value": {
            "currency": "UAH",
            "amount": 100.0,
            "valueAddedTaxIncluded": true
          },
          "dateModified": "2017-08-14T13:35:31.474578+03:00",
          "owner": "broker",
          "assetCustodian": {
            "contactPoint": {
              "name": "Державне управління справами",
              "telephone": "0440000000"
            },
            "identifier": {
              "scheme": "UA-EDR",
              "id": "00037256",
              "uri": "http://www.dus.gov.ua/"
            },
            "name": "Державне управління справами",
            "address": {
              "postalCode": "01220",
              "countryName": "Україна",
              "streetAddress": "вул. Банкова, 11, корпус 1",
              "region": "м. Київ",
              "locality": "м. Київ"
            }
          },
          "address": {
            "postalCode": "79000",
            "countryName": "Україна",
            "streetAddress": "вул. Банкова 1",
            "region": "м. Київ",
            "locality": "м. Київ"
          },
          "date": "2017-08-14T13:35:31.472331+03:00",
          "id": "2f684c8a57f447768a5a451e2e8e5892",
          "unit": {
            "code": "39513200-3",
            "name": "item"
          },
          "quantity": 5
        }
      }


   :reqheader Authorization: optional OAuth token to authenticate
   :statuscode 200: no error
   :statuscode 404: asset not found
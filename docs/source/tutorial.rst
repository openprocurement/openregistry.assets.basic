.. _tutorial:

Tutorial
========

Exploring basic rules
---------------------

Let's try exploring the `/assets` endpoint:

.. literalinclude:: tutorial/asset-listing.http
   :language: javascript

Just invoking it reveals empty set.

Now let's attempt creating some asset:

.. literalinclude:: tutorial/asset-post-attempt.http
   :language: javascript

Error states that the only accepted Content-Type is `application/json`.

Let's satisfy the Content-type requirement:

.. literalinclude:: tutorial/asset-post-attempt-json.http
   :language: javascript

Error states that no `data` has been found in JSON body.


.. index:: Asset

Creating asset
--------------


Let's create asset with the minimal (only required) data set:

.. literalinclude:: tutorial/create-asset.http
   :language: javascript

Success! Now we can see that new object was created. Response code is `201`
and `Location` response header reports the location of the created object.  The
body of response reveals the information about the created asset: its internal
`id` (that matches the `Location` segment), its official `assetID` and
`dateModified` datestamp stating the moment in time when asset was last
modified. Pay attention to the `assetType`. Note that asset is
created with `pending` status.

Let's access the URL of the created object (the `Location` header of the response):

.. literalinclude:: tutorial/blank-asset-view.http
   :language: javascript

.. XXX body is empty for some reason (printf fails)

We can see the same response we got after creating asset.

Let's see what listing of assets reveals us:

.. literalinclude:: tutorial/initial-asset-listing.http
   :language: javascript

We do see the internal `id` of a asset (that can be used to construct full URL by prepending `http://lb.api-sandbox.registry.openprocurement.net/api/0/assets/`) and its `dateModified` datestamp.

The previous asset contained only required fields. Let's try creating asset with more data
(asset has status `created`):

.. literalinclude:: tutorial/create-second-asset.http
   :language: javascript

And again we have `201 Created` response code, `Location` header and body with extra `id`, `assetID`, and `dateModified` properties.

Let's check what asset registry contains:

.. literalinclude:: tutorial/listing-with-some-assets.http
   :language: javascript

And indeed we have 2 assets now.

Modifying Asset
---------------

Let's update asset description:

.. literalinclude:: tutorial/patch-asset.http
   :language: javascript

.. XXX body is empty for some reason (printf fails)

We see the added properies have merged with existing asset data. Additionally, the `dateModified` property was updated to reflect the last modification datestamp.

Checking the listing again reflects the new modification date:

.. literalinclude:: tutorial/asset-listing-after-patch.http
   :language: javascript


Deleting Asset
--------------

Let's delete asset:

.. literalinclude:: tutorial/delete-asset.http
   :language: javascript



Integration with lots
---------------------


.. literalinclude:: tutorial/attached-to-lot-asset-view.http
   :language: javascript


.. literalinclude:: tutorial/detached-from-lot-asset-view.http
   :language: javascript


.. literalinclude:: tutorial/complete-asset-view.http
      :language: javascript

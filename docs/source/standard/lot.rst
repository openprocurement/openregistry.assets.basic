.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: lot

.. _lot:

Lot
====

Schema
------

:id:
    string, auto-generated, read-only
    
:lotID:
   string, auto-generated, read-only

   The lot identifier to refer that lot to in the `paper` documentation. 

   |ocdsDescription|
   LotID is included to make the flattened data structure more convenient.
   
:date:
    string, auto-generated, read-only
    
    The date of lot creation/undoing.
    
:dateModified:    
    string, auto-generated, read-only
    
    |ocdsDescription|
    Date when the lot was last modified.
    
:status:
    string, required
    
    The lot status within the Registry.
    
:assets:
    string, optional
    
    ID of the related :ref:`basic assets`.
    
:lotType:
    string, required

    Type of the given lot.

:title:
    string, multilingual
    
    * Ukrainian by default (required) - Ukrainian title
    
    * ``title_en`` (English) - English title
    
    * ``title_ru`` (Russian) - Russian title
    
    Oprionally can be mentioned in English/Russian.
    
:description:
    string, multilingual, optional
    
    |ocdsDescription|
    A description of the goods, services to be provided.
    
    * Ukrainian by default - Ukrainian decription
    
    * ``decription_en`` (English) - English decription
    
    * ``decription_ru`` (Russian) - Russian decription
    
:documents:
    
    |ocdsDescription|
    All related documents and attachments.
    
:lotCustodian:
   string, required

   An entity managing the lot.

:mode:
    optional
    
    The additional parameter with a value ``test``.

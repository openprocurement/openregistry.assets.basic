.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: basic asset, Parameter, Classification, Unit, Value

.. _basic asset:

Basic Asset
==================================================================================

Schema
------

:id:
    string, auto-generated, read-only
    
:assetID:
   string, auto-generated, read-only

   The asset identifier to refer it to in the `paper` documentation. 

   |ocdsDescription|
   AssetID is included to make the flattened data structure more convenient.
   
:date:
    string, auto-generated, read-only
    
    The date of asset creation/undoing.
    
:dateModified:    
    string, auto-generated, read-only
    
    |ocdsDescription|
    Date when the asset was last modified.
    
:mode:
    optional
    
    The additional parameter with a value ``test``.
    
:status:
    string, required
    
    The asset status within the Registry.
    
:value:
    :ref:`Value`, required 
    
    Estimated asset value.
    
:relatedLot:
    string, required in `active` status
    
    ID of the related Lot.
    
:assetType:
    string, required

    Type of the given asset.

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
    
:assetCustodian:
   :ref:`Organization`, required

   The entity managing the asset.
    
:classification:
    :ref:`Classification`, required

    The primary classification for the asset.

    It is required for `classification.scheme` to be `CPV`. The
    `classification.id` should be valid CPV code.

:additionalClassifications:
    List of :ref:`Classification` objects, optioanl

    |ocdsDescription|
    An array of additional classifications for the item. See the
    `itemClassificationScheme` codelist for common options to use in OCDS. 
    This may also be used to present codes from an internal classification
    scheme.

    One of the possible additional classifiers is CPVS.

:unit:
    :ref:`Unit`, required

    |ocdsDescription| 
    Description of the unit which the good comes in e.g.  hours, kilograms. 
    Made up of a unit name, and the value of a single unit.

:quantity:
    integer, required

    |ocdsDescription|
    The number of units required.

:location:
    dictionary

    Geographical coordinates of the location. Element consists of the following items:

    :latitude:
        string, required
    :longitude:
        string, required
    :elevation:
        string, optional, usually not used
        
.. _assets_workflow: 

Assets Workflow
==============

.. graphviz::

    digraph G {
            node [style=filled, color=lightgrey];
            edge[style=dashed];
            "draft" -> "pending";
            edge[style=dashed]
            "pending" -> "deleted";
            edge[style=solid];
            "pending" -> "locked";
            edge[style=solid];
            "locked" -> "pending";
            edge[style=solid];
            "locked" -> "active";
            edge[style=solid];
            "active" -> "pending";
            edge[style=solid];
            "active" -> "complete";
    }


Legend
--------

   * dashed line - user action
    
   * solid line - action is done automatically

.. _Classification:

Classification
==============

Schema
------

:scheme:
    string

    |ocdsDescription|
    A classification should be drawn from an existing scheme or list of
    codes.  This field is used to indicate the scheme/codelist from which
    the classification is drawn.  For line item classifications, this value
    should represent a known Item Classification Scheme wherever possible.

:id:
    string

    |ocdsDescription|
    The classification code drawn from the selected scheme.

:description:
    string

    |ocdsDescription|
    A textual description or title for the code.

:uri:
    uri

    |ocdsDescription|
    A URI to identify the code. In the event individual URIs are not
    available for items in the identifier scheme this value should be left
    blank.

.. _Unit:

Unit
====

Schema
------

:code:
    string, required

    UN/CEFACT Recommendation 20 unit code.

:name:
    string

    |ocdsDescription|
    Name of the unit
    
.. _value:

Value
===============

Schema
------

:amount:    
    float, required

    Should be positive.
    
:currency:
    string, required
    
    |ocdsDescription|
    The currency in 3-letter ISO 4217 format.
    
:valueAddedTaxIncluded:
    bool, required

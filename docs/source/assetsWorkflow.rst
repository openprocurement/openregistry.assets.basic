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
            "pending" -> "verification";
            edge[style=solid];
            "verification" -> "pending";
            edge[style=solid];
            "verification" -> "active";
            edge[style=solid];
            "active" -> "pending";
            edge[style=solid];
            "active" -> "complete";
    }


Legend
--------

   * dashed line - user action
    
   * solid line - action is done automatically
 

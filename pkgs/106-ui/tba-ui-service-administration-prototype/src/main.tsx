import { dashboard } from "../../_prototype/dashboard";
import "../../_prototype/styles.css";

dashboard("Service Administration", "Review service identities and audit activity from the local prototype.", [
  {
    "name": "Services",
    "path": "/api/services",
    "columns": [
      [
        "Service",
        "name"
      ],
      [
        "Identity",
        "id"
      ],
      [
        "Status",
        "state"
      ]
    ]
  },
  {
    "name": "Audit events",
    "path": "/api/audit",
    "columns": [
      [
        "Action",
        "action"
      ],
      [
        "Actor",
        "actor"
      ],
      [
        "Time",
        "timestamp"
      ]
    ]
  }
]);

import { dashboard } from "../../_prototype/dashboard";
import "../../_prototype/styles.css";

dashboard("Directory SCIM Center", "Inspect sample connections and the provisioning events they produce.", [
  {
    "name": "Connections",
    "path": "/api/admin/connections",
    "columns": [
      [
        "Connection",
        "name"
      ],
      [
        "Profile",
        "sourceProfile"
      ],
      [
        "Status",
        "lifecycleState"
      ]
    ]
  },
  {
    "name": "Events",
    "path": "/api/admin/events",
    "columns": [
      [
        "Operation",
        "operation"
      ],
      [
        "Outcome",
        "status"
      ],
      [
        "Summary",
        "summary"
      ]
    ]
  }
]);

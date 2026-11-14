import { dashboard } from "../../_prototype/dashboard";
import "../../_prototype/styles.css";

dashboard("Directory Provisioning SCIM", "Review sample provisioning connections and recent directory activity.", [
  {
    "name": "Connections",
    "path": "/api/connections",
    "columns": [
      [
        "Connection",
        "name"
      ],
      [
        "Profile",
        "vendorProfile"
      ],
      [
        "Status",
        "status"
      ]
    ]
  },
  {
    "name": "Directory users",
    "path": "/api/directory/users",
    "columns": [
      [
        "Name",
        "displayName"
      ],
      [
        "Username",
        "userName"
      ],
      [
        "Active",
        "active"
      ]
    ]
  }
]);

import { dashboard } from "../../_prototype/dashboard";
import "../../_prototype/styles.css";

dashboard("Authenticator Center", "Inspect the sample account’s authenticators and enrollment catalog.", [
  {
    "name": "Authenticators",
    "path": "/api/account/authenticators",
    "columns": [
      [
        "Label",
        "displayName"
      ],
      [
        "Method",
        "kind"
      ],
      [
        "State",
        "state"
      ]
    ]
  },
  {
    "name": "Enrollment catalog",
    "path": "/api/account/authenticators/catalog",
    "columns": [
      [
        "Name",
        "title"
      ],
      [
        "Method",
        "kind"
      ],
      [
        "Description",
        "description"
      ]
    ]
  }
]);

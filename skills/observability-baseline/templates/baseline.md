# Observability baseline — <app>

No secrets here: DSNs, webhook URLs with tokens, passwords and connection
strings are referenced by environment variable name only.

| Item | State | Evidence | Last proven | Watches |
| --- | --- | --- | --- | --- |
| Logs | <IN PLACE / ADDED / MISSING / NOT APPLICABLE> | <request id found in host logs> | <YYYY-MM-DD> | <host> |
| Health | | <livez/readyz results with DB stopped> | | <routes> |
| Errors | | <test event link> | | <tracker project> |
| Uptime | | <last successful probe> | | <url> |
| Alert | | <received on channel, SUPPLIED by whom> | | <channel> |
| Backups | | <restored backup of …, row compared> | | <database> |
| Runbook | | docs/runbook.md, commands run | | — |

Re-prove an item when what it watches changes.

## History

- <YYYY-MM-DD> · <item> · <why it changed: first launch / incident <ref> / new host>

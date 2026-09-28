# Decisions

2026-09-28  Skills stay routerless; orchestration is a separate opt-in layer
            (delivery-lead, like skills-pipeline) that sequences tickets and never
            states another skill's verdict.                      OBSERVED user: "finish these all"
2026-09-28  Tickets are tracker-agnostic: .delivery/ is the working copy, synced to
            whatever tracker the project uses (Jira, Trello, Nextcloud Deck, ...),
            moved automatically within autonomy set once.        OBSERVED user

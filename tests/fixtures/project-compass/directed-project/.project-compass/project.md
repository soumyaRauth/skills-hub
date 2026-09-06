# Project

**Is**        Warehouse inventory reconciliation                     OBSERVED
**For**       Warehouse staff and their managers                     OBSERVED
**Objective** Replace the pilot customer's paper reconciliation      OBSERVED (README)
**Workflows** intake -> adjustment -> approval -> reconciliation      OBSERVED
**Domain**    Warehouse - Adjustment - Reconciliation                OBSERVED
**Lifecycle** Adjustment: draft/submitted/approved/rejected, enforced
              in src/adjustments/state.js and by a CHECK constraint  OBSERVED
**State**     DIRECTED - reconciliation work is coherent and recent
**Verified**  2026-09-02

ALTER TABLE "Order" ADD COLUMN "region" TEXT NOT NULL;

CREATE INDEX "Order_region_createdAt_idx" ON "Order"("region", "createdAt");

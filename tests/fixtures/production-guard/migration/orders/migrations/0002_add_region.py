from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="order",
            name="region",
            field=models.CharField(max_length=64),
        ),
        migrations.RunSQL(
            sql="""
                UPDATE orders
                SET region = COALESCE(
                    (SELECT a.region FROM addresses a WHERE a.order_id = orders.id),
                    ''
                )
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AddIndex(
            model_name="order",
            index=models.Index(fields=["region"], name="orders_region_idx"),
        ),
    ]

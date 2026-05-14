from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(choices=[("create", "Criacao"), ("update", "Atualizacao"), ("delete", "Exclusao logica"), ("approve", "Aprovacao"), ("cancel", "Cancelamento"), ("login", "Login"), ("fiscal", "Emissao fiscal"), ("financial", "Movimentacao financeira"), ("stock", "Movimentacao estoque"), ("system", "Sistema")], db_index=True, max_length=30)),
                ("module", models.CharField(db_index=True, max_length=80)),
                ("record_model", models.CharField(db_index=True, max_length=120)),
                ("record_id", models.CharField(blank=True, db_index=True, max_length=80)),
                ("record_repr", models.CharField(blank=True, max_length=220)),
                ("before", models.JSONField(blank=True, default=dict)),
                ("after", models.JSONField(blank=True, default=dict)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="global_audit_logs", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at", "-id"],
            },
        ),
        migrations.CreateModel(
            name="EventLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_name", models.CharField(db_index=True, max_length=80)),
                ("module", models.CharField(db_index=True, max_length=80)),
                ("aggregate_type", models.CharField(db_index=True, max_length=120)),
                ("aggregate_id", models.CharField(blank=True, db_index=True, max_length=80)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("status", models.CharField(choices=[("pending", "Pendente"), ("processed", "Processado"), ("partial", "Parcial"), ("failed", "Falhou")], db_index=True, default="pending", max_length=20)),
                ("handlers_processed", models.JSONField(blank=True, default=list)),
                ("error_message", models.TextField(blank=True)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("processed_at", models.DateTimeField(blank=True, null=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="event_logs", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at", "-id"],
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("message", models.TextField()),
                ("level", models.CharField(choices=[("info", "Informacao"), ("success", "Sucesso"), ("warning", "Aviso"), ("critical", "Critico")], db_index=True, default="info", max_length=20)),
                ("category", models.CharField(db_index=True, max_length=80)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("is_read", models.BooleanField(db_index=True, default=False)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("event", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="notifications", to="core.eventlog")),
                ("recipient", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at", "-id"],
            },
        ),
        migrations.AddIndex(model_name="auditlog", index=models.Index(fields=["module", "action", "created_at"], name="core_auditl_module_9ccf7d_idx")),
        migrations.AddIndex(model_name="auditlog", index=models.Index(fields=["record_model", "record_id"], name="core_auditl_record__18f191_idx")),
        migrations.AddIndex(model_name="auditlog", index=models.Index(fields=["user", "created_at"], name="core_auditl_user_id_495f2e_idx")),
        migrations.AddIndex(model_name="eventlog", index=models.Index(fields=["event_name", "status"], name="core_eventl_event_n_544a01_idx")),
        migrations.AddIndex(model_name="eventlog", index=models.Index(fields=["module", "created_at"], name="core_eventl_module_c77cb5_idx")),
        migrations.AddIndex(model_name="eventlog", index=models.Index(fields=["aggregate_type", "aggregate_id"], name="core_eventl_aggrega_f7b09a_idx")),
        migrations.AddIndex(model_name="notification", index=models.Index(fields=["recipient", "is_read", "created_at"], name="core_notifi_recipie_6ddc27_idx")),
        migrations.AddIndex(model_name="notification", index=models.Index(fields=["category", "level"], name="core_notifi_categor_5ae9ca_idx")),
    ]

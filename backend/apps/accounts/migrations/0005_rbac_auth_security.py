import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_add_diretoria_role"),
    ]

    operations = [
        migrations.AddField(model_name="user", name="telefone", field=models.CharField(blank=True, max_length=30)),
        migrations.AddField(model_name="user", name="cargo", field=models.CharField(blank=True, max_length=120)),
        migrations.CreateModel(
            name="Permission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(db_index=True, max_length=120, unique=True)),
                ("module", models.CharField(db_index=True, max_length=60)),
                ("action", models.CharField(db_index=True, max_length=60)),
                ("description", models.CharField(blank=True, max_length=180)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={"ordering": ["module", "code"]},
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(db_index=True, max_length=50, unique=True)),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("is_system", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="AuthAuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("event", models.CharField(choices=[("login_success", "Login realizado"), ("login_failed", "Login falhou"), ("logout", "Logout"), ("password_change", "Troca de senha")], db_index=True, max_length=30)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                ("username_attempted", models.CharField(blank=True, max_length=180)),
                ("success", models.BooleanField(db_index=True, default=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="auth_audit_logs", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.CreateModel(
            name="RolePermission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("permission", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="roles", to="accounts.permission")),
                ("role", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="role_permissions", to="accounts.role")),
            ],
        ),
        migrations.CreateModel(
            name="UserRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_primary", models.BooleanField(default=False)),
                ("role", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="role_users", to="accounts.role")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="role_memberships", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(model_name="permission", index=models.Index(fields=["module", "action", "is_active"], name="accounts_pe_module_533150_idx")),
        migrations.AddIndex(model_name="role", index=models.Index(fields=["code", "is_active"], name="accounts_ro_code_e6d65b_idx")),
        migrations.AddIndex(model_name="authauditlog", index=models.Index(fields=["user", "event"], name="accounts_au_user_23c9b8_idx")),
        migrations.AddIndex(model_name="authauditlog", index=models.Index(fields=["event", "created_at"], name="accounts_au_event_0d1b0d_idx")),
        migrations.AddIndex(model_name="rolepermission", index=models.Index(fields=["role", "permission"], name="accounts_ro_role_4cfa8b_idx")),
        migrations.AddIndex(model_name="userrole", index=models.Index(fields=["user", "is_primary"], name="accounts_us_user_b24f00_idx")),
        migrations.AddConstraint(model_name="rolepermission", constraint=models.UniqueConstraint(fields=("role", "permission"), name="accounts_role_permission_uniq")),
        migrations.AddConstraint(model_name="userrole", constraint=models.UniqueConstraint(fields=("user", "role"), name="accounts_user_role_uniq")),
    ]

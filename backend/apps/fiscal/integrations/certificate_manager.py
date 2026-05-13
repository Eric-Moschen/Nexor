from django.core import signing


class CertificateManager:
    def protect_password(self, raw_password):
        if not raw_password:
            return ""
        return signing.dumps(raw_password, salt="nexor-fiscal-certificate")

    def reveal_password(self, protected_password):
        if not protected_password:
            return ""
        return signing.loads(protected_password, salt="nexor-fiscal-certificate")

    def validate_certificate(self, empresa):
        return bool(empresa.certificado_a1 and empresa.certificado_senha_protegida)

from apps.relatorios.selectors import comercial_indicadores


class ComercialDashboard:
    def build(self, filtros=None):
        return comercial_indicadores(filtros)

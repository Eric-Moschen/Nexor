from apps.relatorios.selectors import estoque_indicadores


class EstoqueDashboard:
    def build(self, filtros=None):
        return estoque_indicadores(filtros)

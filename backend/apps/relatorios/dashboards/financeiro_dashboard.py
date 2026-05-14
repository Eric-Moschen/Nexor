from apps.relatorios.selectors import financeiro_indicadores


class FinanceiroDashboard:
    def build(self, filtros=None):
        return financeiro_indicadores(filtros)

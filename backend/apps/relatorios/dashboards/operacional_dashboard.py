from apps.relatorios.selectors import operacional_indicadores


class OperacionalDashboard:
    def build(self, filtros=None):
        return operacional_indicadores(filtros)

# Exceção para filtros inválidos (min > max)
class InvalidFilterException(Exception):
    def __init__(self, message: str = "Parâmetro de filtro inválido."):
        self.message = message
        super().__init__(self.message)

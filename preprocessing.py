from food_statistics import Statistics
from typing import Dict, List, Set, Any

class MissingValueProcessor:
    """
    Processa valores ausentes (representados como None) no dataset.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        """Retorna as colunas a serem processadas. Se 'columns' for vazio, retorna todas as colunas."""
        return list(columns) if columns else list(self.dataset.keys())

    def isna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Retorna um novo dataset contendo apenas as linhas que possuem
        pelo menos um valor nulo (None) em uma das colunas especificadas.

        Args:
            columns (Set[str]): Um conjunto de nomes de colunas a serem verificadas.
                               Se vazio, todas as colunas são consideradas.

        Returns:
            Dict[str, List[Any]]: Um dicionário representando as linhas com valores nulos.
        """
        
        colunas_verificar = self._get_target_columns(columns)

        novo_dicionario = {col: [] for col in self.dataset}

        numero_linhas = len(self.dataset[next(iter(self.dataset))])

        for i in range(numero_linhas):
            if any(self.dataset[coluna][i] is None for coluna in colunas_verificar):
                for coluna in self.dataset:
                    novo_dicionario[coluna].append(self.dataset[coluna][i])

        return novo_dicionario

    def notna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Retorna um novo dataset contendo apenas as linhas que não possuem
        valores nulos (None) em nenhuma das colunas especificadas.

        Args:
            columns (Set[str]): Um conjunto de nomes de colunas a serem verificadas.
                               Se vazio, todas as colunas são consideradas.

        Returns:
            Dict[str, List[Any]]: Um dicionário representando as linhas sem valores nulos.
        """
        
        colunas_verificar = self._get_target_columns(columns)

        novo_dicionario = {col: [] for col in self.dataset}

        numero_linhas = len(self.dataset[next(iter(self.dataset))])

        for i in range(numero_linhas):
            if all(self.dataset[col][i] is not None for col in colunas_verificar):
                for col in self.dataset:
                    novo_dicionario[col].append(self.dataset[col][i])

        return novo_dicionario

    def fillna(self, columns: Set[str] = None, method: str = 'mean', default_value: Any = 0):
        """
        Preenche valores nulos (None) nas colunas especificadas usando um método.
        Modifica o dataset da classe.

        Args:
            columns (Set[str]): Colunas onde o preenchimento será aplicado. Se vazio, aplica a todas.
            method (str): 'mean', 'median', 'mode', ou 'default_value'.
            default_value (Any): Valor para usar com o método 'default_value'.
        """
        
        colunas_verificar = self._get_target_columns(columns)

        metodos_statistica = Statistics(self.dataset)

        for coluna in colunas_verificar:
            valor_preenchimento = None

            if method == "mean":
                valor_preenchimento = metodos_statistica.mean(coluna)
            elif method == "median":
                valor_preenchimento = metodos_statistica.median(coluna)
            elif method == "mode":
                modas = metodos_statistica.mode(coluna)
                if modas:
                    valor_preenchimento = modas[0]
            elif method == "default_value":
                valor_preenchimento = default_value
            else:
                raise ValueError(f"Método '{method}' não suportado.")

            if valor_preenchimento is not None:
                self.dataset[coluna] = [valor_preenchimento if valor_coluna is None else valor_coluna for valor_coluna in self.dataset[coluna]]

    def dropna(self, columns: Set[str] = None):
        """
        Remove as linhas que contêm valores nulos (None) nas colunas especificadas.
        Modifica o dataset da classe.

        Args:
            columns (Set[str]): Colunas a serem verificadas para valores nulos. Se vazio, todas as colunas são verificadas.
        """

        self.dataset = self.notna(columns)

class Scaler:
    """
    Aplica transformações de escala em colunas numéricas do dataset.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        return list(columns) if columns else list(self.dataset.keys())

    def minMax_scaler(self, columns: Set[str] = None):
        """
        Aplica a normalização Min-Max ($X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}$)
        nas colunas especificadas. Modifica o dataset.

        Args:
            columns (Set[str]): Colunas para aplicar o scaler. Se vazio, tenta aplicar a todas.
        """
        
        colunas_verificar = self._get_target_columns(columns)

        for coluna in colunas_verificar:
            valores = self.dataset[coluna]

            valores_numericos = [valor_numerico for valor_numerico in valores if isinstance(valor_numerico, (int, float)) and valor_numerico is not None ]

            if not valores_numericos:
                continue

            valor_minimo = min(valores_numericos)
            valor_maximo = max(valores_numericos)
            intervalo_valores = valor_maximo - valor_minimo

            valores_escalonados = []
            if intervalo_valores == 0:
                valores_escalonados = [0.0 if isinstance(valor, (int, float)) else valor for valor in valores]
            else:
                for valor in valores:
                    if isinstance(valor, (int, float)):
                        valor_escalonado = (valor - valor_minimo) / intervalo_valores
                        valores_escalonados.append(valor_escalonado)
                    else:
                        valores_escalonados.append(valor)
                
            self.dataset[coluna] = valores_escalonados

    def standard_scaler(self, columns: Set[str] = None):
        """
        Aplica a padronização Z-score ($X_{std} = \frac{X - \mu}{\sigma}$)
        nas colunas especificadas. Modifica o dataset.

        Args:
            columns (Set[str]): Colunas para aplicar o scaler. Se vazio, tenta aplicar a todas.
        """
        colunas_verificar = self._get_target_columns(columns)

        processor = MissingValueProcessor(self.dataset)

        valores_filtrados = processor.notna()

        metodos_statistica = Statistics(valores_filtrados)

        for coluna in colunas_verificar:
            valores = self.dataset[coluna]

            valores_numericos = [valor_numerico for valor_numerico in valores if isinstance(valor_numerico, (int, float)) and valor_numerico is not None]

            if not valores_numericos:
                continue

            media_aritmetica = metodos_statistica.mean(coluna)
            desvio_padrao = metodos_statistica.stdev(coluna)

            valores_escalonados = []
            if desvio_padrao == 0:
                valores_escalonados = [0.0 if isinstance(valor, (int, float)) else valor for valor in valores]
            else:
                for valor in valores:
                    if isinstance(valor, (int, float)):
                        valor_escalonado = (valor - media_aritmetica) / desvio_padrao
                        valores_escalonados.append(valor_escalonado)
                    else:
                        valores_escalonados.append(valor)

            self.dataset[coluna] = valores_escalonados

class Encoder:
    """
    Aplica codificação em colunas categóricas.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def label_encode(self, columns: Set[str]):
        """
        Converte cada categoria em uma coluna em um número inteiro.
        Modifica o dataset.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """

        for coluna in columns:
            if coluna not in self.dataset:
                continue
    
            valores = self.dataset[coluna]
            categorias = sorted({valor for valor in valores if valor is not None})  
            mapa_categorias = {categoria: i for i, categoria in enumerate(categorias)}

            colunas_codificadas = []
            for valor in valores:
                if valor is None:
                    colunas_codificadas.append(None)
                else:
                    colunas_codificadas.append(mapa_categorias[valor])

            self.dataset[coluna] = colunas_codificadas


    def oneHot_encode(self, columns: Set[str]):
        """
        Cria novas colunas binárias para cada categoria nas colunas especificadas (One-Hot Encoding).
        Modifica o dataset adicionando e removendo colunas.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """
        
        for coluna in columns:
            valores = self.dataset[coluna]
            categorias = sorted({val for val in valores if val is not None})

            for categoria in categorias:
                nova_coluna = f"{coluna}_{categoria}"
            
                valores_nova_coluna = [1 if valor == categoria else 0 for valor in valores]

                self.dataset[nova_coluna] = valores_nova_coluna

            del self.dataset[coluna]

class Preprocessing:
    """
    Classe principal que orquestra as operações de pré-processamento de dados.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset
        self._validate_dataset_shape()
        
        # Atributos compostos para cada tipo de tarefa
        self.statistics = Statistics(self.dataset)
        self.missing_values = MissingValueProcessor(self.dataset)
        self.scaler = Scaler(self.dataset)
        self.encoder = Encoder(self.dataset)

    def _validate_dataset_shape(self):
        """
        Valida se todas as listas (colunas) no dicionário do dataset
        têm o mesmo comprimento.
        """

        tamanho_lista_referencia = len(next(iter(self.dataset.values())))
        
        for _, valores in self.dataset.items():
            if len(valores) != tamanho_lista_referencia:
                raise ValueError("Todas as colunas no dataset devem ter o mesmo tamanho.")

    def isna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.isna(). Retorna as linhas com valores nulos.
        """
        return self.missing_values.isna(columns=columns)

    def notna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.notna(). Retorna as linhas sem valores nulos.
        """
        return self.missing_values.notna(columns=columns) 

    def fillna(self, columns: Set[str] = None, method: str = 'mean', default_value: Any = 0):
        """
        Atalho para missing_values.fillna(). Preenche valores nulos.
        Retorna 'self' para permitir encadeamento de métodos.
        """
        self.missing_values.fillna(columns=columns, method=method, default_value=default_value) 
        return self

    def dropna(self, columns: Set[str] = None):
        """
        Atalho para missing_values.dropna(). Remove linhas com valores nulos.
        Retorna 'self' para permitir encadeamento de métodos.
        """
        self.missing_values.dropna(columns=columns) #TROCA
        return self

    def scale(self, columns: Set[str] = None, method: str = 'minMax'):
        """
        Aplica escalonamento nas colunas especificadas.

        Args:
            columns (Set[str]): Colunas para aplicar o escalonamento.
            method (str): O método a ser usado: 'minMax' ou 'standard'.

        Retorna 'self' para permitir encadeamento de métodos.
        """
        if method == 'minMax':
            self.scaler.minMax_scaler(columns=columns) #TROCA
        elif method == 'standard':
            self.scaler.standard_scaler(columns=columns) #TROCA
        else:
            raise ValueError(f"Método de escalonamento '{method}' não suportado. Use 'minMax' ou 'standard'.")
        return self

    def encode(self, columns: Set[str], method: str = 'label'):
        """
        Aplica codificação nas colunas especificadas.

        Args:
            columns (Set[str]): Colunas para aplicar a codificação.
            method (str): O método a ser usado: 'label' ou 'oneHot'.
        
        Retorna 'self' para permitir encadeamento de métodos.
        """
        if not columns:
            print("Aviso: Nenhuma coluna especificada para codificação. Nenhuma ação foi tomada.")
            return self

        if method == 'label':
            self.encoder.label_encode(columns=columns) #TROCA
        elif method == 'oneHot':
            self.encoder.oneHot_encode(columns=columns) #TROCA
        else:
            raise ValueError(f"Método de codificação '{method}' não suportado. Use 'label' ou 'oneHot'.")
        return self

class Statistics:
    """
    Uma classe para realizar cálculos estatísticos em um conjunto de dados.

    Atributos
    ----------
    dataset : dict[str, list]
        O conjunto de dados, estruturado como um dicionário onde as chaves
        são os nomes das colunas e os valores são listas com os dados.
    """
    def __init__(self, dataset):
        """
        Inicializa o objeto Statistics.

        Parâmetros
        ----------
        dataset : dict[str, list]
            O conjunto de dados, onde as chaves representam os nomes das
            colunas e os valores são as listas de dados correspondentes.
        """

        if not isinstance(dataset, dict):
            raise TypeError("O dataset deve ser um dicionário.")
        
        for valor in dataset.values():
            if not isinstance(valor, list):
                raise TypeError("Todos os valores no dicionário do dataset devem ser listas.")
            
        if not dataset:
            raise ValueError("O dataset não pode ser vazio.")
            
        if len( set( len(value) for value in dataset.values() ) ) != 1:
            raise ValueError("Todas as colunas no dataset devem ter o mesmo tamanho.")

        self.dataset = dataset

    def mean(self, column: str) -> float:
        """
        Calcula a média aritmética de uma coluna.

        Fórmula:
        $$ \mu = \frac{1}{N} \sum_{i=1}^{N} x_i $$

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            A média dos valores na coluna.
        """
        self._validate_column(column)
        valores_coluna = self.dataset[column]

        valores_validos = [v for v in valores_coluna if v is not None]

        if not valores_validos:
            raise ValueError(f"A coluna '{column}' está vazia, não é possível calcular a média.")
        
        return sum(valores_validos) / len(valores_validos)

    def _validate_column(self, column: str) -> None:
        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")


    def median(self, column):
        """
        Calcula a mediana de uma coluna.

        A mediana é o valor central de um conjunto de dados ordenado.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            O valor da mediana da coluna.
        """
        self._validate_column(column)
        valores_coluna = self.dataset[column]

        valores_validos = [v for v in valores_coluna if v is not None]

        if not valores_validos:
            raise ValueError(f"A coluna '{column}' está vazia, não é possível calcular a mediana.")
        
        if not all(isinstance(v, (int, float)) for v in valores_validos):
            raise TypeError(f"A coluna '{column}' contém valores não numéricos, impossível calcular a mediana.")

        quantidade_valores = len(valores_coluna)
        coluna_ordenada = sorted(valores_coluna)
        indice = quantidade_valores // 2
        
        if quantidade_valores % 2 == 0:
            return (coluna_ordenada[indice - 1] + coluna_ordenada[indice]) / 2
        else: 
            return coluna_ordenada[indice]


    def mode(self, column):
        """
        Encontra a moda (ou modas) de uma coluna.

        A moda é o valor que aparece com mais frequência no conjunto de dados.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        list
            Uma lista contendo o(s) valor(es) da moda.
        """

        
        self._validate_column(column)
        valores_coluna = self.dataset[column]
        
        valores_coluna = [v for v in self.dataset[column] if v is not None]
        
        if not valores_coluna:
            raise ValueError(f"A coluna '{column}' está vazia, não é possível calcular a moda.")

        frequencias = self.absolute_frequency(column=column)
            
        numero_maximo_repeticoes = max(frequencias.values())

        modas = [k for k, v in frequencias.items() if v == numero_maximo_repeticoes]

        return modas
       
    def stdev(self, column):
        """
        Calcula o desvio padrão populacional de uma coluna.

        Fórmula:
        $$ \sigma = \sqrt{\frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}} $$

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            O desvio padrão dos valores na coluna.
        """
        
        self._validate_column(column)
        valores_coluna = self.dataset[column]

        valores_validos = [v for v in valores_coluna if v is not None]

        if not valores_validos:
            raise ValueError(f"A coluna '{column}' está vazia, não é possível calcular o desvio padrão.")
        
        variancia = self.variance(column=column)
        return variancia ** 0.5

    def variance(self, column):
        """
        Calcula a variância populacional de uma coluna.

        Fórmula:
        $$ \sigma^2 = \frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N} $$

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            A variância dos valores na coluna.
        """
        media_aritimetica = self.mean(column)
        self._validate_column(column)

        valores_coluna = self.dataset[column]

        valores_validos = [v for v in valores_coluna if v is not None]

        if not valores_validos:
            raise ValueError(f"A coluna '{column}' está vazia, não é possível calcular a variância.")

        soma = sum( (valor - media_aritimetica) ** 2 for valor in valores_coluna )

        variancia = soma / len(valores_validos)

        return variancia


    def covariance(self, column_a, column_b):
        """
        Calcula a covariância entre duas colunas.

        Fórmula:
        $$ \text{cov}(X, Y) = \frac{\sum_{i=1}^{N} (x_i - \mu_x)(y_i - \mu_y)}{N} $$

        Parâmetros
        ----------
        column_a : str
            O nome da primeira coluna (X).
        column_b : str
            O nome da segunda coluna (Y).

        Retorno
        -------
        float
            O valor da covariância entre as duas colunas.
        """
        self._validate_column(column_a, column_b)
        
        valores_coluna_a = self.dataset[column_a]
        valores_coluna_b = self.dataset[column_b]

        if not valores_coluna_a or not valores_coluna_b:
            raise ValueError(f"A coluna '{column_a}' ou {column_b} está vazia, não é possível calcular a covariância.")

        pares_validos = [(a, b) for a, b in zip(valores_coluna_a, valores_coluna_b) if a is not None and b is not None]

        if not pares_validos:
            raise ValueError(f"Não há pares válidos entre '{column_a}' e '{column_b}' para calcular a covariância.")


        media_coluna_a = self.mean(column_a)
        media_coluna_b = self.mean(column_b)

        soma = sum( (valor_a - media_coluna_a) * (valor_b - media_coluna_b) for valor_a, valor_b in zip(valores_coluna_a, valores_coluna_b))

        quantidade_pares = len(valores_coluna_a)

        return soma / quantidade_pares

    def itemset(self, column):
        """
        Retorna o conjunto de itens únicos em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        set
            Um conjunto com os valores únicos da coluna.
        """
        self._validate_column(column)
        valores_coluna = self.dataset[column]

        if not valores_coluna:
            raise ValueError(f"A coluna '{column}' está vazia, não é possível calcular o itemset.")
        
        return set(valores_coluna)

    def absolute_frequency(self, column):
        """
        Calcula a frequência absoluta de cada item em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os itens e os valores são
            suas contagens (frequência absoluta).
        """

        self._validate_column(column)
        valores_coluna = self.dataset[column]

        if not valores_coluna:
            raise ValueError(f"A coluna '{column}' está vazia, não é possível calcular a frequência absoluta.")

        frequencia = {}
        for value in valores_coluna:
            if value in frequencia:
                frequencia[value] += 1
            else:
                frequencia[value] = 1

        return frequencia


    def relative_frequency(self, column):
        """
        Calcula a frequência relativa de cada item em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os itens e os valores são
            suas proporções (frequência relativa).
        """

        frequencia_absoluta = self.absolute_frequency(column)
        valores_coluna = self.dataset[column]

        frequencia_relativa = {}
        numero_itens = len(valores_coluna)

        for chave, valor in frequencia_absoluta.items():
            if valor not in frequencia_relativa:
                frequencia_relativa[chave] = valor / numero_itens

        return frequencia_relativa
            
    def cumulative_frequency(self, column, frequency_method='absolute'):
        """
        Calcula a frequência acumulada (absoluta ou relativa) de uma coluna.

        A frequência é calculada sobre os itens ordenados.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        frequency_method : str, opcional
            O método a ser usado: 'absolute' para contagem acumulada ou
            'relative' para proporção acumulada (padrão é 'absolute').

        Retorno
        -------
        dict
            Um dicionário ordenado com os itens como chaves e suas
            frequências acumuladas como valores.
        """

        self._validate_column(column)

        if frequency_method not in {'absolute', 'relative'}:
            raise ValueError("O 'frequency_method' deve ser 'absolute' ou 'relative'.")
    
        if frequency_method == 'absolute':
            frequencia = self.absolute_frequency(column=column)
        else:
            frequencia = self.relative_frequency(column=column)

        chaves_ordenadas = sorted(frequencia.keys())

        frequencia_acumulada_relativa = {}
        soma = 0

        for chave in chaves_ordenadas:
            soma += frequencia[chave]
            frequencia_acumulada_relativa[chave] = soma

        return frequencia_acumulada_relativa
        
    def conditional_probability(self, column, value1, value2):
        """
        Calcula a probabilidade condicional P(X_i = value1 | X_{i-1} = value2).

        Este método trata a coluna como uma sequência e calcula a probabilidade
        de encontrar `value1` imediatamente após `value2`.

        Fórmula: P(A|B) = Contagem de sequências (B, A) / Contagem total de B

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        value1 : any
            O valor do evento consequente (A).
        value2 : any
            O valor do evento condicionante (B).

        Retorno
        -------
        float
            A probabilidade condicional, um valor entre 0 e 1.
        """
        self._validate_column(column)

        valores_coluna = self.dataset[column]

        tamanho_lista = len(valores_coluna)
        evento_b = 0
        evento_a_b = 0

        if tamanho_lista < 2:
            return KeyError(f"Não existe sequência possível")
        
        for i in range(0, tamanho_lista - 1):
            if valores_coluna[i] == value2:
                evento_b += 1
                if valores_coluna[i+1] == value1:
                    evento_a_b += 1
                    
        if evento_b == 0:
            return KeyError(f"Não existe nenhum evento condicional")
    
        return  (evento_a_b / evento_b)

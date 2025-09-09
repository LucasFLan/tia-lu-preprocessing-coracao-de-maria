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
            
        if dataset:
            lista_valores = list(dataset.values())
            tamanho_lista_valores_referencia = len(lista_valores[0])
            for lista in lista_valores[1:]:
                if len(lista) != tamanho_lista_valores_referencia:
                    raise ValueError("Todas as colunas no dataset devem ter o mesmo tamanho.")

        self.dataset = dataset

    def mean(self, column):
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

        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")
   
        valores_coluna = self.dataset[column]

        if not valores_coluna:
            return 0.0
        
        valores_validos = [v for v in valores_coluna if isinstance(v, (int, float))]

        if not valores_validos:
            return 0.0
            
        media_aritmetica = sum(valores_validos) / len(valores_validos)

        return media_aritmetica

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

        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")

        valores_coluna = self.dataset[column]

        if not valores_coluna:
            return 0.0

        quantidade_valores = len(valores_coluna)

        for i in range(quantidade_valores):
            for j in range(0, quantidade_valores - i - 1):
                if valores_coluna[j] > valores_coluna[j + 1]:
                    valores_coluna[j], valores_coluna[j + 1] = valores_coluna[j + 1], valores_coluna[j]
        
        if quantidade_valores % 2 == 0:
            indice = int(quantidade_valores / 2)
            mediana = (valores_coluna[indice-1] + valores_coluna[indice]) / 2
        else: 
            indice_meio = int(quantidade_valores / 2)
            mediana = valores_coluna[indice_meio]

        return mediana

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

        
        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")
        
        valores_coluna = self.dataset[column]

        if not valores_coluna:
            return []

        contador = {}
        for valor in valores_coluna:
            if valor in contador:
                contador[valor] += 1
            else:
                contador[valor] = 1
            
        numero_maximo_repeticoes = max(contador.values())

        modas = []
        for chave, valor in contador.items():
            if(valor == numero_maximo_repeticoes):
                modas.append(chave)

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

    
        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")

        valores_coluna = self.dataset[column]

        if not valores_coluna:
            return 0.0

        media_aritmetica = self.mean(column)

        valores_subtraido_media = []
        for valor in valores_coluna:
            valores_subtraido_media.append(valor - media_aritmetica) 

        soma_valores_ao_quadrado = 0
        for valor_subtraido in valores_subtraido_media:
            valor_ao_quadrado = valor_subtraido ** 2
                
            soma_valores_ao_quadrado += valor_ao_quadrado

        divisao = soma_valores_ao_quadrado / len(valores_coluna)

        desvio_padrao = divisao ** 0.5

        return desvio_padrao
  

        

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
        
        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")        

        valores_coluna = self.dataset[column]

        if not valores_coluna:
            return 0.0

        media_aritimetica = self.mean(column)

        valores_subtraido_media = []
        for valor in valores_coluna:
            valores_subtraido_media.append(valor - media_aritimetica)

        soma = 0
        for valor_subtraido in valores_subtraido_media:
            valor_ao_quadrado = valor_subtraido ** 2
                
            soma += valor_ao_quadrado

        variancia = soma / len(valores_coluna)

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

        if column_a not in self.dataset:
            raise KeyError(f"A coluna a: {column_a} não existe no dataset")
        
        if column_b not in self.dataset:
            raise KeyError(f"A coluna b: {column_b} não existe no dataset")

        valores_coluna_a = self.dataset[column_a]
        valores_coluna_b = self.dataset[column_b]

        if not valores_coluna_a:
            return 0.0

        media_coluna_a = self.mean(column_a)
        media_coluna_b = self.mean(column_b)

        soma = 0
        contador = 0
        for valor_a in valores_coluna_a:
            produto = (valor_a - media_coluna_a) * (valores_coluna_b[contador] - media_coluna_b)

            contador += 1
            soma += produto

        quantidade_pares = len(valores_coluna_a)

        covariancia = soma / quantidade_pares

        return covariancia

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

        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")

        valores_coluna = self.dataset[column]

        if not valores_coluna:
            return set()
        
        valores_unicos = set(valores_coluna)
        
        return valores_unicos

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

        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")

        valores_coluna = self.dataset[column]

        if not valores_coluna:
            return {}

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

        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")

        valores_coluna = self.dataset[column]

        frequencia_absoluta = self.absolute_frequency(column)

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

        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")

        valores_coluna = self.dataset[column]
        quantidade_valores = len(valores_coluna) 

        for i in range(quantidade_valores):
                for j in range(0, quantidade_valores - i - 1):
                    if valores_coluna[j] > valores_coluna[j + 1]:
                        valores_coluna[j], valores_coluna[j + 1] = valores_coluna[j + 1], valores_coluna[j]

        frequencia_acumulada_absoluta = {}

        frequencia_absoluta = self.absolute_frequency(column)

        soma = 0
        for chave, frequencia in frequencia_absoluta.items():
            soma += frequencia
            frequencia_acumulada_absoluta[chave] = soma

        if frequency_method == 'absolute':
            return frequencia_acumulada_absoluta
        elif frequency_method == 'relative':
            frequencia_acumulada_relativa = {}
            for chave, frequencia in frequencia_acumulada_absoluta.items():
                frequencia_acumulada_relativa[chave] = frequencia / quantidade_valores

            return frequencia_acumulada_relativa
        else:
            raise ValueError("O 'frequency_method' deve ser 'absolute' ou 'relative'.")


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

        if column not in self.dataset:
            raise KeyError(f"A coluna '{column}' não existe no dataset.")

        valores_coluna = self.dataset[column]

        tamanho_lista = len(valores_coluna)

        contador = 0
        quantidade_vezes = 0
        for valor in valores_coluna:                      
            if valores_coluna[contador] == value2 and (tamanho_lista-1) > contador:
                if valores_coluna[contador+1] == value1:
                    quantidade_vezes += 1

            contador += 1

        contagem = 0
        i = 0
        for valor in valores_coluna:
            if value2 == valor:
                contagem += 1
                if i == tamanho_lista-1:
                    contagem = contagem - 1
            i += 1

        if contagem == 0:
            return 0.0

        probabilidade_condicional = (quantidade_vezes / contagem)

        return probabilidade_condicional
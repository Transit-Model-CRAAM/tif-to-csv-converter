import cv2                          # Para tratamento da imagem
import numpy as np                  # Para tipagem
import matplotlib.pyplot as plt     # Para plot no jupyter notebook
import math                         # Para calculo
import pandas as pd                  # Para transformação em csv

class Digitalizer: 
    def plot_image(image: np.ndarray) -> None:
        """
        Função para plotar a imagem na tela

        image: imagem
        """
        # Converte de BGR para RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        plt.imshow(rgb_image)
        plt.axis('off')  # Remove os eixos
        plt.show()

    def plot_graph(x: list[float], y: list[float]) -> None:
        """
        Função para plotar o gráfico dos valores

        x: lista de valores em keV
        y: lista de valores de intensidade
        """
        plt.plot(x, y, marker='.', linestyle='-')
        plt.xlabel('keV')
        plt.ylabel('Intensidade')
        plt.title('Gráfico de keV vs Intensidade')
        plt.grid(True)
        plt.show()

    def verify_if_color_is_blue(color: list[int, int, int]) -> bool:
        """
        Função para verificar se o pixel é de cor azul

        color: lista de inteiros em BGR (cor)
        """
        return color[0] >= 200 and color[1] <= 160 and color[2] <= 160

    def find_yaxis_value_per_pixel(graph_image: np.ndarray) -> int:
        """
        Função para achar a distância em pixels do eixo y

        graph_image: imagem
        """
        starting_y = 400
        x = 50

        yf = 26
        points = [starting_y]
        background = False
        for j in range(starting_y, yf-1, -1): # Começa de baixo pra cima
            if not background:
                if graph_image[j][x][0] > 200 and graph_image[j][x][1] > 200 and graph_image[j][x][2] > 200: # Cor de background
                    background = True # Marca como background e procura o próximo tracinho do eixo y
            else:
                if graph_image[j][x][0] < 130 and graph_image[j][x][1] < 130 and graph_image[j][x][2] < 130: # Cor de ponto
                    points.append(j) # guarda o novo ponto
                    background = False # Variável de apoio pra saber quando começar novamente o background

        # Calcula as diferenças entre cada elemento e o anterior (Para poder tirar a média das distâncias)
        diffs = [points[i] - points[i + 1] for i in range(len(points) - 1)]

        # Tira a média das distâncias em pixel
        y_value = sum(diffs) / len(diffs)
        
        return math.ceil(y_value)

    def get_csv_data(self, graph_image: np.ndarray, x0: int, x1: int, y0: int, y1: int, value_per_x_pixel: float, value_per_y_pixel: float, digits: int = 4, x_interval: int = 3):
        """
        Função para transformar os dados da imagem em dados de csv

        graph_image: imagem
        x0: posição inicial em pixels de onde o gráfico começa horizontalmente
        x1: posição final em pixels de onde o gráfico termina horizontalmente
        y0: posição inicial em pixels de onde o gráfico começa verticalmente
        y1: posição final em pixels de onde o gráfico termina verticalmente
        value_per_x_pixel: multiplicador de valor do eixo x para cada pixel
        value_per_y_pixel: multiplicador de valor do eixo y para cada pixel
        digits: quantidade de casas decimais dos valores obtidos para o csv
        x_inverval: intervalo de quantos em quantos pixels vai pegar um valor (eixo x)
        """
        x_values = []
        y_values = []

        old_blue_range = [] # Variável de apoio para saber o range anterior (detecção de picos)
        for j in range(x0, x1, x_interval):
            blue_range = []
            for i in range(y1, y0-1, -1): # Decrescente (Baixo pra cima)
                if len(blue_range) == 1 and not self.verify_if_color_is_blue(graph_image[i][j]): # Se não é mais cor azul
                    blue_range.append(i-1) # Guarda o último ponto da linha vertical de cor azul
                    break
                elif self.verify_if_color_is_blue(graph_image[i][j]):
                    if blue_range == []: # Se ainda não tem nenhum ponto guardado
                        blue_range.append(i) # Início vertical da linha azul
            
            if old_blue_range and old_blue_range[1] < blue_range[1]: # Checagem por picos
                y_to_check = blue_range[1] # Seleciona o pico
            else:
                y_to_check = (blue_range[0] + blue_range[1]) // 2 # Seleciona o meio dos pixeis azuis verticalmente

            x_value = (j - x0) * value_per_x_pixel # Calcula o valor real dada a distância do início do eixo x até o ponto
            if not blue_range:
                y_value = 0
            else:
                y_value = (y1 - y_to_check) * value_per_y_pixel # Calcula o valor real dada a distância do início do eixo y até o ponto

            x_values.append(round(x_value, digits))
            y_values.append(round(y_value, digits))

            old_blue_range = blue_range

        return x_values, y_values

    def curve_check(self, graph_image: np.ndarray, image_height: int, image_width: int) -> None:
        """
        Função para verificação da curva (Apenas visualmente)

        graph_image: imagem
        image_height: altura da imagem em pixels
        image_width: largura da imagem em pixels
        """
        new_graph = graph_image.copy()
        
        for i in range(image_height):
            for j in range(image_width):
                if self.verify_if_color_is_blue(new_graph[i][j]):
                    new_graph[i][j] = [0, 255, 0]

        self.plot_image(new_graph)
class GraphicTiff: 
    '''
    Classe criada para representação de parâmetros base para a criação do plano matricial de conversão
    do arquivo tif para csv 

    parâmetro borda::: 
    parâmetro x0::: 
    parâmetro x1::: 
    parâmetro y0::: 
    parâmetro y1::: 
    parâmetro x_pixel_distance::: 
    parâmetro x_diff::: 
    parâmetro y_diff::: 
    '''
    def __init__(self, borda, x0, x1, y0, y1, x_pixel_distance, x_diff, y_diff):
        self.borda = borda
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0 - borda
        self.y1 = y1 + borda
        self.x_pixel_distance = x_pixel_distance
        self.x_diff = x_diff
        self.y_diff = y_diff